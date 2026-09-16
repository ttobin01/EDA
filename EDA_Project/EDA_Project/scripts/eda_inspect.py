"""
eda_inspect.py

Loads wildcat_loans_clean.csv from the project's data folder and prints
basic structural information: shape, column names with data types, and
missing-value counts per column.

Run from anywhere inside the project (path is resolved relative to this
script's own location, not the current working directory):

    python scripts/eda_inspect.py
"""

from pathlib import Path

import pandas as pd

# This script lives in <project_root>/scripts/, and the data lives in
# <project_root>/02_Data/Raw/ — resolve relative to this file so it works
# no matter where you run it from.
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
DATA_PATH = PROJECT_ROOT / "02_Data" / "Raw" / "wildcat_loans_clean.csv"


def main() -> None:
    df = pd.read_csv(DATA_PATH)

    print(f"Loaded: {DATA_PATH}")
    print()

    print(f"Shape: {df.shape[0]} rows x {df.shape[1]} columns")
    print()

    print("Column names and data types:")
    for col, dtype in df.dtypes.items():
        print(f"  {col:<30} {dtype}")
    print()

    missing = df.isnull().sum()
    print("Missing values per column:")
    for col, count in missing.items():
        print(f"  {col:<30} {count}")


if __name__ == "__main__":
    main()
