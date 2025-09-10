# src/validate_data.py
import pandas as pd
import sys
from collections import Counter

PATH = "../data/raw.csv"   # run this from src/ with `python validate_data.py`

def main():
    try:
        df = pd.read_csv(PATH)
    except Exception as e:
        print("ERROR reading CSV:", e); sys.exit(1)
    # basic checks
    required = {"id","text","label"}
    if not required.issubset(set(df.columns)):
        print("MISSING COLUMNS. CSV must contain:", required); sys.exit(1)
    print("Rows:", len(df))
    missing_text = df['text'].isnull().sum()
    print("Missing text values:", missing_text)
    # class counts
    counts = Counter(df['label'].astype(str))
    print("Label counts:")
    for k,v in counts.items():
        print(f"  {k}: {v}")
    # show sample rows (first 5)
    print("\nSample rows:")
    print(df.head(5).to_string(index=False))

if __name__ == '__main__':
    main()
