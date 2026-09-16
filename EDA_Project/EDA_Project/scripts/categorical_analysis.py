"""
categorical_analysis.py

Step 5 (Section 7.1): For each categorical column (loan_purpose,
loan_status, state), print the count and percentage of rows for each
unique value, sorted from most to least frequent. Percentages shown to
one decimal place.
"""

from pathlib import Path

import pandas as pd

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
DATA_PATH = PROJECT_ROOT / "02_Data" / "Raw" / "wildcat_loans_clean.csv"

CATEGORICAL_COLUMNS = ["loan_purpose", "loan_status", "state"]


def main() -> None:
    df = pd.read_csv(DATA_PATH)

    for col in CATEGORICAL_COLUMNS:
        counts = df[col].value_counts()
        pcts = df[col].value_counts(normalize=True).mul(100).round(1)
        table = pd.DataFrame({"count": counts, "pct": pcts})
        print(f"--- {col} ({df[col].nunique()} unique values) ---")
        print(table.to_string())
        print()


if __name__ == "__main__":
    main()
