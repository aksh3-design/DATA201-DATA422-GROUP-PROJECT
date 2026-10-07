from lib.csvconcatenator import CSVConcatenator
from config import get_listings, LISTINGS_COMBINED_PATH

import pandas as pd
import os


def load_data(data_parser: CSVConcatenator, filename: str, date: str):
    """Adds csv data to CSVConcatenator."""

    data_parser.load_csv(filename) \
        .filter_rows("neighbourhood_group", "Christchurch City") \
        .add_column("month_year", date) \
        .create()


if __name__ == "__main__":

    # Previous combined data: October 2025 - June 2026
    previous_path = "data/listings_previous.csv"

    print("loading previous listings data ...")

    if not os.path.exists(previous_path):
        print(f"No such file or directory: '{previous_path}'")
        exit()

    previous_data = pd.read_csv(previous_path)

    # Load new July and August files from data.toml
    data_parser = CSVConcatenator(dtypes={}, na_values={})

    for filename, date in get_listings():
        try:
            load_data(data_parser, filename, date)
        except FileNotFoundError:
            print(f"No such file or directory: '{filename}'")
            exit()

    print("combining new csv files ...")
    new_data = data_parser.concatenate()

    # Combine previous data with the new months
    print("adding new months to previous listings data ...")

    combined_data = pd.concat(
        [previous_data, new_data],
        ignore_index=True
    )

    # Prevent duplicate property records within the same month
    combined_data = combined_data.drop_duplicates(
        subset=["id", "month_year"],
        keep="last"
    )

    # Sort by month
    combined_data["month_year"] = pd.to_datetime(
        combined_data["month_year"]
    )

    combined_data = combined_data.sort_values("month_year")

    print("writing csv ...")

    combined_data.to_csv(
        LISTINGS_COMBINED_PATH,
        index=False,
        date_format="%Y-%m-%d"
    )

    print("combining completed ...")
