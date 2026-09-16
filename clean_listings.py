import pandas as pd
from pathlib import Path

def clean_listings(
    input_path="data/raw/listings_combined.csv",
    output_path="data/processed/listings_cleaned.csv"
):
    print("--- Cleaning Christchurch Airbnb Listings ---")
    df = pd.read_csv(input_path)
    initial_rows = len(df)
    print(f"Initial listings count: {initial_rows}")

    # 1. Exact duplicates removal
    df = df.drop_duplicates()
    print(f"Rows after dropping exact duplicates: {len(df)}")

    # 2. Missing values in essential identification/spatial columns
    essential_cols = ['id', 'latitude', 'longitude', 'neighbourhood', 'room_type', 'month_year']
    df = df.dropna(subset=essential_cols)
    print(f"Rows after dropping essential missing values: {len(df)}")

    # 3. Invalid values: remove prices <= 0, retain NaN prices
    df = df[~((df['price'].notna()) & (df['price'] <= 0))]
    
    # 4. Check coordinate bounds (-90 to 90 lat, -180 to 180 long)
    df = df[(df['latitude'].between(-90, 90)) & (df['longitude'].between(-180, 180))]
    print(f"Rows after validity checks: {len(df)}")

    # 5. Drop unneeded columns while preserving spatial and pricing features
    cols_to_keep = [
        'id', 'neighbourhood', 'latitude', 'longitude', 'room_type',
        'price', 'minimum_nights', 'number_of_reviews',
        'calculated_host_listings_count', 'availability_365',
        'number_of_reviews_ltm', 'month_year'
    ]
    df_cleaned = df[cols_to_keep]

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    df_cleaned.to_csv(output_path, index=False)
    print(f"Saved cleaned listings to: {output_path} (Final rows: {len(df_cleaned)})\n")
    return df_cleaned

if __name__ == "__main__":
    clean_listings()