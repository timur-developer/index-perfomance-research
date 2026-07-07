import argparse

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd

from config import CHARTS_DIR, RESULTS_DIR
from io_utils import ensure_dirs

Q1_INDEX_CONFIGS = [
    "idx_student_id_only",
    "idx_created_at_only",
    "idx_status_only",
    "idx_status_created_at_only",
    "idx_course_score_only",
    "all_indexes",
]

INDEX_LABELS_RU = {
    "idx_student_id_only": "student_id",
    "idx_created_at_only": "created_at",
    "idx_status_only": "status",
    "idx_status_created_at_only": "status+date",
    "idx_course_score_only": "course+score",
    "all_indexes": "Все индексы",
}

DBMS_LABELS_RU = {
    "postgres": "PostgreSQL",
    "mysql": "MySQL",
    "mongo": "MongoDB",
}

OUTPUT_CSV = RESULTS_DIR / "q1_indexed_times_all_dbms.csv"
OUTPUT_PNG = CHARTS_DIR / "q1_indexed_times_all_dbms.png"
OUTPUT_LOG_PNG = CHARTS_DIR / "q1_indexed_times_all_dbms_log.png"


def load_source_dataframe() -> tuple[pd.DataFrame, str]:
    stats_path = RESULTS_DIR / "benchmark_stats.csv"
    medians_path = RESULTS_DIR / "benchmark_medians.csv"
    raw_path = RESULTS_DIR / "benchmark_results.csv"

    if stats_path.exists():
        df = pd.read_csv(stats_path)
        if "median_ms" not in df.columns:
            raise ValueError(f"В {stats_path} нет колонки median_ms")
        return df.copy(), str(stats_path)

    if medians_path.exists():
        df = pd.read_csv(medians_path)
        if "median_ms" not in df.columns:
            raise ValueError(f"В {medians_path} нет колонки median_ms")
        return df.copy(), str(medians_path)

    if raw_path.exists():
        raw_df = pd.read_csv(raw_path)
        required = {"dbms", "index_mode", "query_id", "query_name", "elapsed_ms"}
        missing = required.difference(raw_df.columns)
        if missing:
            raise ValueError(f"В {raw_path} отсутствуют колонки: {', '.join(sorted(missing))}")
        df = (
            raw_df.groupby(["dbms", "index_mode", "query_id", "query_name"], as_index=False)
            .agg(median_ms=("elapsed_ms", "median"))
        )
        return df, str(raw_path)

    raise FileNotFoundError(
        "Не найдены benchmark_stats.csv, benchmark_medians.csv или benchmark_results.csv в results/"
    )


def build_q1_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    required = {"dbms", "index_mode", "query_id", "median_ms"}
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"Во входных данных отсутствуют колонки: {', '.join(sorted(missing))}")

    filtered = df[
        (df["query_id"] == "Q1") &
        (df["index_mode"].isin(Q1_INDEX_CONFIGS))
    ].copy()

    if filtered.empty:
        raise ValueError("После фильтрации не осталось данных для Q1 с индексами")

    filtered["index_label_ru"] = filtered["index_mode"].map(INDEX_LABELS_RU)
    filtered["dbms_label_ru"] = filtered["dbms"].map(DBMS_LABELS_RU)

    filtered["index_mode"] = pd.Categorical(filtered["index_mode"], categories=Q1_INDEX_CONFIGS, ordered=True)
    filtered["dbms"] = pd.Categorical(filtered["dbms"], categories=["postgres", "mysql", "mongo"], ordered=True)
    filtered = filtered.sort_values(["index_mode", "dbms"]).reset_index(drop=True)

    output = filtered[["dbms", "dbms_label_ru", "index_mode", "index_label_ru", "median_ms"]].copy()
    output = output.rename(
        columns={
            "dbms": "dbms_code",
            "dbms_label_ru": "СУБД",
            "index_mode": "index_mode_code",
            "index_label_ru": "Конфигурация индексов",
            "median_ms": "median_ms",
        }
    )
    return output


def save_csv(plot_df: pd.DataFrame) -> None:
    plot_df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")


def build_pivot(plot_df: pd.DataFrame) -> pd.DataFrame:
    pivot = plot_df.pivot_table(
        index="Конфигурация индексов",
        columns="СУБД",
        values="median_ms",
        aggfunc="first",
    )
    pivot = pivot.reindex([INDEX_LABELS_RU[key] for key in Q1_INDEX_CONFIGS])
    pivot = pivot.reindex(columns=["PostgreSQL", "MySQL", "MongoDB"])
    return pivot


def add_bar_labels(ax, bars, use_log_scale: bool = False) -> None:
    for bar in bars:
        height = bar.get_height()
        if pd.isna(height):
            continue
        x = bar.get_x() + bar.get_width() / 2
        y = height * 1.08 if use_log_scale else height + max(height * 0.02, 1.0)
        ax.text(
            x,
            y,
            f"{height:.3f}",
            ha="center",
            va="bottom",
            fontsize=8,
            rotation=90,
        )


def build_chart(plot_df: pd.DataFrame) -> None:
    plt.rcParams["font.family"] = "DejaVu Sans"
    plt.rcParams["axes.unicode_minus"] = False

    pivot = build_pivot(plot_df)
    x = list(range(len(pivot.index)))
    width = 0.24

    fig, ax = plt.subplots(figsize=(12, 6.5))

    ax.bar([value - width for value in x], pivot["PostgreSQL"], width=width, label="PostgreSQL")
    ax.bar(x, pivot["MySQL"], width=width, label="MySQL")
    ax.bar([value + width for value in x], pivot["MongoDB"], width=width, label="MongoDB")

    ax.set_title("Время выполнения Q1 с индексами")
    ax.set_xlabel("Конфигурации индексов")
    ax.set_ylabel("Медианное время выполнения, мс")
    ax.set_xticks(x)
    ax.set_xticklabels(list(pivot.index), rotation=20)
    ax.legend(title="СУБД")
    ax.grid(axis="y", alpha=0.25)

    fig.tight_layout()
    fig.savefig(OUTPUT_PNG, dpi=220, bbox_inches="tight")
    plt.close(fig)


def build_log_chart_from_csv() -> None:
    plt.rcParams["font.family"] = "DejaVu Sans"
    plt.rcParams["axes.unicode_minus"] = False

    if not OUTPUT_CSV.exists():
        raise FileNotFoundError(f"Не найден файл с данными для графика: {OUTPUT_CSV}")

    plot_df = pd.read_csv(OUTPUT_CSV)
    pivot = build_pivot(plot_df)

    x = list(range(len(pivot.index)))
    width = 0.24

    fig, ax = plt.subplots(figsize=(12, 6.8))

    bars_pg = ax.bar([value - width for value in x], pivot["PostgreSQL"], width=width, label="PostgreSQL")
    bars_my = ax.bar(x, pivot["MySQL"], width=width, label="MySQL")
    bars_mg = ax.bar([value + width for value in x], pivot["MongoDB"], width=width, label="MongoDB")

    max_value = float(pivot.max().max())

    ax.set_yscale("log")
    ax.set_ylim(bottom=0.4, top=max_value * 2.0)
    ax.set_title("Время выполнения Q1 с индексами (логарифмическая шкала)")
    ax.set_xlabel("Конфигурации индексов")
    ax.set_ylabel("Медианное время выполнения, мс")
    ax.set_xticks(x)
    ax.set_xticklabels(list(pivot.index), rotation=20)
    ax.legend(title="СУБД")
    ax.grid(axis="y", alpha=0.25, which="both")

    add_bar_labels(ax, bars_pg, use_log_scale=True)
    add_bar_labels(ax, bars_my, use_log_scale=True)
    add_bar_labels(ax, bars_mg, use_log_scale=True)

    fig.tight_layout()
    fig.savefig(OUTPUT_LOG_PNG, dpi=220, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build dedicated Q1 indexed charts from existing benchmark CSV files."
    )
    parser.parse_args()

    ensure_dirs()

    source_df, source_path = load_source_dataframe()
    plot_df = build_q1_dataframe(source_df)
    save_csv(plot_df)
    build_chart(plot_df)
    build_log_chart_from_csv()

    print(f"PNG saved to: {OUTPUT_PNG}")
    print(f"Log PNG saved to: {OUTPUT_LOG_PNG}")
    print(f"CSV saved to: {OUTPUT_CSV}")
    print(f"Data source used: {source_path}")


if __name__ == "__main__":
    main()
