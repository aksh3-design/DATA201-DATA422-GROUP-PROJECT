import argparse
import pandas as pd
from src.main.lib.schema.bonds.dtypes import dtypes
import json

import statsmodels.api as sm
import numpy as np

import sys
from pathlib import Path

sys.path.insert(0, Path(__file__).parent)

import configparser

config = configparser.ConfigParser()

config.read("src/data/data_range.ini")

START_DATE = [config["daterange"]["start_date"]]
END_DATE = [config["daterange"]["end_date"]]

sa22019_table_path = "src/data/SA22019_TA2019_WARD2019.json"

SA22019_TABLE = None

with open(sa22019_table_path, 'r', encoding='utf-8') as file:
    
    SA22019_TABLE = json.load(file)
    
def clean(data:pd.DataFrame):

    initial_rows = data.shape[0]

    print(f"{'num rows':10}|{'removed':10}| log")

    # ================================================================================

    print(f"{data.shape[0]:10}|{initial_rows-data.shape[0]:10}| datetime datatype correction ...")

    data["TimeFrame"] = pd.to_datetime(data["TimeFrame"], format="ISO8601")

    # ================================================================================
    # remove -99 + NULL

    print(f"{data.shape[0]:10}|{data.shape[0]-initial_rows:10}| removing invalid -99 location codes ...")
    data = data[~(data["Location Id"] == "-99")] # not a valid SA22019 id num

    # ================================================================================

    print(f"{data.shape[0]:10}|{data.shape[0]-initial_rows:10}| removing invalid NULL location codes ...")

    data = data[~(data["Location Id"] == "NULL")] # not a valid SA22019 id num

    data = data.dropna(subset=["Location Id"])
    data["Location Id"] = data["Location Id"].astype("int64")

    # ================================================================================

    print(f"{data.shape[0]:10}|{data.shape[0]-initial_rows:10}| parsing TA2019 and WARD2019 location names from SA2-2019 'Location Id' ...")

    data["TA2019"] = data["Location Id"].apply(parse_TA2019)
    data["WARD2019"] = data["Location Id"].apply(parse_WARD2019)

    # correct Number Of Beds column

    # ================================================================================

    print(f"{data.shape[0]:10}|{data.shape[0]-initial_rows:10}| parsing Number of Beds Categories ...")

    data["Number Of Beds"] = data["Number Of Beds"].apply(parse_num_beds)

    # ================================================================================

    # remove for ease of MICE imputation of Log Std Dev, Location Id, Geometric Mean Rent

    drop_columns = [
            "Upper Quartile Rent",
            "Lower Quartile Rent",
            "Median Rent"
            ]

    print(f"{data.shape[0]:10}|{data.shape[0]-initial_rows:10}| drop columns:")

    for col in drop_columns:
        print(f"{'':10}|{'':10}|\t - '{col}'")

    data = data.drop(columns=drop_columns)

    # ================================================================================

    print(f"{data.shape[0]:10}|{data.shape[0]-initial_rows:10}| preparing columns dtypes for multiple imputation ...")
    
    data = prep_col(data, "Log Std Dev Weekly Rent", float)
    data = prep_col(data, "Geometric Mean Rent", float)
    data = prep_col(data, "Total Bonds", int)
    data = prep_col(data, "Active Bonds", int)
    data = prep_col(data, "Closed Bonds", int)

    data.columns = data.columns.str.replace(" ", "_") # statsmodels library does not like spaces in column names

    # ================================================================================

    print(f"{data.shape[0]:10}|{data.shape[0]-initial_rows:10}| multiple imputation on remaining columns ...")

    mice_data = sm.MICEData(data[[
        "Log_Std_Dev_Weekly_Rent",
        "Geometric_Mean_Rent",
        "Total_Bonds",
        "Active_Bonds",
        "Closed_Bonds"
        ]])

    mice_data.update_all(n_iter=10) # recommended from lectures

    # ================================================================================

    print(f"{data.shape[0]:10}|{data.shape[0]-initial_rows:10}| imputations complete!")

    data[[
        "Log_Std_Dev_Weekly_Rent",
        "Geometric_Mean_Rent",
        "Total_Bonds",
        "Active_Bonds",
        "Closed_Bonds"
        ]] = mice_data.data

    data.columns = data.columns.str.replace("_", " ") # maintaining the standard

    # ================================================================================

    print(data.columns)

    data = data.astype(dtype=dtypes)

    print(f"{data.shape[0]:10}|{data.shape[0]-initial_rows:10}| filtering for date range {START_DATE} - {END_DATE} ...")

    data = data[data["TimeFrame"].between(START_DATE[0], END_DATE[0])]

    print(f"{data.shape[0]:10}|{data.shape[0]-initial_rows:10}| Writing ...")

    return data

def prep_col(data:pd.DataFrame, col_name:str, type):

    data[col_name] = pd.to_numeric(data[col_name], errors='coerce')
    data[col_name] = data[col_name].astype(type)

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
    # pass

    parser = argparse.ArgumentParser(
        prog="Tenancy Bonds Dataset Cleaning Utility",
        description="Takes detailed quaterly datasets and prepares them according to the bonds dataset schema.")

    parser.add_argument('input_filename')
    parser.add_argument('-o', '--output')

    args = parser.parse_args()

    default_output = "cleaned_bonds_data.csv"
    data = None

    if args.input_filename:
        try:
            print("loading csv ...")
            data = pd.read_csv(f"{args.input_filename}.csv", dtype={"Number Of Beds" : "string"}, keep_default_na=False) # NA is a category, not null
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

