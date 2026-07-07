import argparse
import csv
import time

from config import RESULTS_DIR
from create_schema import prepare_mongo_collection, run_mysql_schema, run_postgres_schema
from io_utils import ensure_dirs
from load_data import load_mongo, load_mysql, load_postgres
from manage_indexes import apply_index_config, drop_mongo_indexes, drop_mysql_indexes, drop_postgres_indexes

DBMS_LIST = ["postgres", "mysql", "mongo"]
LOAD_CONFIGS = ["no_indexes", "all_indexes"]


def reset_schema(dbms: str) -> None:
    if dbms == "postgres":
        run_postgres_schema()
        drop_postgres_indexes()
    elif dbms == "mysql":
        run_mysql_schema()
        drop_mysql_indexes()
    elif dbms == "mongo":
        prepare_mongo_collection()
        drop_mongo_indexes()
    else:
        raise ValueError(f"Unsupported DBMS: {dbms}")


def load_for_dbms(dbms: str) -> None:
    if dbms == "postgres":
        load_postgres()
    elif dbms == "mysql":
        load_mysql()
    elif dbms == "mongo":
        load_mongo()
    else:
        raise ValueError(f"Unsupported DBMS: {dbms}")


def measure_load(dbms: str, index_config: str) -> dict[str, float | str]:
    print(f"\n=== {dbms.upper()} / {index_config} load ===")
    reset_schema(dbms)
    apply_index_config(index_config, dbms)
    start = time.perf_counter()
    load_for_dbms(dbms)
    elapsed_ms = (time.perf_counter() - start) * 1000
    print(f"Load time: {elapsed_ms:.2f} ms")
    return {
        "dbms": dbms,
        "index_mode": index_config,
        "elapsed_ms": round(elapsed_ms, 3),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Measure data load time with and without indexes.")
    parser.add_argument(
        "--dbms",
        nargs="+",
        choices=["all", *DBMS_LIST],
        default=["all"],
    )
    args = parser.parse_args()

    ensure_dirs()
    selected_dbms = DBMS_LIST if "all" in args.dbms else args.dbms

    records = []
    for dbms in selected_dbms:
        for index_config in LOAD_CONFIGS:
            records.append(measure_load(dbms, index_config))

    output_path = RESULTS_DIR / "load_performance.csv"
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["dbms", "index_mode", "elapsed_ms"])
        writer.writeheader()
        writer.writerows(records)
    print(f"Saved load performance results: {output_path}")


if __name__ == "__main__":
    main()
