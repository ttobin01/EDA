"""
distribution_analysis.py

Step 6 (Section 8.2):
1. Histogram of loan_amount (30 bins) with vertical lines at the mean
   and median, saved to outputs/hist_loan_amount.png.
2. Horizontal box plot of interest_rate across the four loan_status
   categories, saved to outputs/box_interest_by_status.png.
"""

from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

# matplotlib 3.11 renamed boxplot's `vert` (bool) to `orientation` (str);
# `vert` still works but prints a deprecation warning. Use whichever this
# installed version expects.
_MPL_VERSION = tuple(int(p) for p in matplotlib.__version__.split(".")[:2])
_BOXPLOT_ORIENTATION_KWARGS = (
    {"orientation": "horizontal"} if _MPL_VERSION >= (3, 11) else {"vert": False}
)

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
STATUS_COLORS = [BLUE, ORANGE, AQUA, YELLOW]


def style_axes(ax):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(MUTED)
    ax.spines["bottom"].set_color(MUTED)
    ax.tick_params(colors=INK)
    ax.grid(axis="x", color=GRID, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)


def make_histogram(df: pd.DataFrame) -> None:
    mean_val = df["loan_amount"].mean()
    median_val = df["loan_amount"].median()

    fig, ax = plt.subplots(figsize=(9, 5.5), facecolor="#fcfcfb")
    ax.set_facecolor("#fcfcfb")

    ax.hist(df["loan_amount"], bins=30, color=BLUE, edgecolor="#fcfcfb", linewidth=0.5, zorder=2)

    ax.axvline(mean_val, color=ORANGE, linewidth=2, linestyle="--", zorder=3)
    ax.axvline(median_val, color=AQUA, linewidth=2, linestyle="--", zorder=3)

    ymax = ax.get_ylim()[1]
    ax.text(mean_val, ymax * 0.97, f"  Mean: ${mean_val:,.0f}", color=ORANGE,
            va="top", ha="left", fontsize=10, fontweight="bold")
    ax.text(median_val, ymax * 0.88, f"  Median: ${median_val:,.0f}", color=AQUA,
            va="top", ha="left", fontsize=10, fontweight="bold")

    ax.set_title("Distribution of Loan Amounts — Wildcat Capital Portfolio",
                  fontsize=13, color=INK, fontweight="bold", pad=14)
    ax.set_xlabel("Loan Amount ($)", color=INK, fontsize=10)
    ax.set_ylabel("Number of Loans", color=INK, fontsize=10)

    style_axes(ax)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "hist_loan_amount.png", dpi=150)
    plt.close(fig)


def make_boxplot(df: pd.DataFrame) -> None:
    groups = [df.loc[df["loan_status"] == status, "interest_rate"] for status in STATUS_ORDER]

    fig, ax = plt.subplots(figsize=(9, 5), facecolor="#fcfcfb")
    ax.set_facecolor("#fcfcfb")

    bp = ax.boxplot(
        groups,
        **_BOXPLOT_ORIENTATION_KWARGS,
        patch_artist=True,
        tick_labels=STATUS_ORDER,
        widths=0.55,
        medianprops={"color": INK, "linewidth": 1.8},
        whiskerprops={"color": MUTED},
        capprops={"color": MUTED},
        flierprops={"markerfacecolor": MUTED, "markeredgecolor": "none", "markersize": 4, "alpha": 0.6},
    )
    for patch, color in zip(bp["boxes"], STATUS_COLORS):
        patch.set_facecolor(color)
        patch.set_alpha(0.85)
        patch.set_edgecolor("#fcfcfb")

    ax.set_title("Interest Rate by Loan Status", fontsize=13, color=INK, fontweight="bold", pad=14)
    ax.set_xlabel("Interest Rate (%)", color=INK, fontsize=10)

    style_axes(ax)
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "box_interest_by_status.png", dpi=150)
    plt.close(fig)


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    df = pd.read_csv(DATA_PATH)

    make_histogram(df)
    make_boxplot(df)

    print(f"Saved: {OUTPUT_DIR / 'hist_loan_amount.png'}")
    print(f"Saved: {OUTPUT_DIR / 'box_interest_by_status.png'}")

    # Quick numeric summary alongside the charts
    print()
    print(f"loan_amount  mean=${df['loan_amount'].mean():,.2f}  median=${df['loan_amount'].median():,.2f}")
    print()
    print("interest_rate by loan_status:")
    print(df.groupby("loan_status")["interest_rate"].describe()[["mean", "50%", "std"]].round(2).reindex(STATUS_ORDER))


if __name__ == "__main__":
    main()
