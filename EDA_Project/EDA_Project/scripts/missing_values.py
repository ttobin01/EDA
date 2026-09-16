"""
missing_values.py

Step 3 (Section 5.2): Print count and percentage of missing values for
every column. Then, for credit_score specifically, compare the
loan_status and loan_purpose distributions among rows where credit_score
is missing vs. the full dataset, to check whether the missingness looks
random or concentrated in a particular group.
"""

from pathlib import Path

import pandas as pd

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
DATA_PATH = PROJECT_ROOT / "02_Data" / "Raw" / "wildcat_loans_clean.csv"


def main() -> None:
    df = pd.read_csv(DATA_PATH)
    n = len(df)

    print("Missing values per column (count and percentage):")
    missing = df.isnull().sum()
    for col, count in missing.items():
        pct = count / n * 100
        print(f"  {col:<30} {count:>6}   {pct:5.2f}%")
    print()

    missing_mask = df["credit_score"].isna()
    n_missing = missing_mask.sum()
    print(f"Rows with missing credit_score: {n_missing} ({n_missing / n * 100:.1f}% of all loans)")
    print()

    for col in ["loan_status", "loan_purpose"]:
        print(f"--- {col}: missing-credit_score rows vs. full dataset ---")
        missing_dist = (
            df.loc[missing_mask, col].value_counts(normalize=True).mul(100).round(1)
        )
        full_dist = df[col].value_counts(normalize=True).mul(100).round(1)
        comparison = pd.DataFrame(
            {"missing_credit_score_%": missing_dist, "full_dataset_%": full_dist}
        ).fillna(0.0)
        comparison = comparison.sort_values("full_dataset_%", ascending=False)
        print(comparison.to_string())
        print()


if __name__ == "__main__":
    main()
