"""
grouping_analysis.py

Step 7 (Section 9.2):
1. Group by loan_status: count, mean loan_amount (2dp), mean interest_rate
   (4dp), mean credit_score excluding nulls (1dp), mean debt_to_income_ratio
   (4dp). Sorted by count descending.
2. Group by loan_purpose: count of loans and count/percentage with
   loan_status == "Default". Sorted by default percentage descending.
"""

from pathlib import Path

import pandas as pd

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
DATA_PATH = PROJECT_ROOT / "02_Data" / "Raw" / "wildcat_loans_clean.csv"


def main() -> None:
    df = pd.read_csv(DATA_PATH)

    print("--- Grouped by loan_status ---")
    by_status = (
        df.groupby("loan_status")
        .agg(
            count=("loan_status", "size"),
            mean_loan_amount=("loan_amount", "mean"),
            mean_interest_rate=("interest_rate", "mean"),
            mean_credit_score=("credit_score", "mean"),
            mean_debt_to_income=("debt_to_income_ratio", "mean"),
        )
        .sort_values("count", ascending=False)
    )
    by_status["mean_loan_amount"] = by_status["mean_loan_amount"].round(2)
    by_status["mean_interest_rate"] = by_status["mean_interest_rate"].round(4)
    by_status["mean_credit_score"] = by_status["mean_credit_score"].round(1)
    by_status["mean_debt_to_income"] = by_status["mean_debt_to_income"].round(4)
    print(by_status.to_string())
    print()

    print("--- Grouped by loan_purpose: default rate ---")
    total_by_purpose = df.groupby("loan_purpose").size().rename("count")
    default_by_purpose = (
        df[df["loan_status"] == "Default"].groupby("loan_purpose").size().rename("default_count")
    )
    purpose_table = pd.concat([total_by_purpose, default_by_purpose], axis=1).fillna(0)
    purpose_table["default_count"] = purpose_table["default_count"].astype(int)
    purpose_table["default_pct"] = (purpose_table["default_count"] / purpose_table["count"] * 100).round(2)
    purpose_table = purpose_table.sort_values("default_pct", ascending=False)
    print(purpose_table.to_string())


if __name__ == "__main__":
    main()
