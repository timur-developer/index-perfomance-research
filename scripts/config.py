from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
RESULTS_DIR = PROJECT_ROOT / "results"
CHARTS_DIR = PROJECT_ROOT / "charts"
EXPLAIN_DIR = PROJECT_ROOT / "explain_plans"
SQL_DIR = PROJECT_ROOT / "sql"
DOCS_DIR = PROJECT_ROOT / "docs"

DATA_CSV = DATA_DIR / "student_activity.csv"
DATASET_METADATA_JSON = DATA_DIR / "student_activity_metadata.json"

ROWS = 1_000_000
DEFAULT_SEED = None
WARMUP_RUNS = 0
MEASURED_RUNS = 1000

POSTGRES = {
    "host": "localhost",
    "port": 5432,
    "dbname": "research_db",
    "user": "research",
    "password": "research",
}

MYSQL = {
    "host": "localhost",
    "port": 3307,
    "database": "research_db",
    "user": "research",
    "password": "research",
}

MONGO = {
    "uri": "mongodb://localhost:27017",
    "database": "research_db",
    "collection": "student_activity",
}

CSV_COLUMNS = [
    "activity_id",
    "student_id",
    "course_id",
    "faculty",
    "group_code",
    "activity_type",
    "status",
    "score",
    "created_at",
    "updated_at",
    "semester",
]

QUERY_CONSTANTS = {
    "student_id": 4242,
    "start_date": "2025-09-01 00:00:00",
    "end_date": "2025-10-01 00:00:00",
    "status": "graded",
}

INDEX_CONFIG_ORDER = [
    "no_indexes",
    "idx_student_id_only",
    "idx_created_at_only",
    "idx_status_only",
    "idx_status_created_at_only",
    "idx_course_score_only",
    "all_indexes",
]
