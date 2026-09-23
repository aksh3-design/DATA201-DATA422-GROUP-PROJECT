# Tenancy Bonds Dataset Cleaning Utility.
# More information in docs/bondclean.md

from lib.schema.bonds.dtypes import dtypes
from lib.transform import filter_row_by_value, parse_column_entries, to_numerical_specific
from lib.log import print_clean_log, print_clean_cascade, print_clean_simple
from config import DATA_IN_PATH, DATA_OUT_PATH, START_DATE, END_DATE, SA22019_TABLE 

import pandas as pd
import statsmodels.api as sm

# clean the dataset

def clean(data:pd.DataFrame):

    initial_rows = data.shape[0]

    drop_columns = [ # remove for ease of MICE imputation of Log Std Dev, Location Id, Geometric Mean Rent
            "Upper Quartile Rent",
            "Lower Quartile Rent",
            "Median Rent"
            ]
    
    mice_columns = {
            "Log Std Dev Weekly Rent": float,
            "Geometric Mean Rent": float,
            "Total Bonds": int,
            "Active Bonds": int,
            "Closed Bonds": int
            }

    # drop unnecessary columns =======================================================

    print_clean_log(data, initial_rows, "log")

    print_clean_log(data, initial_rows, "drop columns:")
    print_clean_cascade(drop_columns)
    
    data = data.drop(columns=drop_columns)
    
    # convert TimeFrame to datetime datatype =========================================

    print_clean_log(data, initial_rows, "datetime datatype correction ...")
    data["TimeFrame"] = pd.to_datetime(data["TimeFrame"], format="ISO8601")

    # remove -99 + NULL ==============================================================

    print_clean_log(data, initial_rows, "removing invalid -99 location codes ...")
    data = filter_row_by_value(data, "Location Id", "-99")

    print_clean_log(data, initial_rows, "removing invalid NULL location codes ...")
    data = filter_row_by_value(data, "Location Id", "NULL")

    # remove missing location codes ==================================================

    print_clean_log(data, initial_rows, "removing missing location codes ...")
    
    data = data.dropna(subset=["Location Id"])
    data["Location Id"] = data["Location Id"].astype("int64")

    # parse functions ================================================================

    print_clean_log(data, initial_rows, "parsing TA2019 and WARD2019 location names from SA2-2019 'Location Id' ...")

    data = parse_column_entries(data, "Location Id", parse_TA2019, True, "TA2019")
    data = parse_column_entries(data, "Location Id", parse_WARD2019, True, "WARD2019")

    print_clean_log(data, initial_rows, "parsing Number of Beds Categories ...")

    data = parse_column_entries(data, "Number Of Beds", parse_num_beds)

    # convert datatypes of columns to suitable type for mice =========================

    print_clean_log(data, initial_rows, "preparing columns dtypes for multiple imputation ...")
    print_clean_cascade(mice_columns)

    for column, type in mice_columns.items():
        data = to_numerical_specific(data, column, type)

    # convert column names to suitable format for statsmodel library =================

    temp_mice_column_names = []

    for column in mice_columns.keys():
        temp_mice_column_names.append(column.replace(" ", "_"))
    
    data.columns = data.columns.str.replace(" ", "_") # statsmodels library does not support spaces in column names

    # run mice on columns ============================================================

    print_clean_log(data, initial_rows, "multiple imputation on remaining columns ...")
    print_clean_cascade(mice_columns.keys())

    mice_data = sm.MICEData(data[temp_mice_column_names])
    mice_data.update_all(n_iter=10) # recommended iteration count from lectures

    # cleanup column names, column datatypes =========================================

    print_clean_log(data, initial_rows, "imputations complete!")

    data[temp_mice_column_names] = mice_data.data
    data.columns = data.columns.str.replace("_", " ")

    data = data.astype(dtype=dtypes)

    # filter for entries with daterange (see date_range.ini) =========================

    print_clean_log(data, initial_rows, f"filtering for date range {START_DATE} - {END_DATE} ...")

    data = data[data["TimeFrame"].between(START_DATE, END_DATE)]

    # filter for entrise in Christchurch City ========================================

    print_clean_log(data, initial_rows, "Removing rows not in Christchurch City")

    data = filter_row_by_value(data, "TA2019", "Christchurch City")

    print_clean_log(data, initial_rows, "Cleanup Complete.")

    return data

def parse_TA2019(code:int|str):
    """
    Takes SA2-2019 location codes and converts them into TA2019 names.

    Args:
        code (int): SA2-2019 area code
    Returns:
            str: TA2019 name. 
    """

    try:
        result = SA22019_TABLE[str(code)]["TA2019_name"]
    except KeyError:
        result = code

    return result

def parse_WARD2019(code:int|str):
    """
    Takes SA2-2019 location codes and converts them into WARD2019 names.

    Args:
        code (int): SA2-2019 area code
    Returns:
            str: WARD2019 name. 
    """
    
    try:
        result = SA22019_TABLE[str(code)]["WARD2019_name"]
    except KeyError:
        result = code
    
    return result

def parse_num_beds(val:str):
    """
    Takes string type entries from 'Number Of Beds' column and parses a to-spec categorical string classifcation.

    Args:
        val (str): entry (Number Of Beds)

    Returns:
        str: categorical classification
    """

    val = str(val)

    match val:
        case "1":
            return val
        case "2":
            return val
        case "3":
            return val
        case "4":
            return val
        case "5":
            return "5+"
        case "5+":
            return val
        case "NA":
            return val
        case "ALL":
            return val

    # handle rouge numbers

    if int(val) > 5:
        return "5+"
    if int(val) < 1:
        return "NA"

if __name__ == "__main__":

    from pathlib import Path

    filename = "Detailed-Quarterly-Tenancy-Q1-2020-Q3-2026.csv"
    filepath = Path(f"{DATA_IN_PATH}{filename}")
    fileout = Path(f"{DATA_OUT_PATH}{filename}")

    data = None

    print(f"{'num rows':10}|{'removed':10}| log")

    try:
        print_clean_simple("loading csv ...")
        data = pd.read_csv(filepath, dtype={"Number Of Beds" : "string"}, keep_default_na=False) # NA is a category, not null
    except FileNotFoundError:
        print_clean_simple(f"No such file or directory: '{filepath}'")
        exit()

    print_clean_simple("cleaning csv ...")
    data = clean(data)

    print_clean_simple("writing csv ...")
    data.to_csv(f"{fileout}", index=False)

    print_clean_simple("cleaning completed.")

