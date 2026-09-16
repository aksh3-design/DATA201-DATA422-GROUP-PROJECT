import pandas as pd
from pathlib import Path

def clean_bonds(
    input_path="data/raw/Detailed-Quarterly-Tenancy-Q1-2020-Q3-2026.csv",
    output_path="data/processed/bonds_cleaned.csv"
):
    print("--- Cleaning Tenancy Services Rental Bond Data ---")
    df = pd.read_csv(input_path)
    print(f"Initial bond records: {len(df)}")

    # 1. Filter timeframe to match listings (Q4 2025, Q1 2026, Q2 2026)
    target_quarters = ['2025-10-01', '2026-01-01', '2026-04-01']
    df_filtered = df[df['TimeFrame'].isin(target_quarters)].copy()
    print(f"Rows after timeframe filtering (Q4 2025 - Q2 2026): {len(df_filtered)}")

    # 2. Filter missing Location Id
    df_filtered = df_filtered.dropna(subset=['Location Id'])
    print(f"Rows after removing missing Location Id: {len(df_filtered)}")

    # 3. Remove non-specific Location Id == -99
    df_filtered = df_filtered[df_filtered['Location Id'] != -99].copy()
    print(f"Rows after removing Location Id == -99: {len(df_filtered)}")

    # Standardize Location Id as integer
    df_filtered['Location Id'] = df_filtered['Location Id'].astype(int)

    # 4. Save cleaned dataset
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    df_filtered.to_csv(output_path, index=False)
    print(f"Saved cleaned bond data to: {output_path} (Final rows: {len(df_filtered)})\n")
    return df_filtered

if __name__ == "__main__":
    clean_bonds()