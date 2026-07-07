import argparse
import csv
import json
import random
from datetime import datetime, timedelta

from tqdm import tqdm

from config import CSV_COLUMNS, DATA_CSV, DATASET_METADATA_JSON, ROWS, DEFAULT_SEED
from io_utils import ensure_dirs

FACULTIES = ["IKNT", "FIZMEH", "GUM", "IME", "IBS", "ISE", "ICE", "IET", "ICST", "IDPO"]
ACTIVITY_TYPES = [
    "assignment_submitted",
    "test_completed",
    "exam_attempt",
    "attendance_mark",
    "project_defense",
    "course_enrollment",
]
STATUS_WEIGHTS = [
    ("graded", 0.26),
    ("submitted", 0.20),
    ("passed", 0.18),
    ("failed", 0.08),
    ("overdue", 0.10),
    ("absent", 0.10),
    ("draft", 0.08),
]
START_DATE = datetime(2024, 9, 1, 0, 0, 0)
END_DATE = datetime(2026, 6, 1, 0, 0, 0)
TOTAL_SECONDS = int((END_DATE - START_DATE).total_seconds())


def weighted_choice(rng: random.Random, weighted_values: list[tuple[str, float]]) -> str:
    values = [item[0] for item in weighted_values]
    weights = [item[1] for item in weighted_values]
    return rng.choices(values, weights=weights, k=1)[0]


def semester_for(dt: datetime) -> str:
    if 9 <= dt.month <= 12:
        return f"{dt.year}_fall"
    return f"{dt.year}_spring"


def generate_row(activity_id: int, rng: random.Random) -> dict:
    student_id = rng.randint(1, 100_000)
    course_id = rng.randint(1, 2_000)
    faculty = rng.choice(FACULTIES)
    group_year = rng.choice([2021, 2022, 2023, 2024, 2025])
    group_num = rng.randint(1, 30)
    group_code = f"{faculty}-{str(group_year)[-2:]}-{group_num:02d}"
    activity_type = rng.choice(ACTIVITY_TYPES)
    status = weighted_choice(rng, STATUS_WEIGHTS)

    # Баллы имеют неравномерное распределение, похожее на учебные данные:
    # большинство значений в среднем диапазоне, но есть низкие и высокие оценки.
    score = max(0, min(100, int(rng.gauss(72, 18))))

    created_at = START_DATE + timedelta(seconds=rng.randint(0, TOTAL_SECONDS))
    updated_at = created_at + timedelta(days=rng.randint(0, 30), seconds=rng.randint(0, 86_400))

    return {
        "activity_id": activity_id,
        "student_id": student_id,
        "course_id": course_id,
        "faculty": faculty,
        "group_code": group_code,
        "activity_type": activity_type,
        "status": status,
        "score": score,
        "created_at": created_at.strftime("%Y-%m-%d %H:%M:%S"),
        "updated_at": updated_at.strftime("%Y-%m-%d %H:%M:%S"),
        "semester": semester_for(created_at),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate student activity dataset.")
    parser.add_argument("--rows", type=int, default=ROWS, help="Number of rows to generate.")
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED, help="Optional random seed.")
    args = parser.parse_args()

    ensure_dirs()
    used_seed = args.seed if args.seed is not None else random.SystemRandom().randint(1, 2**31 - 1)
    rng = random.Random(used_seed)

    print(f"Generating {args.rows:,} rows to {DATA_CSV}")
    print(f"Seed used: {used_seed}")

    with DATA_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        for activity_id in tqdm(range(1, args.rows + 1), unit="rows"):
            writer.writerow(generate_row(activity_id, rng))

    DATASET_METADATA_JSON.write_text(
        json.dumps(
            {
                "rows": args.rows,
                "seed": used_seed,
                "seed_was_provided": args.seed is not None,
                "created_at_utc": datetime.utcnow().isoformat() + "Z",
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print("Done.")


if __name__ == "__main__":
    main()
