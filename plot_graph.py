"""plot_graph.py

Analyze and visualize results from experiment_results.csv.

Expected columns:
  Timestamp, Player_ID, Mode_Played, Win_Loss, Catch_Duration_Sec,
  Difficulty_Score, Fun_Score, DDA_Similarity, DDA_More_Fun

Notes:
  - DDA_Similarity (1=Easy, 2=Medium, 3=Hard) and DDA_More_Fun (0-9)
    are only populated when Mode_Played == "DDA".
"""

from __future__ import annotations

import os

try:
    import pandas as pd
except ImportError as e:
    raise SystemExit(
        "Missing dependency 'pandas'. Install it with: pip install pandas"
    ) from e

try:
    import matplotlib.pyplot as plt
except ImportError as e:
    raise SystemExit(
        "Missing dependency 'matplotlib'. Install it with: pip install matplotlib"
    ) from e

try:
    import numpy as np
except ImportError as e:
    raise SystemExit(
        "Missing dependency 'numpy'. Install it with: pip install numpy"
    ) from e

try:
    import seaborn as sns
except ImportError as e:
    raise SystemExit(
        "Missing dependency 'seaborn'. Install it with: pip install seaborn"
    ) from e


INPUT_CSV = "experiment_results.csv"
OUTPUT_DIR = "Graph"
OUTPUT_1 = os.path.join(OUTPUT_DIR, "1_catch_duration.png")
OUTPUT_2 = os.path.join(OUTPUT_DIR, "2_difficulty_vs_fun.png")
OUTPUT_3 = os.path.join(OUTPUT_DIR, "3_dda_similarity.png")
OUTPUT_4 = os.path.join(OUTPUT_DIR, "4_win_rate.png")
OUTPUT_5 = os.path.join(OUTPUT_DIR, "5_dda_more_fun.png")
OUTPUT_6 = os.path.join(OUTPUT_DIR, "6_flow_state_scatter.png")
OUTPUT_SUMMARY = os.path.join(OUTPUT_DIR, "summary_stats.csv")
MODE_ORDER = ["EASY", "MEDIUM", "HARD", "DDA"]


def _coerce_numeric(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    for col in cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def main(show: bool = False) -> None:
    if not os.path.isfile(INPUT_CSV):
        print(f"Error: '{INPUT_CSV}' not found.")
        print("Please ensure you have run the experiment and the results file exists.")
        return

    df = pd.read_csv(INPUT_CSV)

    # Create output directory for exported charts
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    required_cols = {
        "Mode_Played",
        "Win_Loss",
        "Catch_Duration_Sec",
        "Difficulty_Score",
        "Fun_Score",
        "DDA_Similarity",
        "DDA_More_Fun",
    }
    missing = sorted(required_cols - set(df.columns))
    if missing:
        print("Error: CSV missing required columns:")
        for col in missing:
            print(f"  - {col}")
        return

    df = _coerce_numeric(
        df,
        [
            "Catch_Duration_Sec",
            "Difficulty_Score",
            "Fun_Score",
            "DDA_Similarity",
            "DDA_More_Fun",
        ],
    )

    df["Mode_Played"] = pd.Categorical(df["Mode_Played"], categories=MODE_ORDER, ordered=True)
    df = df.sort_values("Mode_Played")

    sns.set_theme(style="whitegrid")

    # Summary Statistics Table (CSV Export)
    outcomes = df.dropna(subset=["Mode_Played", "Win_Loss"])
    total_by_mode = df.groupby("Mode_Played", observed=False).size().reindex(MODE_ORDER).fillna(0)
    wins_by_mode = (
        outcomes[outcomes["Win_Loss"].astype(str).str.upper() == "WIN"]
        .groupby("Mode_Played", observed=False)
        .size()
        .reindex(MODE_ORDER)
        .fillna(0)
    )
    win_rate_pct = (wins_by_mode / total_by_mode.replace(0, np.nan) * 100.0).fillna(0)

    summary = (
        df.groupby("Mode_Played", observed=False)
        .agg(
            Player_Count=("Player_ID", "count"),
            Avg_Catch_Duration_Sec=("Catch_Duration_Sec", "mean"),
            Avg_Difficulty_Score=("Difficulty_Score", "mean"),
            Avg_Fun_Score=("Fun_Score", "mean"),
        )
        .reindex(MODE_ORDER)
    )
    summary["Win_Rate_Pct"] = win_rate_pct
    summary = summary.reset_index()
    summary.to_csv(OUTPUT_SUMMARY, index=False)

    # 1) Catch Duration per Mode (Boxplot)
    fig, ax = plt.subplots(figsize=(8, 6))
    duration_df = df.dropna(subset=["Catch_Duration_Sec", "Mode_Played"])
    if duration_df.empty:
        ax.text(0.5, 0.5, "No catch duration data to plot", ha="center", va="center")
        ax.set_axis_off()
    else:
        sns.boxplot(
            data=duration_df,
            x="Mode_Played",
            y="Catch_Duration_Sec",
            order=MODE_ORDER,
            ax=ax,
        )
        ax.set_title("Catch Duration per Mode")
        ax.set_xlabel("Mode")
        ax.set_ylabel("Catch Duration (sec)")

    plt.tight_layout()
    plt.savefig(OUTPUT_1, dpi=300, bbox_inches="tight")
    if show:
        plt.show()
    plt.close(fig)

    # 2) Difficulty vs Fun (Grouped Bar)
    fig, ax = plt.subplots(figsize=(10, 6))
    df_scores = df.dropna(subset=["Mode_Played"])
    means = (
        df_scores.groupby("Mode_Played", observed=False)[["Difficulty_Score", "Fun_Score"]]
        .mean(numeric_only=True)
        .reindex(MODE_ORDER)
    )
    means_long = means.reset_index().melt(
        id_vars="Mode_Played",
        value_vars=["Difficulty_Score", "Fun_Score"],
        var_name="Metric",
        value_name="Average",
    )
    means_long["Metric"] = means_long["Metric"].map(
        {"Difficulty_Score": "Difficulty", "Fun_Score": "Fun"}
    )

    if means_long["Average"].dropna().empty:
        ax.text(0.5, 0.5, "No survey score data to plot", ha="center", va="center")
        ax.set_axis_off()
    else:
        sns.barplot(
            data=means_long,
            x="Mode_Played",
            y="Average",
            hue="Metric",
            order=MODE_ORDER,
            ax=ax,
        )
        ax.set_title("Difficulty vs Fun (Average)")
        ax.set_xlabel("Mode")
        ax.set_ylabel("Average Score")
        ax.set_ylim(0, 9.5)
        ax.legend(title="")

    plt.tight_layout()
    plt.savefig(OUTPUT_2, dpi=300, bbox_inches="tight")
    if show:
        plt.show()
    plt.close(fig)

    # 3) DDA Similarity (Pie Chart)
    fig, ax = plt.subplots(figsize=(8, 6))
    dda_df = df[df["Mode_Played"] == "DDA"].dropna(subset=["DDA_Similarity"])
    if dda_df.empty:
        ax.text(0.5, 0.5, "No DDA similarity data to plot", ha="center", va="center")
        ax.set_axis_off()
    else:
        similarity_map = {1: "Easy", 2: "Medium", 3: "Hard"}
        similarity = dda_df["DDA_Similarity"].round().astype("Int64")
        similarity = similarity[similarity.isin([1, 2, 3])]
        counts = similarity.map(similarity_map).value_counts().reindex(["Easy", "Medium", "Hard"]).fillna(0)

        if counts.sum() == 0:
            ax.text(0.5, 0.5, "No valid DDA similarity values (1/2/3)", ha="center", va="center")
            ax.set_axis_off()
        else:
            ax.pie(
                counts.values,
                labels=counts.index,
                autopct=lambda p: f"{p:.1f}%" if p > 0 else "",
                startangle=90,
            )
            ax.set_title("DDA Similarity (Players' Perception)")

    plt.tight_layout()
    plt.savefig(OUTPUT_3, dpi=300, bbox_inches="tight")
    if show:
        plt.show()
    plt.close(fig)

    # 4) Win Rate per Mode (Bar)
    fig, ax = plt.subplots(figsize=(8, 6))
    if outcomes.empty:
        ax.text(0.5, 0.5, "No win/loss data to plot", ha="center", va="center")
        ax.set_axis_off()
    else:
        # Use precomputed totals for consistency with summary export
        win_pct = win_rate_pct

        sns.barplot(
            x=win_pct.index,
            y=win_pct.values,
            order=MODE_ORDER,
            ax=ax,
            color=sns.color_palette("deep")[0],
        )
        ax.set_title("Win Rate per Mode")
        ax.set_xlabel("Mode")
        ax.set_ylabel("Win Rate (%)")
        ax.set_ylim(0, 105)
        for i, val in enumerate(win_pct.values):
            ax.text(i, min(val + 2, 103), f"{val:.1f}%", ha="center", va="bottom", fontsize=9)

    plt.tight_layout()
    plt.savefig(OUTPUT_4, dpi=300, bbox_inches="tight")
    if show:
        plt.show()
    plt.close(fig)

    # 5) DDA 'More Fun' Distribution (Histogram/Bar)
    fig, ax = plt.subplots(figsize=(8, 6))
    dda_more_fun = df[df["Mode_Played"] == "DDA"].dropna(subset=["DDA_More_Fun"])
    if dda_more_fun.empty:
        ax.text(0.5, 0.5, "No DDA 'More Fun' data to plot", ha="center", va="center")
        ax.set_axis_off()
    else:
        scores = dda_more_fun["DDA_More_Fun"].round().astype("Int64")
        scores = scores[(scores >= 0) & (scores <= 9)]
        counts = scores.value_counts().reindex(list(range(0, 10))).fillna(0)

        sns.barplot(
            x=counts.index,
            y=counts.values,
            ax=ax,
            color=sns.color_palette("deep")[2],
        )
        ax.set_title("DDA 'More Fun' Score Distribution")
        ax.set_xlabel("Score (0-9)")
        ax.set_ylabel("Player Count")

    plt.tight_layout()
    plt.savefig(OUTPUT_5, dpi=300, bbox_inches="tight")
    if show:
        plt.show()
    plt.close(fig)

    # 6) Difficulty vs Fun Scatter (Color by Mode, with jitter)
    fig, ax = plt.subplots(figsize=(9, 7))
    scatter_df = df.dropna(subset=["Mode_Played", "Difficulty_Score", "Fun_Score"]).copy()
    if scatter_df.empty:
        ax.text(0.5, 0.5, "No Difficulty/Fun data to plot", ha="center", va="center")
        ax.set_axis_off()
    else:
        # Add a bit of jitter to reduce overplotting
        jitter_scale = 0.12
        scatter_df["Difficulty_J"] = scatter_df["Difficulty_Score"] + np.random.normal(
            0.0, jitter_scale, size=len(scatter_df)
        )
        scatter_df["Fun_J"] = scatter_df["Fun_Score"] + np.random.normal(
            0.0, jitter_scale, size=len(scatter_df)
        )

        palette = {
            "EASY": sns.color_palette("deep")[0],
            "MEDIUM": sns.color_palette("deep")[1],
            "HARD": sns.color_palette("deep")[3],
            # Make DDA pop
            "DDA": "gold",
        }

        sns.scatterplot(
            data=scatter_df,
            x="Difficulty_J",
            y="Fun_J",
            hue="Mode_Played",
            hue_order=MODE_ORDER,
            palette=palette,
            alpha=0.8,
            s=60,
            ax=ax,
        )
        ax.set_title("Difficulty vs Fun (Scatter)")
        ax.set_xlabel("Difficulty Score")
        ax.set_ylabel("Fun Score")
        ax.set_xlim(-0.5, 9.5)
        ax.set_ylim(-0.5, 9.5)
        ax.legend(title="Mode")

    plt.tight_layout()
    plt.savefig(OUTPUT_6, dpi=300, bbox_inches="tight")
    if show:
        plt.show()
    plt.close(fig)

    print("Saved charts to:")
    print(f"  - {OUTPUT_1}")
    print(f"  - {OUTPUT_2}")
    print(f"  - {OUTPUT_3}")
    print(f"  - {OUTPUT_4}")
    print(f"  - {OUTPUT_5}")
    print(f"  - {OUTPUT_6}")
    print(f"  - {OUTPUT_SUMMARY}")


if __name__ == "__main__":
    main(show=False)
