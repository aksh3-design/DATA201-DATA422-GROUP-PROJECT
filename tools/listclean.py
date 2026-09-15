import argparse
import pandas as pd
from src.main.lib.schema.listings.dtypes import dtypes
    
def clean(data:pd.DataFrame):

    data["neighbourhood"] = data["neighbourhood"].astype("category")
    
    data["last_review"] = pd.to_datetime(data["last_review"], format="ISO8601")
    
    data["month_year"] = pd.to_datetime(data["month_year"], format="ISO8601")

    data.drop(columns=[
        "name",
        "host_id",
        "host_name",
        "neighbourhood_group",
        "last_review",
        "reviews_per_month",
        "license"
    ])

    return data

if __name__ == "__main__":
    pass

    parser = argparse.ArgumentParser(
        prog="Airbnb Listing Dataset Cleaner",
        description="Takes Inside Airbnb listings csv files for New Zealand and cleans them according to the listings dataset schema.")

    parser.add_argument('input_filename')
    parser.add_argument('-o', '--output')

    args = parser.parse_args()

    default_output = "cleaned_listing_data.csv"
    data = None

    if args.input_filename:
        try:
            print("loading csv ...")
            data = pd.read_csv(f"{args.input_filename}.csv")
        except FileNotFoundError:
            print(f"No such file or directory: '{args.input_filename}'")
            exit()

    print("cleaning csv ...")
    data = clean(data)

    print("writing csv ...")
    if args.output:
        data.to_csv(f"{args.output}.csv", index=False)
    else:
        data.to_csv(f"{default_output}", index=False)

    print("cleaning completed.")

