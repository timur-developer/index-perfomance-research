from db_connections import postgres_conn, mysql_conn, mongo_client
from config import SQL_DIR, MONGO
from io_utils import ensure_dirs


def run_postgres_schema() -> None:
    sql = (SQL_DIR / "postgres_schema.sql").read_text(encoding="utf-8")
    with postgres_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
        conn.commit()
    print("PostgreSQL schema created.")


def run_mysql_schema() -> None:
    sql = (SQL_DIR / "mysql_schema.sql").read_text(encoding="utf-8")
    statements = [stmt.strip() for stmt in sql.split(";") if stmt.strip()]
    conn = mysql_conn()
    try:
        with conn.cursor() as cur:
            for stmt in statements:
                cur.execute(stmt)
        conn.commit()
    finally:
        conn.close()
    print("MySQL schema created.")


def prepare_mongo_collection() -> None:
    client = mongo_client()
    db = client[MONGO["database"]]
    db[MONGO["collection"]].drop()
    db.create_collection(MONGO["collection"])
    client.close()
    print("MongoDB collection recreated.")


def main() -> None:
    ensure_dirs()
    run_postgres_schema()
    run_mysql_schema()
    prepare_mongo_collection()


if __name__ == "__main__":
    main()
