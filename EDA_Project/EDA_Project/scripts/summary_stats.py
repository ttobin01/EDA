"""
summary_stats.py

Step 4 (Section 6.2): Print descriptive statistics (count, mean, std,
min, 25th percentile, median, 75th percentile, max) for all numeric
columns. Loan amounts are rounded to two decimal places.
"""

from pathlib import Path

import pandas as pd

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
DATA_PATH = PROJECT_ROOT / "02_Data" / "Raw" / "wildcat_loans_clean.csv"


def main() -> None:
    df = pd.read_csv(DATA_PATH)

    numeric_df = df.select_dtypes(include="number")
    stats = numeric_df.describe().T.round(2)

    pd.set_option("display.width", 120)
    print(stats.to_string())


if __name__ == "__main__":
    main()
