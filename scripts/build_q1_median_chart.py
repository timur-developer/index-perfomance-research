import argparse

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd

from config import CHARTS_DIR, RESULTS_DIR
from io_utils import ensure_dirs

SOURCE_CSV = RESULTS_DIR / "benchmark_results.csv"
OUTPUT_CSV = RESULTS_DIR / "q1_student_id_median_times_all_dbms.csv"
OUTPUT_PNG = CHARTS_DIR / "q1_student_id_median_times_all_dbms.png"
OUTPUT_LOG_PNG = CHARTS_DIR / "q1_student_id_median_times_all_dbms_log.png"

DBMS_LABELS_RU = {
    "postgres": "PostgreSQL",
    "mysql": "MySQL",
    "mongo": "MongoDB",
}

DBMS_ORDER = ["postgres", "mysql", "mongo"]


def load_raw_results() -> pd.DataFrame:
    if not SOURCE_CSV.exists():
        raise FileNotFoundError(f"Не найден исходный файл результатов: {SOURCE_CSV}")

    df = pd.read_csv(SOURCE_CSV)
    required = {"dbms", "index_mode", "query_id", "elapsed_ms"}
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"В {SOURCE_CSV} отсутствуют колонки: {', '.join(sorted(missing))}")
    return df


def build_median_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    filtered = df[
        (df["query_id"] == "Q1") &
        (df["index_mode"] == "idx_student_id_only")
    ].copy()

    if filtered.empty:
        raise ValueError("После фильтрации не осталось данных для Q1 и idx_student_id_only")

    grouped = (
        filtered.groupby("dbms", as_index=False)
        .agg(median_ms=("elapsed_ms", "median"))
    )

    grouped["dbms"] = pd.Categorical(grouped["dbms"], categories=DBMS_ORDER, ordered=True)
    grouped = grouped.sort_values("dbms").reset_index(drop=True)
    grouped["dbms_label_ru"] = grouped["dbms"].astype(str).map(DBMS_LABELS_RU)

    output = grouped[["dbms", "dbms_label_ru", "median_ms"]].copy()
    output = output.rename(
        columns={
            "dbms": "dbms_code",
            "dbms_label_ru": "СУБД",
            "median_ms": "median_ms",
        }
    )
    return output


def save_csv(plot_df: pd.DataFrame) -> None:
    plot_df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")


def add_bar_labels(ax, bars, use_log_scale: bool = False) -> None:
    for bar in bars:
        height = bar.get_height()
        if pd.isna(height):
            continue
        x = bar.get_x() + bar.get_width() / 2
        y = height * 1.06 if use_log_scale else height + max(height * 0.02, 1.0)
        ax.text(
            x,
            y,
            f"{height:.3f}",
            ha="center",
            va="bottom",
            fontsize=9,
        )


def build_chart(plot_df: pd.DataFrame) -> None:
    plt.rcParams["font.family"] = "DejaVu Sans"
    plt.rcParams["axes.unicode_minus"] = False

    x = list(range(len(plot_df)))
    labels = plot_df["СУБД"].tolist()
    values = plot_df["median_ms"].tolist()

    fig, ax = plt.subplots(figsize=(8, 5.8))
    bars = ax.bar(x, values, width=0.55)

    ax.set_title("Медианное время выполнения Q1 с индексом student_id")
    ax.set_xlabel("СУБД")
    ax.set_ylabel("Медианное время выполнения, мс")
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.grid(axis="y", alpha=0.25)

    add_bar_labels(ax, bars, use_log_scale=False)

    fig.tight_layout()
    fig.savefig(OUTPUT_PNG, dpi=220, bbox_inches="tight")
    plt.close(fig)


def build_log_chart(plot_df: pd.DataFrame) -> None:
    plt.rcParams["font.family"] = "DejaVu Sans"
    plt.rcParams["axes.unicode_minus"] = False

    x = list(range(len(plot_df)))
    labels = plot_df["СУБД"].tolist()
    values = plot_df["median_ms"].tolist()
    max_value = max(values)

    fig, ax = plt.subplots(figsize=(8, 6.0))
    bars = ax.bar(x, values, width=0.55)

    ax.set_yscale("log")
    ax.set_ylim(bottom=0.4, top=max_value * 2.0)
    ax.set_title("Медианное время выполнения Q1 с индексом student_id")
    ax.set_xlabel("СУБД")
    ax.set_ylabel("Медианное время выполнения, мс")
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.grid(axis="y", alpha=0.25, which="both")

    add_bar_labels(ax, bars, use_log_scale=True)

    fig.tight_layout()
    fig.savefig(OUTPUT_LOG_PNG, dpi=220, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build median Q1 charts for idx_student_id_only from existing benchmark_results.csv."
    )
    parser.parse_args()

    ensure_dirs()

    raw_df = load_raw_results()
    plot_df = build_median_dataframe(raw_df)
    save_csv(plot_df)
    build_chart(plot_df)
    build_log_chart(plot_df)

    print(f"Source CSV used: {SOURCE_CSV}")
    print(f"CSV saved to: {OUTPUT_CSV}")
    print(f"PNG saved to: {OUTPUT_PNG}")
    print(f"Log PNG saved to: {OUTPUT_LOG_PNG}")


if __name__ == "__main__":
    main()
