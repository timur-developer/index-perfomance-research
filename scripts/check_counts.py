from config import MONGO
from db_connections import postgres_conn, mysql_conn, mongo_client


def main() -> None:
    with postgres_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM student_activity;")
            print("PostgreSQL rows:", cur.fetchone()[0])

    conn = mysql_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM student_activity;")
            print("MySQL rows:", cur.fetchone()[0])
    finally:
        conn.close()

    client = mongo_client()
    try:
        collection = client[MONGO["database"]][MONGO["collection"]]
        print("MongoDB documents:", collection.count_documents({}))
    finally:
        client.close()


if __name__ == "__main__":
    main()
