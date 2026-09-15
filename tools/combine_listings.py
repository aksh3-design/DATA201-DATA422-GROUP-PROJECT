from src.main.lib.load.csvconcatenator import CSVConcatenator
import argparse
import pandas as pd

def load_data(args, data, filename, date):
    data.load_csv(f"{args.input_file_directory}/{filename}").filter_rows("neighbourhood_group", "Christchurch City").add_column("month_year", f"{date}").create()

FILE_DATES = [ # I know this isn't ideal
    ("/listings_oct.csv", "2025-10-01"),
    ("/listings_nov.csv", "2025-11-01"),
    ("/listings_dec.csv", "2025-12-01"),
    ("/listings_jan.csv", "2026-01-01"),
    ("/listings_feb.csv", "2026-02-01"),
    ("/listings_mar.csv", "2026-03-01"),
    ("/listings_apr.csv", "2026-04-01"),
    ("/listings_may.csv", "2026-05-01"),
    ("/listings_jun.csv", "2026-06-01")
]

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        prog="Airbnb Listing Dataset Concatenator",
        description="Takes Inside Airbnb listings csv files in given and combines them. Filtering for Christchurch listings.")

    parser.add_argument('input_file_directory')
    parser.add_argument('-o', '--output')

    args = parser.parse_args()

    default_output = "listings_combined.csv"
    data = CSVConcatenator(dtypes={}, na_values={})

    if args.input_file_directory:
        try:
            for filename, date in FILE_DATES:
                load_data(args, data, filename, date)
        except FileNotFoundError:
            print(f"No such file or directory: '{args.input_file_directory}'")
            exit()

    print("combining csv ...")
    data = data.concatenate()

    print("writing csv ...")
    if args.output:
        data.to_csv(f"{args.output}.csv", index=False, date_format="%Y-%m-%d")
    else:
        data.to_csv(f"{default_output}", index=False, date_format="%Y-%m-%d")

    print("combining completed ...")