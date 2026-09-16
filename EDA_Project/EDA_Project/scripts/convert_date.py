"""
convert_date.py

Step 2 (Section 4.2): Check whether origination_date is stored as a
datetime type. If it is stored as text, convert it to datetime and print
a before/after confirmation.
"""

from pathlib import Path

import pandas as pd

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
DATA_PATH = PROJECT_ROOT / "02_Data" / "Raw" / "wildcat_loans_clean.csv"


def main() -> None:
    df = pd.read_csv(DATA_PATH)

    before_type = df["origination_date"].dtype
    print(f"origination_date type BEFORE conversion: {before_type}")

    if pd.api.types.is_datetime64_any_dtype(df["origination_date"]):
        print("Column is already a datetime type. No conversion needed.")
        return

    df["origination_date"] = pd.to_datetime(df["origination_date"])

    after_type = df["origination_date"].dtype
    print(f"origination_date type AFTER conversion:  {after_type}")
    print()
    print("Conversion successful." if str(after_type).startswith("datetime64")
          else "Conversion did not produce a datetime type - investigate date formatting.")


if __name__ == "__main__":
    main()
