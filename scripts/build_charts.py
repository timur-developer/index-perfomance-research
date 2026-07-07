import argparse

import matplotlib.pyplot as plt
import pandas as pd

from config import CHARTS_DIR, INDEX_CONFIG_ORDER, RESULTS_DIR
from io_utils import ensure_dirs

QUERY_ORDER = ["Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7"]
DBMS_ORDER = ["postgres", "mysql", "mongo"]
INDEX_LABEL_SHORT = {
    "no_indexes": "Без индексов",
    "idx_student_id_only": "student_id",
    "idx_created_at_only": "created_at",
    "idx_status_only": "status",
    "idx_status_created_at_only": "status+date",
    "idx_course_score_only": "course+score",
    "all_indexes": "Все индексы",
}


def build_stats(df: pd.DataFrame) -> pd.DataFrame:
    stats = df.groupby(["dbms", "index_mode", "index_label", "query_id", "query_name"], as_index=False).agg(
        median_ms=("elapsed_ms", "median"),
        mean_ms=("elapsed_ms", "mean"),
        min_ms=("elapsed_ms", "min"),
        max_ms=("elapsed_ms", "max"),
        std_ms=("elapsed_ms", "std"),
    )
    percentiles = (
        df.groupby(["dbms", "index_mode", "index_label", "query_id", "query_name"])["elapsed_ms"]
        .quantile([0.95, 0.99])
        .unstack()
        .reset_index()
        .rename(columns={0.95: "p95", 0.99: "p99"})
    )
    stats = stats.merge(percentiles, on=["dbms", "index_mode", "index_label", "query_id", "query_name"], how="left")
    stats["std_ms"] = stats["std_ms"].fillna(0.0)
    return stats


def build_effectiveness_table(stats: pd.DataFrame) -> pd.DataFrame:
    baseline = (
        stats[stats["index_mode"] == "no_indexes"][["dbms", "query_id", "median_ms"]]
        .rename(columns={"median_ms": "baseline_median_ms"})
    )
    comparison = stats.merge(baseline, on=["dbms", "query_id"], how="left")
    comparison = comparison[comparison["index_mode"] != "no_indexes"].copy()
    comparison["relative_effect"] = comparison["baseline_median_ms"] / comparison["median_ms"]
    return comparison.sort_values(["dbms", "query_id", "index_mode"])


def plot_boxplots(df: pd.DataFrame) -> None:
    plt.rcParams["font.family"] = "DejaVu Sans"
    for dbms in DBMS_ORDER:
        subset = df[df["dbms"] == dbms]
        fig, axes = plt.subplots(nrows=4, ncols=2, figsize=(14, 14))
        axes = axes.flatten()
        for idx, query_id in enumerate(QUERY_ORDER):
            ax = axes[idx]
            query_df = subset[subset["query_id"] == query_id]
            data = []
            labels = []
            for mode in INDEX_CONFIG_ORDER:
                values = query_df[query_df["index_mode"] == mode]["elapsed_ms"].tolist()
                if values:
                    data.append(values)
                    labels.append(INDEX_LABEL_SHORT[mode])
            if data:
                ax.boxplot(data, tick_labels=labels, showfliers=False)
            ax.set_title(query_id)
            ax.tick_params(axis="x", rotation=45)
            ax.set_ylabel("ms")
        axes[-1].axis("off")
        fig.suptitle(f"{dbms}: query time distributions by index configuration")
        fig.tight_layout()
        fig.savefig(CHARTS_DIR / f"{dbms}_boxplots.png", dpi=180)
        plt.close(fig)


def plot_run_trends(df: pd.DataFrame) -> None:
    plt.rcParams["font.family"] = "DejaVu Sans"
    for dbms in DBMS_ORDER:
        subset = df[df["dbms"] == dbms]
        fig, axes = plt.subplots(nrows=4, ncols=2, figsize=(14, 14))
        axes = axes.flatten()
        for idx, query_id in enumerate(QUERY_ORDER):
            ax = axes[idx]
            query_df = subset[subset["query_id"] == query_id]
            for mode in INDEX_CONFIG_ORDER:
                mode_df = query_df[query_df["index_mode"] == mode]
                if mode_df.empty:
                    continue
                ax.plot(
                    mode_df["run_no"],
                    mode_df["elapsed_ms"],
                    linewidth=1,
                    alpha=0.8,
                    label=INDEX_LABEL_SHORT[mode],
                )
            ax.set_title(query_id)
            ax.set_xlabel("run")
            ax.set_ylabel("ms")
        handles, labels = axes[0].get_legend_handles_labels()
        if handles:
            fig.legend(handles, labels, loc="upper center", ncol=3)
        axes[-1].axis("off")
        fig.suptitle(f"{dbms}: measured run timeline by index configuration")
        fig.tight_layout(rect=(0, 0, 1, 0.96))
        fig.savefig(CHARTS_DIR / f"{dbms}_run_trends.png", dpi=180)
        plt.close(fig)


def plot_effectiveness_heatmaps(effectiveness: pd.DataFrame) -> None:
    plt.rcParams["font.family"] = "DejaVu Sans"
    for dbms in DBMS_ORDER:
        subset = effectiveness[effectiveness["dbms"] == dbms].copy()
        if subset.empty:
            continue
        pivot = subset.pivot_table(index="index_mode", columns="query_id", values="relative_effect", aggfunc="first")
        pivot = pivot.reindex(INDEX_CONFIG_ORDER[1:]).reindex(columns=QUERY_ORDER)
        fig, ax = plt.subplots(figsize=(10, 5))
        image = ax.imshow(pivot.values, aspect="auto", cmap="RdYlGn")
        ax.set_xticks(range(len(pivot.columns)))
        ax.set_xticklabels(list(pivot.columns))
        ax.set_yticks(range(len(pivot.index)))
        ax.set_yticklabels([INDEX_LABEL_SHORT[index_mode] for index_mode in pivot.index])
        ax.set_title(f"{dbms}: relative effect vs no_indexes")
        fig.colorbar(image, ax=ax, label="baseline / selected config")
        fig.tight_layout()
        fig.savefig(CHARTS_DIR / f"{dbms}_relative_effect.png", dpi=180)
        plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build benchmark charts and derived tables.")
    parser.parse_args()

    ensure_dirs()
    results_path = RESULTS_DIR / "benchmark_results.csv"
    if not results_path.exists():
        raise FileNotFoundError("benchmark_results.csv not found. Run scripts/benchmark.py first.")

    df = pd.read_csv(results_path)
    stats = build_stats(df)
    stats.to_csv(RESULTS_DIR / "benchmark_stats.csv", index=False)
    stats[["dbms", "index_mode", "index_label", "query_id", "query_name", "median_ms"]].to_csv(
        RESULTS_DIR / "benchmark_medians.csv",
        index=False,
    )

    effectiveness = build_effectiveness_table(stats)
    effectiveness.to_csv(RESULTS_DIR / "index_effectiveness.csv", index=False)

    plot_boxplots(df)
    plot_run_trends(df)
    plot_effectiveness_heatmaps(effectiveness)

    print(f"Charts saved to: {CHARTS_DIR}")
    print(f"Derived tables saved to: {RESULTS_DIR}")


if __name__ == "__main__":
    main()
