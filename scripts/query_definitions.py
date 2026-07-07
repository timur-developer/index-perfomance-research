from datetime import datetime

from config import QUERY_CONSTANTS

STUDENT_ID = QUERY_CONSTANTS["student_id"]
START_DATE_SQL = QUERY_CONSTANTS["start_date"]
END_DATE_SQL = QUERY_CONSTANTS["end_date"]
START_DATE_MONGO = datetime.strptime(START_DATE_SQL, "%Y-%m-%d %H:%M:%S")
END_DATE_MONGO = datetime.strptime(END_DATE_SQL, "%Y-%m-%d %H:%M:%S")
STATUS = QUERY_CONSTANTS["status"]

POSTGRES_QUERIES = {
    "Q1": {
        "name": "Exact search by student_id",
        "sql": f"SELECT COUNT(*) FROM student_activity WHERE student_id = {STUDENT_ID};",
    },
    "Q2": {
        "name": "Date range filtering by created_at",
        "sql": f"""
            SELECT COUNT(*)
            FROM student_activity
            WHERE created_at >= TIMESTAMP '{START_DATE_SQL}'
              AND created_at < TIMESTAMP '{END_DATE_SQL}';
        """,
    },
    "Q3": {
        "name": "Low-selectivity filtering by status",
        "sql": f"SELECT COUNT(*) FROM student_activity WHERE status = '{STATUS}';",
    },
    "Q4": {
        "name": "Combined filtering by status and created_at",
        "sql": f"""
            SELECT COUNT(*)
            FROM student_activity
            WHERE status = '{STATUS}'
              AND created_at >= TIMESTAMP '{START_DATE_SQL}'
              AND created_at < TIMESTAMP '{END_DATE_SQL}';
        """,
    },
    "Q5": {
        "name": "Sort by created_at DESC with LIMIT",
        "sql": """
            SELECT activity_id, student_id, course_id, status, created_at
            FROM student_activity
            ORDER BY created_at DESC
            LIMIT 100;
        """,
    },
    "Q6": {
        "name": "Aggregation by course_id for graded activities",
        "sql": f"""
            SELECT course_id, COUNT(*) AS cnt, AVG(score) AS avg_score
            FROM student_activity
            WHERE status = '{STATUS}'
            GROUP BY course_id
            ORDER BY cnt DESC
            LIMIT 20;
        """,
    },
    "Q7": {
        "name": "Broad score range where indexes are expected to help little",
        "sql": "SELECT COUNT(*) FROM student_activity WHERE score BETWEEN 0 AND 100;",
    },
}

# MySQL accepts the same SQL for this experiment if timestamp literals are represented as strings.
MYSQL_QUERIES = {
    qid: {
        "name": payload["name"],
        "sql": payload["sql"].replace("TIMESTAMP '", "'")
    }
    for qid, payload in POSTGRES_QUERIES.items()
}

MONGO_QUERIES = {
    "Q1": {
        "name": "Exact search by student_id",
        "kind": "aggregate",
        "pipeline": [
            {"$match": {"student_id": STUDENT_ID}},
            {"$count": "count"},
        ],
    },
    "Q2": {
        "name": "Date range filtering by created_at",
        "kind": "aggregate",
        "pipeline": [
            {"$match": {"created_at": {"$gte": START_DATE_MONGO, "$lt": END_DATE_MONGO}}},
            {"$count": "count"},
        ],
    },
    "Q3": {
        "name": "Low-selectivity filtering by status",
        "kind": "aggregate",
        "pipeline": [
            {"$match": {"status": STATUS}},
            {"$count": "count"},
        ],
    },
    "Q4": {
        "name": "Combined filtering by status and created_at",
        "kind": "aggregate",
        "pipeline": [
            {"$match": {"status": STATUS, "created_at": {"$gte": START_DATE_MONGO, "$lt": END_DATE_MONGO}}},
            {"$count": "count"},
        ],
    },
    "Q5": {
        "name": "Sort by created_at DESC with LIMIT",
        "kind": "find",
        "filter": {},
        "projection": {"activity_id": 1, "student_id": 1, "course_id": 1, "status": 1, "created_at": 1},
        "sort": [("created_at", -1)],
        "limit": 100,
    },
    "Q6": {
        "name": "Aggregation by course_id for graded activities",
        "kind": "aggregate",
        "pipeline": [
            {"$match": {"status": STATUS}},
            {"$group": {"_id": "$course_id", "cnt": {"$sum": 1}, "avg_score": {"$avg": "$score"}}},
            {"$sort": {"cnt": -1}},
            {"$limit": 20},
        ],
    },
    "Q7": {
        "name": "Broad score range where indexes are expected to help little",
        "kind": "aggregate",
        "pipeline": [
            {"$match": {"score": {"$gte": 0, "$lte": 100}}},
            {"$count": "count"},
        ],
    },
}
