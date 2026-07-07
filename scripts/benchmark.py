import argparse
import csv
import json
import statistics
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from config import (
    DATASET_METADATA_JSON,
    EXPLAIN_DIR,
    INDEX_CONFIG_ORDER,
    MEASURED_RUNS,
    MONGO,
    QUERY_CONSTANTS,
    RESULTS_DIR,
    ROWS,
    WARMUP_RUNS,
)
from db_connections import mongo_client, mysql_conn, postgres_conn
from io_utils import ensure_dirs, write_json, write_text
from manage_indexes import INDEX_CONFIG_LABELS, apply_index_config
from query_definitions import MONGO_QUERIES, MYSQL_QUERIES, POSTGRES_QUERIES

DBMS_LIST = ["postgres", "mysql", "mongo"]
INDEX_CONFIGS = INDEX_CONFIG_ORDER


def strip_sql(sql: str) -> str:
    return " ".join(sql.strip().rstrip(";").split())


def load_dataset_metadata() -> dict[str, Any]:
    if not DATASET_METADATA_JSON.exists():
        return {}
    return json.loads(DATASET_METADATA_JSON.read_text(encoding="utf-8"))


def run_postgres_query(sql: str) -> int:
    with postgres_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            rows = cur.fetchall()
            return len(rows)


def explain_postgres(sql: str, path: Path) -> float | None:
    explain_sql = f"EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON) {strip_sql(sql)}"
    with postgres_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(explain_sql)
            plan = cur.fetchone()[0]
    write_json(path, plan)
    try:
        return float(plan[0].get("Execution Time"))
    except Exception:
        return None


def run_mysql_query(sql: str) -> int:
    conn = mysql_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(strip_sql(sql))
            rows = cur.fetchall()
            return len(rows)
    finally:
        conn.close()


def explain_mysql(sql: str, path: Path) -> None:
    conn = mysql_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(f"EXPLAIN ANALYZE {strip_sql(sql)}")
            rows = cur.fetchall()
    finally:
        conn.close()
    payload = "\n".join(str(row[0]) if len(row) == 1 else str(row) for row in rows)
    write_text(path, payload)


def run_mongo_query(collection, query: dict[str, Any]) -> int:
    if query["kind"] == "aggregate":
        rows = list(collection.aggregate(query["pipeline"]))
        return len(rows)
    if query["kind"] == "find":
        rows = list(
            collection.find(query["filter"], query["projection"])
            .sort(query["sort"])
            .limit(query["limit"])
        )
        return len(rows)
    raise ValueError(f"Unsupported MongoDB query kind: {query['kind']}")


def explain_mongo(db, collection_name: str, query: dict[str, Any], path: Path) -> int | None:
    if query["kind"] == "aggregate":
        command = {
            "aggregate": collection_name,
            "pipeline": query["pipeline"],
            "cursor": {},
        }
    elif query["kind"] == "find":
        command = {
            "find": collection_name,
            "filter": query["filter"],
            "projection": query["projection"],
            "sort": dict(query["sort"]),
            "limit": query["limit"],
        }
    else:
        raise ValueError(f"Unsupported MongoDB query kind: {query['kind']}")

    plan = db.command("explain", command, verbosity="executionStats")
    write_json(path, plan)
    return plan.get("executionStats", {}).get("executionTimeMillis")


def time_function(fn) -> tuple[float, int]:
    start = time.perf_counter()
    row_count = fn()
    elapsed_ms = (time.perf_counter() - start) * 1000
    return elapsed_ms, row_count


def make_record(
    dbms: str,
    index_config: str,
    query_id: str,
    query_name: str,
    run_no: int,
    elapsed_ms: float,
    rows_returned: int,
    explain_execution_ms: float | int | None,
) -> dict[str, Any]:
    return {
        "dbms": dbms,
        "index_mode": index_config,
        "index_label": INDEX_CONFIG_LABELS.get(index_config, index_config),
        "query_id": query_id,
        "query_name": query_name,
        "run_no": run_no,
        "elapsed_ms": round(elapsed_ms, 3),
        "rows_returned": rows_returned,
        "explain_execution_ms": explain_execution_ms,
    }


def run_dbms_mode(dbms: str, index_config: str, warmups: int, measured: int) -> list[dict[str, Any]]:
    print(f"\n=== {dbms.upper()} / {index_config} ===")
    apply_index_config(index_config, dbms=dbms)

    records: list[dict[str, Any]] = []

    if dbms == "postgres":
        for qid, query in POSTGRES_QUERIES.items():
            sql = query["sql"]
            explain_ms = explain_postgres(sql, EXPLAIN_DIR / "postgres" / f"{index_config}_{qid}.json")
            for _ in range(warmups):
                run_postgres_query(sql)
            for run_no in range(1, measured + 1):
                elapsed_ms, row_count = time_function(lambda: run_postgres_query(sql))
                records.append(make_record(dbms, index_config, qid, query["name"], run_no, elapsed_ms, row_count, explain_ms))
                print(f"{qid} run {run_no}/{measured}: {elapsed_ms:.2f} ms")

    elif dbms == "mysql":
        for qid, query in MYSQL_QUERIES.items():
            sql = query["sql"]
            explain_mysql(sql, EXPLAIN_DIR / "mysql" / f"{index_config}_{qid}.txt")
            for _ in range(warmups):
                run_mysql_query(sql)
            for run_no in range(1, measured + 1):
                elapsed_ms, row_count = time_function(lambda: run_mysql_query(sql))
                records.append(make_record(dbms, index_config, qid, query["name"], run_no, elapsed_ms, row_count, None))
                print(f"{qid} run {run_no}/{measured}: {elapsed_ms:.2f} ms")

    elif dbms == "mongo":
        client = mongo_client()
        db = client[MONGO["database"]]
        collection = db[MONGO["collection"]]
        try:
            for qid, query in MONGO_QUERIES.items():
                explain_ms = explain_mongo(db, MONGO["collection"], query, EXPLAIN_DIR / "mongo" / f"{index_config}_{qid}.json")
                for _ in range(warmups):
                    run_mongo_query(collection, query)
                for run_no in range(1, measured + 1):
                    elapsed_ms, row_count = time_function(lambda q=query: run_mongo_query(collection, q))
                    records.append(make_record(dbms, index_config, qid, query["name"], run_no, elapsed_ms, row_count, explain_ms))
                    print(f"{qid} run {run_no}/{measured}: {elapsed_ms:.2f} ms")
        finally:
            client.close()
    else:
        raise ValueError(f"Unsupported DBMS: {dbms}")

    return records


def write_results(records: list[dict[str, Any]]) -> None:
    output = RESULTS_DIR / "benchmark_results.csv"
    fieldnames = [
        "dbms",
        "index_mode",
        "index_label",
        "query_id",
        "query_name",
        "run_no",
        "elapsed_ms",
        "rows_returned",
        "explain_execution_ms",
    ]
    with output.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)
    print(f"\nSaved raw benchmark results: {output}")


def percentile(values: list[float], p: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]
    rank = (len(ordered) - 1) * p
    lower = int(rank)
    upper = min(lower + 1, len(ordered) - 1)
    weight = rank - lower
    return ordered[lower] * (1 - weight) + ordered[upper] * weight


def write_summary(records: list[dict[str, Any]]) -> None:
    grouped: dict[tuple[str, str, str, str], list[float]] = {}
    names: dict[str, str] = {}
    for rec in records:
        key = (rec["dbms"], rec["index_mode"], rec["query_id"], rec["query_name"])
        grouped.setdefault(key, []).append(float(rec["elapsed_ms"]))
        names[rec["query_id"]] = rec["query_name"]

    lines = [
        "# Benchmark summary",
        "",
        "Summary statistics are calculated from measured runs only.",
        "",
        "| DBMS | Index config | Query | Median, ms | Mean, ms | Min, ms | Max, ms | Std, ms | p95, ms | p99, ms |",
        "|---|---|---|---:|---:|---:|---:|---:|---:|---:|",
    ]

    medians: dict[tuple[str, str, str], float] = {}
    for (dbms, mode, qid, qname), values in sorted(grouped.items()):
        median_ms = statistics.median(values)
        mean_ms = statistics.mean(values)
        std_ms = statistics.pstdev(values) if len(values) > 1 else 0.0
        p95_ms = percentile(values, 0.95)
        p99_ms = percentile(values, 0.99)
        medians[(dbms, mode, qid)] = median_ms
        lines.append(
            f"| {dbms} | {mode} | {qid}: {qname} | {median_ms:.3f} | {mean_ms:.3f} | {min(values):.3f} | {max(values):.3f} | {std_ms:.3f} | {p95_ms:.3f} | {p99_ms:.3f} |"
        )

    lines.extend([
        "",
        "## Relative effect versus no_indexes",
        "",
        "The ratio is calculated as median(no_indexes) / median(selected_config). Values above 1 indicate acceleration.",
        "",
        "| DBMS | Index config | Query | Relative effect |",
        "|---|---|---|---:|",
    ])

    for dbms in sorted({rec["dbms"] for rec in records}):
        for mode in INDEX_CONFIGS:
            if mode == "no_indexes":
                continue
            for qid in sorted({rec["query_id"] for rec in records}):
                baseline = medians.get((dbms, "no_indexes", qid))
                current = medians.get((dbms, mode, qid))
                if baseline is not None and current and current > 0:
                    lines.append(f"| {dbms} | {mode} | {qid}: {names[qid]} | {baseline / current:.2f}x |")

    summary_path = RESULTS_DIR / "benchmark_summary.md"
    write_text(summary_path, "\n".join(lines) + "\n")
    print(f"Saved summary: {summary_path}")


def write_metadata(warmups: int, runs: int, selected_dbms: list[str], rows: int, selected_configs: list[str]) -> None:
    dataset_metadata = load_dataset_metadata()
    metadata = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "rows": rows,
        "dataset": dataset_metadata,
        "warmup_runs": warmups,
        "measured_runs": runs,
        "dbms": selected_dbms,
        "docker_resource_limits_per_dbms": {
            "cpus": "2.0",
            "mem_limit": "3g",
        },
        "query_constants": QUERY_CONSTANTS,
        "index_modes": selected_configs,
        "notes": [
            "All measured runs are stored in the raw CSV file.",
            "No-index mode keeps only technical primary key or MongoDB _id index.",
            "Each index configuration is applied independently before the benchmark series.",
            "PostgreSQL parallel query and JIT are disabled in docker-compose.yml to reduce variance.",
        ],
    }
    write_json(RESULTS_DIR / "experiment_metadata.json", metadata)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run index performance benchmarks.")
    parser.add_argument("--warmups", type=int, default=WARMUP_RUNS)
    parser.add_argument("--runs", type=int, default=MEASURED_RUNS)
    parser.add_argument("--rows", type=int, default=ROWS)
    parser.add_argument(
        "--dbms",
        nargs="+",
        choices=["all", "postgres", "mysql", "mongo"],
        default=["all"],
    )
    parser.add_argument(
        "--index-configs",
        nargs="+",
        choices=["all", *INDEX_CONFIGS],
        default=["all"],
    )
    args = parser.parse_args()

    ensure_dirs()
    selected_dbms = DBMS_LIST if "all" in args.dbms else args.dbms
    selected_configs = INDEX_CONFIGS if "all" in args.index_configs else args.index_configs

    all_records: list[dict[str, Any]] = []
    for dbms in selected_dbms:
        for index_config in selected_configs:
            all_records.extend(run_dbms_mode(dbms, index_config, args.warmups, args.runs))

    write_results(all_records)
    write_summary(all_records)
    write_metadata(args.warmups, args.runs, selected_dbms, args.rows, selected_configs)


if __name__ == "__main__":
    main()
