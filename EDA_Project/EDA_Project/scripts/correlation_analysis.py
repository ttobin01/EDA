"""
correlation_analysis.py

Step 8 (Section 10.1):
1. Correlation matrix for numeric columns (excluding loan_id and
   borrower_id), rounded to 2 decimals, plus the three strongest
   correlations (positive or negative, excluding self-correlation).
2. Scatter plot of credit_score (x) vs. interest_rate (y), colored by
   loan_status, saved to outputs/scatter_credit_rate.png.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
DATA_PATH = PROJECT_ROOT / "02_Data" / "Raw" / "wildcat_loans_clean.csv"
OUTPUT_DIR = PROJECT_ROOT / "outputs"

BLUE = "#2a78d6"
ORANGE = "#eb6834"
AQUA = "#1baf7a"
YELLOW = "#eda100"
INK = "#0b0b0b"
MUTED = "#898781"
GRID = "#e1e0d9"

STATUS_ORDER = ["Current", "Paid Off", "Delinquent", "Default"]
STATUS_COLORS = {"Current": BLUE, "Paid Off": ORANGE, "Delinquent": AQUA, "Default": YELLOW}

EXCLUDE_COLS = ["loan_id", "borrower_id"]


def print_correlations(df: pd.DataFrame) -> None:
    numeric_df = df.select_dtypes(include="number").drop(columns=EXCLUDE_COLS, errors="ignore")
    corr = numeric_df.corr().round(2)

    print("Correlation matrix:")
    print(corr.to_string())
    print()

    # Strongest correlations, excluding self-correlation and duplicate pairs
    pairs = []
    cols = corr.columns
    for i in range(len(cols)):
        for j in range(i + 1, len(cols)):
            pairs.append((cols[i], cols[j], corr.iloc[i, j]))

    pairs.sort(key=lambda p: abs(p[2]), reverse=True)

    print("Three strongest correlations:")
    for a, b, val in pairs[:3]:
        print(f"  {a} <-> {b}: {val:+.2f}")


def make_scatter(df: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(9, 6), facecolor="#fcfcfb")
    ax.set_facecolor("#fcfcfb")

    for status in STATUS_ORDER:
        subset = df[df["loan_status"] == status]
        ax.scatter(
            subset["credit_score"], subset["interest_rate"],
            s=18, alpha=0.55, color=STATUS_COLORS[status], label=status,
            edgecolors="none",
        )

    ax.set_title("Credit Score vs. Interest Rate by Loan Status",
                  fontsize=13, color=INK, fontweight="bold", pad=14)
    ax.set_xlabel("Credit Score", color=INK, fontsize=10)
    ax.set_ylabel("Interest Rate (%)", color=INK, fontsize=10)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(MUTED)
    ax.spines["bottom"].set_color(MUTED)
    ax.tick_params(colors=INK)
    ax.grid(color=GRID, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)

    legend = ax.legend(title="Loan Status", frameon=False, loc="upper right")
    legend.get_title().set_color(INK)
    for text in legend.get_texts():
        text.set_color(INK)

    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "scatter_credit_rate.png", dpi=150)
    plt.close(fig)


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    df = pd.read_csv(DATA_PATH)

    print_correlations(df)
    print()
    make_scatter(df)
    print(f"Saved: {OUTPUT_DIR / 'scatter_credit_rate.png'}")


if __name__ == "__main__":
    main()
