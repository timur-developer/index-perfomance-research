import argparse
import csv
from datetime import datetime
from pathlib import Path

from tqdm import tqdm

from config import CSV_COLUMNS, DATA_CSV, MONGO
from db_connections import postgres_conn, mysql_conn, mongo_client


def ensure_csv_exists(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(f"CSV file not found: {path}. Run scripts/generate_data.py first.")


def load_postgres() -> None:
    ensure_csv_exists(DATA_CSV)
    copy_sql = f"""
        COPY student_activity ({', '.join(CSV_COLUMNS)})
        FROM STDIN WITH (FORMAT CSV, HEADER TRUE)
    """
    with postgres_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("TRUNCATE TABLE student_activity;")
            with DATA_CSV.open("r", encoding="utf-8") as f:
                cur.copy_expert(copy_sql, f)
            cur.execute("ANALYZE student_activity;")
        conn.commit()
    print("PostgreSQL data loaded.")


def load_mysql() -> None:
    ensure_csv_exists(DATA_CSV)
    csv_path = DATA_CSV.resolve().as_posix()
    columns = ", ".join(CSV_COLUMNS)
    load_sql = f"""
        LOAD DATA LOCAL INFILE '{csv_path}'
        INTO TABLE student_activity
        CHARACTER SET utf8mb4
        FIELDS TERMINATED BY ',' ENCLOSED BY '"'
        LINES TERMINATED BY '\\n'
        IGNORE 1 LINES
        ({columns})
    """
    conn = mysql_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("TRUNCATE TABLE student_activity;")
            cur.execute(load_sql)
            cur.execute("ANALYZE TABLE student_activity;")
        conn.commit()
    finally:
        conn.close()
    print("MySQL data loaded.")


def parse_mongo_doc(row: dict) -> dict:
    return {
        "_id": int(row["activity_id"]),
        "activity_id": int(row["activity_id"]),
        "student_id": int(row["student_id"]),
        "course_id": int(row["course_id"]),
        "faculty": row["faculty"],
        "group_code": row["group_code"],
        "activity_type": row["activity_type"],
        "status": row["status"],
        "score": int(row["score"]),
        "created_at": datetime.strptime(row["created_at"], "%Y-%m-%d %H:%M:%S"),
        "updated_at": datetime.strptime(row["updated_at"], "%Y-%m-%d %H:%M:%S"),
        "semester": row["semester"],
    }


def load_mongo(batch_size: int = 10_000) -> None:
    ensure_csv_exists(DATA_CSV)
    client = mongo_client()
    db = client[MONGO["database"]]
    collection = db[MONGO["collection"]]
    collection.drop()

    batch = []
    with DATA_CSV.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in tqdm(reader, desc="MongoDB insert", unit="rows"):
            batch.append(parse_mongo_doc(row))
            if len(batch) >= batch_size:
                collection.insert_many(batch, ordered=False)
                batch.clear()
        if batch:
            collection.insert_many(batch, ordered=False)

    client.close()
    print("MongoDB data loaded.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Load deterministic dataset to DBMS containers.")
    parser.add_argument(
        "--dbms",
        choices=["all", "postgres", "mysql", "mongo"],
        default="all",
        help="Target DBMS.",
    )
    args = parser.parse_args()

    if args.dbms in ["all", "postgres"]:
        load_postgres()
    if args.dbms in ["all", "mysql"]:
        load_mysql()
    if args.dbms in ["all", "mongo"]:
        load_mongo()


if __name__ == "__main__":
    main()
