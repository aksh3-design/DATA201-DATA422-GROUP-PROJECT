import argparse
import pandas as pd
from src.main.lib.schema.listings.dtypes import dtypes

import statsmodels.api as sm
import numpy as np
    
def clean(data:pd.DataFrame):

    initial_rows = data.shape[0]

    print(f"{'num rows':10}|{'removed':10}| log")

    print(f"{data.shape[0]:10}|{data.shape[0]-initial_rows:10}| datetime datatype correction ...")

    data["last_review"] = pd.to_datetime(data["last_review"], format="ISO8601")
    
    data["month_year"] = pd.to_datetime(data["month_year"], format="ISO8601")

    print(f"{data.shape[0]:10}|{data.shape[0]-initial_rows:10}| category datatype correction ...")

    data["neighbourhood"] = data["neighbourhood"].astype("category")

    drop_columns = [
            "name",
            "host_id",
            "host_name",
            "neighbourhood_group",
            "last_review",
            "reviews_per_month",
            "license"
        ]

    print(f"{data.shape[0]:10}|{data.shape[0]-initial_rows:10}| drop columns:")
    
    for col in drop_columns:
        print(f"{'':10}|{'':10}|\t - '{col}'")

    data.drop(columns=drop_columns, inplace=True)

    print(f"{data.shape[0]:10}|{data.shape[0]-initial_rows:10}| one-hot encoding room_type for use in multiple imputation ...")

    data = pd.concat([data, pd.get_dummies(data[["room_type"]], dtype=int)], axis=1) # one-hot encode roomtype and append for imputation (It makes sense that this would affect the price)
    data.drop(columns=["room_type_Entire home/apt"], inplace=True) # instead of drop_first=True, for generality

    data.columns = data.columns.str.replace(" ", "_") # statsmodels library does not like spaces in column names

    print(f"{data.shape[0]:10}|{data.shape[0]-initial_rows:10}| multiple imputation to find missing price values ...")

    micedata = sm.MICEData(data[[
        "room_type_Hotel_room",
        "room_type_Private_room",
        "room_type_Shared_room",
        "price",
        "number_of_reviews_ltm",
        "availability_365"
    ]])

    micedata.update_all(n_iter=10)

    data[[
            "room_type_Hotel_room",
            "room_type_Private_room",
            "room_type_Shared_room",
            "price",
            "number_of_reviews_ltm",
            "availability_365"
        ]] = micedata.data

    print(f"{data.shape[0]:10}|{data.shape[0]-initial_rows:10}| drop encoded columns")

    data.drop(columns=["room_type_Hotel_room", "room_type_Private_room", "room_type_Shared_room"], inplace=True)

    data = data.astype(dtype=dtypes)

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










