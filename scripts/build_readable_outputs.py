from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import pandas as pd

from config import CHARTS_DIR, INDEX_CONFIG_ORDER, RESULTS_DIR

ROOT = Path(__file__).resolve().parents[1]
METADATA_PATH = RESULTS_DIR / "experiment_metadata.json"
STATS_PATH = RESULTS_DIR / "benchmark_stats.csv"
EFFECTIVENESS_PATH = RESULTS_DIR / "index_effectiveness.csv"
LOAD_PERFORMANCE_PATH = RESULTS_DIR / "load_performance.csv"

SUMMARY_RU_PATH = RESULTS_DIR / "summary_ru.md"
BENCHMARK_TABLE_RU_PATH = RESULTS_DIR / "benchmark_table_ru.csv"
INDEX_EFFECTIVENESS_RU_PATH = RESULTS_DIR / "index_effectiveness_ru.csv"
LOAD_PERFORMANCE_RU_PATH = RESULTS_DIR / "load_performance_ru.csv"

DBMS_ORDER = ["postgres", "mysql", "mongo"]
QUERY_ORDER = ["Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7"]

DBMS_RU = {
    "postgres": "PostgreSQL",
    "mysql": "MySQL",
    "mongo": "MongoDB",
}

INDEX_MODE_RU = {
    "no_indexes": "Без индексов",
    "idx_student_id_only": "student_id",
    "idx_created_at_only": "created_at",
    "idx_status_only": "status",
    "idx_status_created_at_only": "status+date",
    "idx_course_score_only": "course+score",
    "all_indexes": "Все индексы",
}

QUERY_RU = {
    "Q1": "поиск по student_id",
    "Q2": "фильтрация по диапазону created_at",
    "Q3": "фильтрация по status",
    "Q4": "фильтрация по status и created_at",
    "Q5": "сортировка по created_at с LIMIT",
    "Q6": "агрегация по course_id",
    "Q7": "широкий диапазон score",
}

INDEX_JUSTIFICATION = {
    "idx_student_id_only": "Подходит для точечного поиска по идентификатору студента и высокой селективности запроса Q1.",
    "idx_created_at_only": "Нужен для диапазонной фильтрации и сортировки по времени в запросах Q2 и Q5.",
    "idx_status_only": "Проверяет полезность индекса по полю с невысокой селективностью для запроса Q3.",
    "idx_status_created_at_only": "Целевой составной индекс для комбинированного фильтра в запросе Q4.",
    "idx_course_score_only": "Показывает, помогает ли составной индекс при агрегировании и работе с курсом и оценкой.",
    "all_indexes": "Позволяет оценить суммарный эффект и понять, не возникает ли избыточность между индексами.",
}


def load_metadata() -> dict[str, Any]:
    if not METADATA_PATH.exists():
        return {}
    return json.loads(METADATA_PATH.read_text(encoding="utf-8"))


def markdown_table(headers: list[str], rows: list[list[str]]) -> str:
    lines = []
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
    for row in rows:
        lines.append("| " + " | ".join(row) + " |")
    return "\n".join(lines)


def load_required_tables() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame | None, dict[str, Any]]:
    missing = [path for path in [STATS_PATH, EFFECTIVENESS_PATH, METADATA_PATH] if not path.exists()]
    if missing:
        raise FileNotFoundError("Не найдены необходимые файлы результатов. Сначала выполните benchmark и build_charts.")
    stats = pd.read_csv(STATS_PATH)
    effectiveness = pd.read_csv(EFFECTIVENESS_PATH)
    load_perf = pd.read_csv(LOAD_PERFORMANCE_PATH) if LOAD_PERFORMANCE_PATH.exists() else None
    return stats, effectiveness, load_perf, load_metadata()


def classify_effect(value: float) -> str:
    if value > 1.1:
        return "accelerates"
    if value < 0.9:
        return "decelerates"
    return "neutral"


def unique_sorted_query_ids(series: pd.Series) -> list[str]:
    seen = {str(value) for value in series.dropna().tolist()}
    return [query_id for query_id in QUERY_ORDER if query_id in seen]


def join_query_ids(query_ids: list[str]) -> str:
    return ", ".join(query_ids) if query_ids else "нет"


def preliminary_conclusion(accelerates: list[str], neutral: list[str], decelerates: list[str]) -> str:
    if accelerates and not decelerates:
        return "целесообразен"
    if accelerates and decelerates:
        return "нужен дополнительный анализ"
    if neutral and not accelerates and not decelerates:
        return "спорный"
    if decelerates and not accelerates:
        return "спорный"
    return "нужен дополнительный анализ"


def build_russian_tables(stats: pd.DataFrame, effectiveness: pd.DataFrame, load_perf: pd.DataFrame | None) -> None:
    stats_ru = stats.copy()
    stats_ru["СУБД"] = stats_ru["dbms"].map(DBMS_RU)
    stats_ru["Конфигурация индексов"] = stats_ru["index_mode"].map(INDEX_MODE_RU)
    stats_ru["Запрос"] = stats_ru["query_id"].map(QUERY_RU)
    stats_ru = stats_ru[
        [
            "СУБД",
            "Конфигурация индексов",
            "query_id",
            "Запрос",
            "median_ms",
            "mean_ms",
            "min_ms",
            "max_ms",
            "std_ms",
            "p95",
            "p99",
        ]
    ].rename(
        columns={
            "query_id": "Код запроса",
            "median_ms": "Медиана, мс",
            "mean_ms": "Среднее, мс",
            "min_ms": "Минимум, мс",
            "max_ms": "Максимум, мс",
            "std_ms": "Стандартное отклонение, мс",
            "p95": "p95, мс",
            "p99": "p99, мс",
        }
    )
    stats_ru.to_csv(BENCHMARK_TABLE_RU_PATH, index=False, sep=";", encoding="utf-8-sig")

    eff_ru = effectiveness.copy()
    eff_ru["СУБД"] = eff_ru["dbms"].map(DBMS_RU)
    eff_ru["Конфигурация индексов"] = eff_ru["index_mode"].map(INDEX_MODE_RU)
    eff_ru["Запрос"] = eff_ru["query_id"].map(QUERY_RU)
    eff_ru["Интерпретация"] = eff_ru["relative_effect"].map(
        lambda value: "ускоряет" if value > 1.1 else ("замедляет" if value < 0.9 else "почти не влияет")
    )
    eff_ru = eff_ru[
        ["СУБД", "Конфигурация индексов", "query_id", "Запрос", "baseline_median_ms", "median_ms", "relative_effect", "Интерпретация"]
    ].rename(
        columns={
            "query_id": "Код запроса",
            "baseline_median_ms": "Базовая медиана без индексов, мс",
            "median_ms": "Медиана выбранной конфигурации, мс",
            "relative_effect": "Относительный эффект",
        }
    )
    eff_ru.to_csv(INDEX_EFFECTIVENESS_RU_PATH, index=False, sep=";", encoding="utf-8-sig")

    if load_perf is not None:
        load_ru = load_perf.copy()
        load_ru["СУБД"] = load_ru["dbms"].map(DBMS_RU)
        load_ru["Конфигурация индексов"] = load_ru["index_mode"].map(INDEX_MODE_RU)
        load_ru = load_ru[["СУБД", "Конфигурация индексов", "elapsed_ms"]].rename(columns={"elapsed_ms": "Время загрузки, мс"})
        load_ru.to_csv(LOAD_PERFORMANCE_RU_PATH, index=False, sep=";", encoding="utf-8-sig")


def build_summary(stats: pd.DataFrame, effectiveness: pd.DataFrame, load_perf: pd.DataFrame | None, metadata: dict[str, Any]) -> None:
    dataset = metadata.get("dataset", {})
    rows = metadata.get("rows", "не указано")
    seed = dataset.get("seed", "не указано")
    seed_given = dataset.get("seed_was_provided", False)
    warmups = metadata.get("warmup_runs", "не указано")
    runs = metadata.get("measured_runs", "не указано")

    best_rows = []
    for dbms in DBMS_ORDER:
        db_subset = effectiveness[effectiveness["dbms"] == dbms]
        if db_subset.empty:
            continue
        best = db_subset.sort_values("relative_effect", ascending=False).iloc[0]
        worst = db_subset.sort_values("relative_effect", ascending=True).iloc[0]
        best_rows.append([DBMS_RU[dbms], "лучший", INDEX_MODE_RU[best["index_mode"]], best["query_id"], f"{best['relative_effect']:.2f}"])
        best_rows.append([DBMS_RU[dbms], "худший", INDEX_MODE_RU[worst["index_mode"]], worst["query_id"], f"{worst['relative_effect']:.2f}"])

    index_rows = [[INDEX_MODE_RU[key], value] for key, value in INDEX_JUSTIFICATION.items()]

    necessity_rows = []
    for dbms in DBMS_ORDER:
        db_subset = effectiveness[effectiveness["dbms"] == dbms].copy()
        for mode in INDEX_CONFIG_ORDER[1:]:
            subset = db_subset[db_subset["index_mode"] == mode].copy()
            if subset.empty:
                continue
            subset["effect_class"] = subset["relative_effect"].map(classify_effect)
            accelerates = unique_sorted_query_ids(subset[subset["effect_class"] == "accelerates"]["query_id"])
            neutral = unique_sorted_query_ids(subset[subset["effect_class"] == "neutral"]["query_id"])
            decelerates = unique_sorted_query_ids(subset[subset["effect_class"] == "decelerates"]["query_id"])
            necessity_rows.append(
                [
                    DBMS_RU[dbms],
                    INDEX_MODE_RU[mode],
                    join_query_ids(accelerates),
                    join_query_ids(neutral),
                    join_query_ids(decelerates),
                    preliminary_conclusion(accelerates, neutral, decelerates),
                ]
            )

    load_rows: list[list[str]] = []
    if load_perf is not None:
        pivot = load_perf.pivot_table(index="dbms", columns="index_mode", values="elapsed_ms", aggfunc="first")
        for dbms in DBMS_ORDER:
            if dbms not in pivot.index:
                continue
            no_idx = float(pivot.loc[dbms, "no_indexes"])
            all_idx = float(pivot.loc[dbms, "all_indexes"])
            load_rows.append([DBMS_RU[dbms], f"{no_idx:.2f}", f"{all_idx:.2f}", f"{all_idx / no_idx:.2f}"])

    lines = [
        "# Краткое описание результатов эксперимента",
        "",
        "## 1. Условия и воспроизводимость",
        "",
        f"- Количество строк в наборе данных: **{rows}**.",
        f"- Seed последней генерации: **{seed}**.",
        f"- Seed был задан вручную: **{'да' if seed_given else 'нет'}**.",
        f"- Количество warm-up запусков: **{warmups}**.",
        f"- Количество измеряемых запусков: **{runs}**.",
        "- Один и тот же CSV-файл загружается в PostgreSQL, MySQL и MongoDB.",
        "- Для точного повторения конкретного набора данных можно явно передать параметр `--seed`.",
        "",
        "## 2. Почему выбраны эти индексы",
        "",
        markdown_table(["Конфигурация", "Обоснование"], index_rows),
        "",
        "## 3. Нужен ли каждый индекс",
        "",
        markdown_table(
            ["СУБД", "Конфигурация индекса", "Ускоряет", "Почти не влияет", "Замедляет", "Предварительный вывод"],
            necessity_rows,
        ),
        "",
        "## 4. Лучшие и худшие эффекты по СУБД",
        "",
        markdown_table(["СУБД", "Тип наблюдения", "Конфигурация", "Запрос", "Относительный эффект"], best_rows),
        "",
        "## 5. Накладные расходы индексов на загрузку данных",
        "",
    ]

    if load_rows:
        lines.extend([
            markdown_table(
                ["СУБД", "Без индексов, мс", "Со всеми индексами, мс", "Коэффициент замедления"],
                load_rows,
            ),
            "",
        ])
    else:
        lines.extend([
            "Файл `results/load_performance.csv` пока не сформирован. Для этого нужно выполнить `python scripts/measure_load_performance.py`.",
            "",
        ])

    lines.extend([
        "## 6. Типы индексов, которые стоит учитывать в этой задаче",
        "",
        "- PostgreSQL: базовый вариант - B-tree; для `student_id` можно отдельно проверить Hash, для `created_at` - BRIN.",
        "- MySQL: для текущих запросов основной практический вариант - обычные и составные B-tree индексы InnoDB.",
        "- MongoDB: релевантны single-field и compound индексы; hashed индекс имеет смысл рассматривать для равенства по `student_id`.",
        "",
        "## 7. Артефакты для анализа",
        "",
        "- `results/benchmark_results.csv` - все измеряемые прогоны.",
        "- `results/benchmark_stats.csv` - агрегированная статистика по каждой конфигурации.",
        "- `results/benchmark_medians.csv` - медианы по каждой группе, используемые для дополнительных Q1-выводов.",
        "- `results/index_effectiveness.csv` - сравнение каждой конфигурации с режимом без индексов.",
        "- `results/load_performance.csv` - сравнение времени загрузки данных.",
        "- `results/benchmark_summary.md` - машинно сгенерированная текстовая сводка по benchmark.",
        "- `results/benchmark_table_ru.csv`, `results/index_effectiveness_ru.csv`, `results/load_performance_ru.csv` - русскоязычные таблицы для чтения и вставки в отчет.",
        "- `charts/postgres_boxplots.png`, `charts/mysql_boxplots.png`, `charts/mongo_boxplots.png` - распределения времени.",
        "- `charts/postgres_run_trends.png`, `charts/mysql_run_trends.png`, `charts/mongo_run_trends.png` - ход измерений по номерам прогонов.",
        "- `charts/postgres_relative_effect.png`, `charts/mysql_relative_effect.png`, `charts/mongo_relative_effect.png` - влияние каждой конфигурации индексов.",
        "- `results/q1_student_id_median_times_all_dbms.csv`, `results/q1_student_id_run_times_all_dbms.csv` - дополнительные Q1-таблицы, если запускались helper-скрипты.",
        "- `charts/q1_student_id_median_times_all_dbms.png`, `charts/q1_student_id_median_times_all_dbms_log.png`, `charts/q1_student_id_run_times_with_median_subplots.png` - дополнительные Q1-графики, если запускались helper-скрипты.",
    ])

    SUMMARY_RU_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build Russian-readable benchmark summaries.")
    parser.parse_args()

    stats, effectiveness, load_perf, metadata = load_required_tables()
    build_russian_tables(stats, effectiveness, load_perf)
    build_summary(stats, effectiveness, load_perf, metadata)
    print(f"Русскоязычное описание сохранено: {SUMMARY_RU_PATH}")
    print(f"Русскоязычная таблица статистики сохранена: {BENCHMARK_TABLE_RU_PATH}")
    print(f"Русскоязычная таблица эффективности сохранена: {INDEX_EFFECTIVENESS_RU_PATH}")
    if LOAD_PERFORMANCE_RU_PATH.exists():
        print(f"Русскоязычная таблица загрузки сохранена: {LOAD_PERFORMANCE_RU_PATH}")
    print(f"Папка с графиками: {CHARTS_DIR}")


if __name__ == "__main__":
    main()
