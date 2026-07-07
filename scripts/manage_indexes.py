import argparse

from pymongo import ASCENDING, DESCENDING, HASHED

from config import INDEX_CONFIG_ORDER, MONGO
from db_connections import postgres_conn, mysql_conn, mongo_client

INDEX_DEFINITIONS = {
    "postgres": {
        "idx_student_id_only": {
            "indexes": [
                (
                    "idx_pg_student_id",
                    "CREATE INDEX IF NOT EXISTS idx_pg_student_id ON student_activity(student_id)",
                ),
            ],
        },
        "idx_created_at_only": {
            "indexes": [
                (
                    "idx_pg_created_at",
                    "CREATE INDEX IF NOT EXISTS idx_pg_created_at ON student_activity(created_at)",
                ),
            ],
        },
        "idx_status_only": {
            "indexes": [
                (
                    "idx_pg_status",
                    "CREATE INDEX IF NOT EXISTS idx_pg_status ON student_activity(status)",
                ),
            ],
        },
        "idx_status_created_at_only": {
            "indexes": [
                (
                    "idx_pg_status_created_at",
                    "CREATE INDEX IF NOT EXISTS idx_pg_status_created_at ON student_activity(status, created_at DESC)",
                ),
            ],
        },
        "idx_course_score_only": {
            "indexes": [
                (
                    "idx_pg_course_score",
                    "CREATE INDEX IF NOT EXISTS idx_pg_course_score ON student_activity(course_id, score)",
                ),
            ],
        },
        "all_indexes": {
            "indexes": [
                (
                    "idx_pg_student_id",
                    "CREATE INDEX IF NOT EXISTS idx_pg_student_id ON student_activity(student_id)",
                ),
                (
                    "idx_pg_created_at",
                    "CREATE INDEX IF NOT EXISTS idx_pg_created_at ON student_activity(created_at)",
                ),
                (
                    "idx_pg_status",
                    "CREATE INDEX IF NOT EXISTS idx_pg_status ON student_activity(status)",
                ),
                (
                    "idx_pg_status_created_at",
                    "CREATE INDEX IF NOT EXISTS idx_pg_status_created_at ON student_activity(status, created_at DESC)",
                ),
                (
                    "idx_pg_course_score",
                    "CREATE INDEX IF NOT EXISTS idx_pg_course_score ON student_activity(course_id, score)",
                ),
            ],
        },
        "alternative_index_types": {
            "indexes": [
                (
                    "idx_pg_student_id_hash",
                    "CREATE INDEX IF NOT EXISTS idx_pg_student_id_hash ON student_activity USING HASH(student_id)",
                ),
                (
                    "idx_pg_created_at_brin",
                    "CREATE INDEX IF NOT EXISTS idx_pg_created_at_brin ON student_activity USING BRIN(created_at)",
                ),
                (
                    "idx_pg_status_created_at_btree",
                    "CREATE INDEX IF NOT EXISTS idx_pg_status_created_at_btree ON student_activity(status, created_at DESC)",
                ),
            ],
        },
    },
    "mysql": {
        "idx_student_id_only": {
            "indexes": [
                ("idx_mysql_student_id", "CREATE INDEX idx_mysql_student_id ON student_activity(student_id)"),
            ],
        },
        "idx_created_at_only": {
            "indexes": [
                ("idx_mysql_created_at", "CREATE INDEX idx_mysql_created_at ON student_activity(created_at)"),
            ],
        },
        "idx_status_only": {
            "indexes": [
                ("idx_mysql_status", "CREATE INDEX idx_mysql_status ON student_activity(status)"),
            ],
        },
        "idx_status_created_at_only": {
            "indexes": [
                (
                    "idx_mysql_status_created_at",
                    "CREATE INDEX idx_mysql_status_created_at ON student_activity(status, created_at DESC)",
                ),
            ],
        },
        "idx_course_score_only": {
            "indexes": [
                (
                    "idx_mysql_course_score",
                    "CREATE INDEX idx_mysql_course_score ON student_activity(course_id, score)",
                ),
            ],
        },
        "all_indexes": {
            "indexes": [
                ("idx_mysql_student_id", "CREATE INDEX idx_mysql_student_id ON student_activity(student_id)"),
                ("idx_mysql_created_at", "CREATE INDEX idx_mysql_created_at ON student_activity(created_at)"),
                ("idx_mysql_status", "CREATE INDEX idx_mysql_status ON student_activity(status)"),
                (
                    "idx_mysql_status_created_at",
                    "CREATE INDEX idx_mysql_status_created_at ON student_activity(status, created_at DESC)",
                ),
                (
                    "idx_mysql_course_score",
                    "CREATE INDEX idx_mysql_course_score ON student_activity(course_id, score)",
                ),
            ],
        },
        "alternative_index_types": {
            "indexes": [
                ("idx_mysql_student_id", "CREATE INDEX idx_mysql_student_id ON student_activity(student_id)"),
                ("idx_mysql_created_at", "CREATE INDEX idx_mysql_created_at ON student_activity(created_at)"),
                (
                    "idx_mysql_status_created_at",
                    "CREATE INDEX idx_mysql_status_created_at ON student_activity(status, created_at DESC)",
                ),
            ],
        },
    },
    "mongo": {
        "idx_student_id_only": {
            "indexes": [
                ("idx_mongo_student_id", [("student_id", ASCENDING)]),
            ],
        },
        "idx_created_at_only": {
            "indexes": [
                ("idx_mongo_created_at", [("created_at", ASCENDING)]),
            ],
        },
        "idx_status_only": {
            "indexes": [
                ("idx_mongo_status", [("status", ASCENDING)]),
            ],
        },
        "idx_status_created_at_only": {
            "indexes": [
                ("idx_mongo_status_created_at", [("status", ASCENDING), ("created_at", DESCENDING)]),
            ],
        },
        "idx_course_score_only": {
            "indexes": [
                ("idx_mongo_course_score", [("course_id", ASCENDING), ("score", ASCENDING)]),
            ],
        },
        "all_indexes": {
            "indexes": [
                ("idx_mongo_student_id", [("student_id", ASCENDING)]),
                ("idx_mongo_created_at", [("created_at", ASCENDING)]),
                ("idx_mongo_status", [("status", ASCENDING)]),
                ("idx_mongo_status_created_at", [("status", ASCENDING), ("created_at", DESCENDING)]),
                ("idx_mongo_course_score", [("course_id", ASCENDING), ("score", ASCENDING)]),
            ],
        },
        "alternative_index_types": {
            "indexes": [
                ("idx_mongo_student_id_hashed", [("student_id", HASHED)]),
                ("idx_mongo_created_at", [("created_at", ASCENDING)]),
                ("idx_mongo_status_created_at", [("status", ASCENDING), ("created_at", DESCENDING)]),
            ],
        },
    },
}

INDEX_CONFIG_LABELS = {
    "no_indexes": "No user indexes",
    "idx_student_id_only": "Only student_id index",
    "idx_created_at_only": "Only created_at index",
    "idx_status_only": "Only status index",
    "idx_status_created_at_only": "Only composite index on status + created_at",
    "idx_course_score_only": "Only composite index on course_id + score",
    "all_indexes": "All benchmark indexes",
    "alternative_index_types": "Alternative index types",
}


def supported_index_configs() -> list[str]:
    return INDEX_CONFIG_ORDER + ["alternative_index_types"]


def postgres_index_names() -> list[str]:
    names: set[str] = set()
    for config in INDEX_DEFINITIONS["postgres"].values():
        names.update(name for name, _ in config["indexes"])
    return sorted(names)


def mysql_index_names() -> list[str]:
    names: set[str] = set()
    for config in INDEX_DEFINITIONS["mysql"].values():
        names.update(name for name, _ in config["indexes"])
    return sorted(names)


def drop_postgres_indexes() -> None:
    with postgres_conn() as conn:
        with conn.cursor() as cur:
            for name in postgres_index_names():
                cur.execute(f"DROP INDEX IF EXISTS {name}")
            cur.execute("ANALYZE student_activity")
        conn.commit()
    print("PostgreSQL user indexes dropped.")


def create_postgres_indexes(index_config: str) -> None:
    drop_postgres_indexes()
    if index_config == "no_indexes":
        return
    statements = INDEX_DEFINITIONS["postgres"][index_config]["indexes"]
    with postgres_conn() as conn:
        with conn.cursor() as cur:
            for _, statement in statements:
                cur.execute(statement)
            cur.execute("ANALYZE student_activity")
        conn.commit()
    print(f"PostgreSQL index configuration applied: {index_config}")


def drop_mysql_indexes() -> None:
    conn = mysql_conn()
    try:
        with conn.cursor() as cur:
            for name in mysql_index_names():
                try:
                    cur.execute(f"DROP INDEX {name} ON student_activity")
                except Exception:
                    conn.rollback()
                    continue
            cur.execute("ANALYZE TABLE student_activity")
        conn.commit()
    finally:
        conn.close()
    print("MySQL user indexes dropped.")


def create_mysql_indexes(index_config: str) -> None:
    drop_mysql_indexes()
    if index_config == "no_indexes":
        return
    statements = INDEX_DEFINITIONS["mysql"][index_config]["indexes"]
    conn = mysql_conn()
    try:
        with conn.cursor() as cur:
            for _, statement in statements:
                cur.execute(statement)
            cur.execute("ANALYZE TABLE student_activity")
        conn.commit()
    finally:
        conn.close()
    print(f"MySQL index configuration applied: {index_config}")


def mongo_collection():
    client = mongo_client()
    return client, client[MONGO["database"]][MONGO["collection"]]


def drop_mongo_indexes() -> None:
    client, collection = mongo_collection()
    try:
        for name in list(collection.index_information().keys()):
            if name != "_id_":
                collection.drop_index(name)
    finally:
        client.close()
    print("MongoDB user indexes dropped.")


def create_mongo_indexes(index_config: str) -> None:
    drop_mongo_indexes()
    if index_config == "no_indexes":
        return
    client, collection = mongo_collection()
    try:
        for name, keys in INDEX_DEFINITIONS["mongo"][index_config]["indexes"]:
            collection.create_index(keys, name=name)
    finally:
        client.close()
    print(f"MongoDB index configuration applied: {index_config}")


def apply_index_config(index_config: str, dbms: str = "all") -> None:
    if index_config not in supported_index_configs():
        raise ValueError(f"Unsupported index configuration: {index_config}")
    if dbms in ["all", "postgres"]:
        create_postgres_indexes(index_config)
    if dbms in ["all", "mysql"]:
        create_mysql_indexes(index_config)
    if dbms in ["all", "mongo"]:
        create_mongo_indexes(index_config)


def main() -> None:
    parser = argparse.ArgumentParser(description="Apply or drop user index configurations.")
    parser.add_argument("mode", choices=["apply", "drop"], help="Index action.")
    parser.add_argument("--dbms", choices=["all", "postgres", "mysql", "mongo"], default="all")
    parser.add_argument("--config", choices=supported_index_configs(), default="all_indexes")
    args = parser.parse_args()

    if args.mode == "drop":
        if args.dbms in ["all", "postgres"]:
            drop_postgres_indexes()
        if args.dbms in ["all", "mysql"]:
            drop_mysql_indexes()
        if args.dbms in ["all", "mongo"]:
            drop_mongo_indexes()
        return

    apply_index_config(args.config, args.dbms)


if __name__ == "__main__":
    main()
