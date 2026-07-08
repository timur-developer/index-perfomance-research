import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd

from config import CHARTS_DIR, RESULTS_DIR
from io_utils import ensure_dirs

DBMS_ORDER = ["postgres", "mysql", "mongo"]
DBMS_LABELS = {
    "postgres": "PostgreSQL",
    "mysql": "MySQL",
    "mongo": "MongoDB",
}
QUERY_ORDER = ["Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7"]
INDEX_ORDER = [
    "no_indexes",
    "idx_student_id_only",
    "idx_created_at_only",
    "idx_status_only",
    "idx_status_created_at_only",
    "idx_course_score_only",
    "all_indexes",
]
INDEX_LABELS_RU = {
    "no_indexes": "Без индексов",
    "idx_student_id_only": "student_id",
    "idx_created_at_only": "created_at",
    "idx_status_only": "status",
    "idx_status_created_at_only": "status+date",
    "idx_course_score_only": "course+score",
    "all_indexes": "Все индексы",
}
QUERY_EXPLANATIONS = [
    ("Q1", "Поиск по student_id"),
    ("Q2", "Фильтрация по created_at"),
    ("Q3", "Фильтрация по status"),
    ("Q4", "Фильтрация по status + created_at"),
    ("Q5", "Сортировка по created_at DESC"),
    ("Q6", "Агрегация по course_id"),
    ("Q7", "Широкий диапазон score"),
]

LOAD_PERFORMANCE_CSV = RESULTS_DIR / "load_performance.csv"
BENCHMARK_MEDIANS_CSV = RESULTS_DIR / "benchmark_medians.csv"
Q1_RUN_TIMES_CSV = RESULTS_DIR / "q1_student_id_run_times_all_dbms.csv"
BENCHMARK_RESULTS_CSV = RESULTS_DIR / "benchmark_results.csv"


def configure_fonts() -> None:
    plt.rcParams["font.family"] = "DejaVu Sans"
    plt.rcParams["axes.unicode_minus"] = False


def annotate_bars(ax, bars, offset_ratio: float = 0.015) -> None:
    top = ax.get_ylim()[1]
    for bar in bars:
        height = float(bar.get_height())
        x = bar.get_x() + bar.get_width() / 2
        ax.text(
            x,
            height + top * offset_ratio,
            f"{height:.2f}",
            ha="center",
            va="bottom",
            fontsize=18,
        )


def build_load_time_comparison(load_performance_csv: Path) -> bool:
    if not load_performance_csv.exists():
        print(f"Skipped load_time_comparison.png: source file not found: {load_performance_csv}")
        return False

    df = pd.read_csv(load_performance_csv)
    required = {"dbms", "index_mode", "elapsed_ms"}
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"В {load_performance_csv} отсутствуют колонки: {', '.join(sorted(missing))}")

    pivot = df.pivot_table(index="dbms", columns="index_mode", values="elapsed_ms", aggfunc="first")
    pivot = pivot.reindex(DBMS_ORDER)
    labels = [DBMS_LABELS[dbms] for dbms in pivot.index]
    x = list(range(len(labels)))
    width = 0.34

    configure_fonts()
    plt.rcParams["axes.titlesize"] = 28
    plt.rcParams["axes.labelsize"] = 22
    plt.rcParams["xtick.labelsize"] = 18
    plt.rcParams["ytick.labelsize"] = 18
    plt.rcParams["legend.fontsize"] = 18

    fig, ax = plt.subplots(figsize=(13.0, 8.0))
    bars_no = ax.bar([value - width / 2 for value in x], pivot["no_indexes"], width=width, label="No indexes")
    bars_all = ax.bar([value + width / 2 for value in x], pivot["all_indexes"], width=width, label="All indexes")

    ax.set_title("Data load time with and without indexes", pad=20)
    ax.set_ylabel("Load time, ms", labelpad=14)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.tick_params(axis="x", pad=8)
    ax.grid(axis="y", alpha=0.22)
    ax.legend(loc="upper right", frameon=False, fontsize=19)
    ax.set_axisbelow(True)

    annotate_bars(ax, bars_no)
    annotate_bars(ax, bars_all)

    fig.tight_layout()
    fig.savefig(CHARTS_DIR / "load_time_comparison.png", dpi=220, bbox_inches="tight")
    plt.close(fig)
    return True


def load_median_pivot(benchmark_medians_csv: Path, dbms: str) -> pd.DataFrame:
    if not benchmark_medians_csv.exists():
        raise FileNotFoundError(f"Не найден файл: {benchmark_medians_csv}")

    df = pd.read_csv(benchmark_medians_csv)
    subset = df[df["dbms"] == dbms].copy()
    if subset.empty:
        raise ValueError(f"В {benchmark_medians_csv} нет данных для {dbms}")

    pivot = subset.pivot_table(index="query_id", columns="index_mode", values="median_ms", aggfunc="first")
    pivot = pivot.reindex(QUERY_ORDER).reindex(columns=INDEX_ORDER)

    if pivot.isna().any().any():
        raise ValueError(f"Для {dbms} не хватает значений median_ms по всем комбинациям query/index")

    return pivot


def generate_main_chart(dbms: str, pivot: pd.DataFrame) -> None:
    positive_values = pivot.to_numpy(dtype=float)
    positive_values = positive_values[positive_values > 0]
    if not len(positive_values):
        raise ValueError(f"Для {dbms} нет положительных значений median_ms")

    min_positive = float(positive_values.min())
    max_positive = float(positive_values.max())

    configure_fonts()
    plt.rcParams["axes.titlesize"] = 24
    plt.rcParams["axes.labelsize"] = 20
    plt.rcParams["xtick.labelsize"] = 17
    plt.rcParams["ytick.labelsize"] = 17
    plt.rcParams["legend.fontsize"] = 16

    fig, ax = plt.subplots(figsize=(15, 9))
    x = list(range(len(QUERY_ORDER)))
    width = 0.11

    for idx, index_mode in enumerate(INDEX_ORDER):
        shift = (idx - (len(INDEX_ORDER) - 1) / 2) * width
        ax.bar(
            [value + shift for value in x],
            pivot[index_mode],
            width=width,
            label=INDEX_LABELS_RU[index_mode],
            alpha=0.95,
            linewidth=0.6,
            edgecolor="white",
        )

    ax.set_title(f"{DBMS_LABELS[dbms]}: медианное время выполнения запросов", pad=16)
    ax.set_xlabel("Запрос", labelpad=10)
    ax.set_ylabel("Медианное время, мс", labelpad=10)
    ax.set_xticks(x)
    ax.set_xticklabels(QUERY_ORDER)
    ax.tick_params(axis="x", pad=6)
    ax.tick_params(axis="y", pad=6)
    ax.set_yscale("log")
    ax.set_ylim(min_positive / 1.5, max_positive * 1.35)
    ax.text(
        0.99,
        0.97,
        "Логарифмическая шкала",
        transform=ax.transAxes,
        ha="right",
        va="top",
        fontsize=16,
        bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.9, "pad": 1.8},
    )
    ax.grid(axis="y", alpha=0.18, which="both", linewidth=0.9)
    ax.set_axisbelow(True)
    ax.legend(
        loc="upper center",
        bbox_to_anchor=(0.5, -0.12),
        ncol=4,
        frameon=True,
        columnspacing=1.0,
        handletextpad=0.6,
        borderpad=0.55,
    )

    fig.subplots_adjust(left=0.1, right=0.985, top=0.88, bottom=0.24)
    fig.savefig(CHARTS_DIR / f"{dbms}_median.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def generate_query_explanations() -> None:
    configure_fonts()
    fig, ax = plt.subplots(figsize=(15, 3.2))
    fig.patch.set_facecolor("white")
    ax.axis("off")

    fig.text(
        0.5,
        0.84,
        "Пояснения к запросам Q1–Q7",
        ha="center",
        va="center",
        fontsize=18,
        fontweight="bold",
    )

    left_items = QUERY_EXPLANATIONS[:3]
    right_items = QUERY_EXPLANATIONS[3:]

    left_x = 0.08
    right_x = 0.54
    start_y = 0.62
    line_step = 0.17

    for idx, (query_id, description) in enumerate(left_items):
        fig.text(
            left_x,
            start_y - idx * line_step,
            f"{query_id} — {description}",
            ha="left",
            va="center",
            fontsize=17,
        )

    for idx, (query_id, description) in enumerate(right_items):
        fig.text(
            right_x,
            start_y - idx * line_step,
            f"{query_id} — {description}",
            ha="left",
            va="center",
            fontsize=17,
        )

    fig.savefig(CHARTS_DIR / "median_explanations.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def build_median_outputs(benchmark_medians_csv: Path) -> None:
    for dbms in DBMS_ORDER:
        pivot = load_median_pivot(benchmark_medians_csv, dbms)
        generate_main_chart(dbms, pivot)
    generate_query_explanations()


def load_q1_run_times_dataframe() -> pd.DataFrame:
    if Q1_RUN_TIMES_CSV.exists():
        df = pd.read_csv(Q1_RUN_TIMES_CSV)
        required = {"dbms_code", "СУБД", "run_no", "elapsed_ms"}
        missing = required.difference(df.columns)
        if missing:
            raise ValueError(f"В {Q1_RUN_TIMES_CSV} отсутствуют колонки: {', '.join(sorted(missing))}")
        df["dbms_code"] = pd.Categorical(df["dbms_code"], categories=DBMS_ORDER, ordered=True)
        return df.sort_values(["dbms_code", "run_no"]).reset_index(drop=True)

    if not BENCHMARK_RESULTS_CSV.exists():
        raise FileNotFoundError(
            "Не найдены q1_student_id_run_times_all_dbms.csv и benchmark_results.csv для построения q1_student_id_run_times_all_dbms.png"
        )

    raw_df = pd.read_csv(BENCHMARK_RESULTS_CSV)
    required = {"dbms", "index_mode", "query_id", "run_no", "elapsed_ms"}
    missing = required.difference(raw_df.columns)
    if missing:
        raise ValueError(f"В {BENCHMARK_RESULTS_CSV} отсутствуют колонки: {', '.join(sorted(missing))}")

    filtered = raw_df[
        (raw_df["query_id"] == "Q1")
        & (raw_df["index_mode"] == "idx_student_id_only")
    ].copy()
    filtered["dbms"] = pd.Categorical(filtered["dbms"], categories=DBMS_ORDER, ordered=True)
    filtered["dbms_label_ru"] = filtered["dbms"].astype(str).map(DBMS_LABELS)
    filtered = filtered.sort_values(["dbms", "run_no"]).reset_index(drop=True)
    return filtered.rename(columns={"dbms": "dbms_code", "dbms_label_ru": "СУБД"})[
        ["dbms_code", "СУБД", "run_no", "elapsed_ms"]
    ]


def build_q1_run_times_all_dbms() -> None:
    plot_df = load_q1_run_times_dataframe()

    configure_fonts()
    plt.rcParams["axes.titlesize"] = 34
    plt.rcParams["axes.labelsize"] = 28
    plt.rcParams["xtick.labelsize"] = 24
    plt.rcParams["ytick.labelsize"] = 24
    plt.rcParams["legend.fontsize"] = 22

    fig, ax = plt.subplots(figsize=(15.2, 9.8))

    for dbms in DBMS_ORDER:
        subset = plot_df[plot_df["dbms_code"] == dbms].copy()
        if subset.empty:
            continue
        ax.plot(
            subset["run_no"],
            subset["elapsed_ms"],
            linewidth=3.2,
            alpha=0.95,
            label=DBMS_LABELS[dbms],
        )

    ax.set_title("Время выполнения каждого запуска Q1 с индексом student_id", pad=22)
    ax.set_xlabel("Номер запуска", labelpad=16)
    ax.set_ylabel("Время выполнения, мс", labelpad=16)
    ax.tick_params(axis="x", pad=8)
    ax.tick_params(axis="y", pad=8)
    ax.grid(alpha=0.22, linewidth=1.0)
    ax.legend(title="СУБД", title_fontsize=22, fontsize=22, loc="upper right", frameon=True)
    ax.set_axisbelow(True)

    fig.subplots_adjust(left=0.11, right=0.975, top=0.88, bottom=0.14)
    fig.savefig(CHARTS_DIR / "q1_student_id_run_times_all_dbms.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build report-oriented charts from local results CSV files.")
    parser.parse_args()

    ensure_dirs()
    build_median_outputs(BENCHMARK_MEDIANS_CSV)
    build_q1_run_times_all_dbms()
    build_load_time_comparison(LOAD_PERFORMANCE_CSV)

    print(f"Report charts saved to: {CHARTS_DIR}")


if __name__ == "__main__":
    main()
