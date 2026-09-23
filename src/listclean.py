# Airbnb Listings Dataset Cleaning Utility.
# More information in docs/listclean.md

from src.main.lib.schema.listings.dtypes import dtypes
from main.lib.transform import one_hot_encode
from main.lib.log import print_clean_log, print_clean_cascade, print_clean_simple

import pandas as pd
import statsmodels.api as sm

import configparser

# gather configurations into global variables

def get_daterange_from_config(filepath:str="src/data/data_range.ini"):
    """Loades data date ranges from configuration files"""
    config = configparser.ConfigParser()

    config.read(filepath)

    return ([config["daterange"]["start_date"]], [config["daterange"]["end_date"]])

START_DATE, END_DATE = get_daterange_from_config() 
    
def clean(data:pd.DataFrame):

    initial_rows = data.shape[0]

    drop_columns = [
            "name",
            "host_id",
            "host_name",
            "neighbourhood_group",
            "last_review",
            "reviews_per_month",
            "license"
        ]

    mice_columns = [
            "room_type_Hotel_room",
            "room_type_Private room",
            "room_type_Shared_room",
            "price",
            "number_of_reviews_ltm",
            "availability_365"
        ]

    drop_after_mice = [
        "number_of_reviews",
        "number_of_reviews_ltm",
        "availability_365",
        "calculated_host_listings_count"
    ]

    # drop unnecessary columns =======================================================

    print_clean_log(data, initial_rows, "drop columns:")
    print_clean_cascade(drop_columns)

    data = data.drop(columns=drop_columns)

    # convert TimeFrame to datetime datatype =========================================

    print_clean_log(data, initial_rows, "datetime datatype correction ...")
    data["month_year"] = pd.to_datetime(data["month_year"], format="ISO8601")

    # convert neighbourhood to category datatype =====================================

    print_clean_log(data, initial_rows, "category datatype correction ...")
    data["neighbourhood"] = data["neighbourhood"].astype("category")

    # one-hot encode categorical data for use in mice ================================

    print_clean_log(data, initial_rows, "one-hot encoding room_type for use in multiple imputation ...")

    data = one_hot_encode(data, "room_type")
    data.drop(columns=["room_type_Entire home/apt"], inplace=True) # Generates a more stable model

    # convert column names to suitable format for statsmodel library =================

    temp_mice_column_names = []

    for column in mice_columns:
        temp_mice_column_names.append(column.replace(" ", "_"))

    data.columns = data.columns.str.replace(" ", "_") # statsmodels library does not support spaces in column names

    # run mice on columns ============================================================

    print_clean_log(data, initial_rows, "multiple imputation to find missing price values ...")
    print_clean_cascade(mice_columns)

    mice_data = sm.MICEData(data[temp_mice_column_names])

    mice_data.update_all(n_iter=10)

    print_clean_log(data, initial_rows, "imputations complete!")

    # cleanup column names, column datatypes =========================================

    data[temp_mice_column_names] = mice_data.data
    data = data.astype(dtypes) 

    # drop one-hot encoded columns ===================================================

    print_clean_log(data, initial_rows, "drop encoded columns")

    data = data.drop(columns=["room_type_Hotel_room", "room_type_Private_room", "room_type_Shared_room"])

    # filter for entries with daterange (see date_range.ini) =========================

    print_clean_log(data, initial_rows, f"filtering for date range {START_DATE} - {END_DATE} ...")
    
    data = data[data["month_year"].between(START_DATE[0], END_DATE[0])]

    print_clean_log(data, initial_rows, "Writing ...")

    # remove columns relevant only for mice ==========================================

    data = data.drop(columns=drop_after_mice)

    return data

if __name__ == "__main__":

    from pathlib import Path
    
    filename = "listings_combined.csv"
    filepath = Path(f"./data/{filename}")
    fileout = Path(f"./out/{filename}")

    data = None

    print(f"{'num rows':10}|{'removed':10}| log")

    try:
        print_clean_simple("loading csv ...")
        data = pd.read_csv(filepath)
    except FileNotFoundError:
        print_clean_simple(f"No such file or directory: '{filepath}'")
        exit()

    print_clean_simple("cleaning csv ...")
    data = clean(data)

    print_clean_simple("writing csv ...")
    data.to_csv(f"{fileout}", index=False)

    print_clean_simple("cleaning completed.")











