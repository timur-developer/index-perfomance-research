import argparse

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd

from config import CHARTS_DIR, RESULTS_DIR
from io_utils import ensure_dirs

SOURCE_CSV = RESULTS_DIR / "benchmark_results.csv"
OUTPUT_CSV = RESULTS_DIR / "q1_student_id_run_times_all_dbms.csv"
MEDIAN_OUTPUT_CSV = RESULTS_DIR / "q1_student_id_median_times_all_dbms.csv"
OUTPUT_PNG = CHARTS_DIR / "q1_student_id_run_times_with_median_subplots.png"

DBMS_LABELS_RU = {
    "postgres": "PostgreSQL",
    "mysql": "MySQL",
    "mongo": "MongoDB",
}

DBMS_ORDER = ["postgres", "mysql", "mongo"]
DBMS_COLORS = {
    "postgres": "#1f77b4",
    "mysql": "#ff7f0e",
    "mongo": "#2ca02c",
}


def load_raw_results() -> pd.DataFrame:
    if not SOURCE_CSV.exists():
        raise FileNotFoundError(f"Не найден исходный файл результатов: {SOURCE_CSV}")

    df = pd.read_csv(SOURCE_CSV)
    required = {"dbms", "index_mode", "query_id", "run_no", "elapsed_ms"}
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"В {SOURCE_CSV} отсутствуют колонки: {', '.join(sorted(missing))}")
    return df


def build_filtered_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    filtered = df[
        (df["query_id"] == "Q1")
        & (df["index_mode"] == "idx_student_id_only")
    ].copy()

    if filtered.empty:
        raise ValueError("После фильтрации не осталось данных для Q1 и idx_student_id_only")

    filtered["dbms"] = pd.Categorical(filtered["dbms"], categories=DBMS_ORDER, ordered=True)
    filtered["dbms_label_ru"] = filtered["dbms"].astype(str).map(DBMS_LABELS_RU)
    filtered = filtered.sort_values(["dbms", "run_no"]).reset_index(drop=True)

    output = filtered[["dbms", "dbms_label_ru", "run_no", "elapsed_ms"]].copy()
    return output.rename(columns={"dbms": "dbms_code", "dbms_label_ru": "СУБД"})


def build_median_dataframe(plot_df: pd.DataFrame) -> pd.DataFrame:
    grouped = (
        plot_df.groupby(["dbms_code", "СУБД"], as_index=False, observed=True)
        .agg(median_ms=("elapsed_ms", "median"))
    )
    grouped["dbms_code"] = pd.Categorical(grouped["dbms_code"], categories=DBMS_ORDER, ordered=True)
    return grouped.sort_values("dbms_code").reset_index(drop=True)


def save_run_times_csv(plot_df: pd.DataFrame) -> None:
    plot_df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")


def save_median_csv(median_df: pd.DataFrame) -> None:
    median_df.to_csv(MEDIAN_OUTPUT_CSV, index=False, encoding="utf-8-sig")


def build_chart(plot_df: pd.DataFrame, median_df: pd.DataFrame) -> None:
    plt.rcParams["font.family"] = "DejaVu Sans"
    plt.rcParams["axes.unicode_minus"] = False

    fig, axes = plt.subplots(
        nrows=3,
        ncols=1,
        figsize=(13, 10.5),
        sharex=True,
    )
    max_run_no = int(plot_df["run_no"].max())

    for ax, dbms_code in zip(axes, DBMS_ORDER):
        subset = plot_df[plot_df["dbms_code"] == dbms_code]
        if subset.empty:
            continue

        label = DBMS_LABELS_RU[dbms_code]
        color = DBMS_COLORS[dbms_code]
        median_value = float(
            median_df.loc[median_df["dbms_code"] == dbms_code, "median_ms"].iloc[0]
        )
        max_elapsed = float(subset["elapsed_ms"].max())

        ax.plot(
            subset["run_no"],
            subset["elapsed_ms"],
            color=color,
            linewidth=1,
            alpha=0.55,
        )
        ax.axhline(
            y=median_value,
            color=color,
            linestyle="--",
            linewidth=2,
        )
        ax.text(
            0.985,
            0.90,
            f"median = {median_value:.3f} ms",
            transform=ax.transAxes,
            ha="right",
            va="top",
            fontsize=9,
            color=color,
            bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.75, "pad": 1.5},
        )

        ax.set_title(label, loc="left", fontsize=11, fontweight="bold")
        ax.set_ylabel("Время выполнения, мс")
        ax.set_xlim(1, max_run_no)
        ax.set_ylim(0, max_elapsed * 1.05)
        ax.grid(alpha=0.25)

    axes[-1].set_xlabel("Номер запуска")
    fig.suptitle("Время выполнения Q1 по запускам с линиями медианы", fontsize=14)
    fig.tight_layout(rect=[0, 0, 1, 0.97])
    fig.savefig(OUTPUT_PNG, dpi=220, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build a Q1 run-times chart with separate DBMS subplots and median lines."
    )
    parser.parse_args()

    ensure_dirs()

    raw_df = load_raw_results()
    plot_df = build_filtered_dataframe(raw_df)
    median_df = build_median_dataframe(plot_df)

    save_run_times_csv(plot_df)
    save_median_csv(median_df)
    build_chart(plot_df, median_df)

    print(f"Source CSV used: {SOURCE_CSV}")
    print(f"Filtered rows: {len(plot_df)}")
    print(f"PNG saved to: {OUTPUT_PNG}")
    print(f"Run-times CSV saved to: {OUTPUT_CSV}")
    print(f"Median CSV saved to: {MEDIAN_OUTPUT_CSV}")


if __name__ == "__main__":
    main()
