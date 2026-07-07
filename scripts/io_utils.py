import json
from pathlib import Path
from typing import Any

from config import CHARTS_DIR, DATA_DIR, DOCS_DIR, EXPLAIN_DIR, RESULTS_DIR


def ensure_dirs() -> None:
    for path in [DATA_DIR, RESULTS_DIR, CHARTS_DIR, EXPLAIN_DIR, DOCS_DIR]:
        path.mkdir(parents=True, exist_ok=True)
    for dbms in ["postgres", "mysql", "mongo"]:
        (EXPLAIN_DIR / dbms).mkdir(parents=True, exist_ok=True)


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2, default=str)


def write_text(path: Path, payload: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        f.write(payload)
