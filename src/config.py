# Collection of functions which loads variables from configfiles

import pandas as pd
import src.lib.schema.bonds.dtypes as bonds
import src.lib.schema.listings.dtypes as listings

CONFIG_INI_PATH = "config.ini"

import configparser
import json

config = configparser.ConfigParser()
config.read(CONFIG_INI_PATH)

DATA_IN_PATH = config["dirpath"]["in"]
DATA_OUT_PATH = config["dirpath"]["out"]

def load_csv(filepath_or_buffer, dtype, na_values):
    try:
        return pd.read_csv(filepath_or_buffer=filepath_or_buffer, dtype=dtype, na_values=na_values)
    except FileNotFoundError:
        print(f"Warning. {filepath_or_buffer} not found or does not exist.")

AIRBNB_RAW_NAME = config["data.airbnb"]["raw"]
BONDS_RAW_NAME = config["data.bonds"]["raw"]
AIRBNB_CLEAN_NAME = config["data.airbnb"]["clean"]
BONDS_CLEAN_NAME = config["data.bonds"]["clean"]

AIRBNB_RAW = load_csv(DATA_IN_PATH+AIRBNB_RAW_NAME, listings.dtypes,  listings.na_values)
BONDS_RAW = load_csv(DATA_IN_PATH+BONDS_RAW_NAME, bonds.dtypes,  bonds.na_values)
AIRBNB_CLEAN = load_csv(DATA_IN_PATH+AIRBNB_CLEAN_NAME, listings.dtypes,  listings.na_values)
BONDS_CLEAN = load_csv(DATA_IN_PATH+BONDS_CLEAN_NAME, bonds.dtypes,  bonds.na_values)

# For reviews per month statistics

REVIEWS_RESULTS = config["data.reviews.monthly_results"]["clean"]

REVIEWS_NUMBER = config["data.reviews.figure.number"]["clean"]
REVIEWS_TOPTEN = config["data.reviews.figure.topten"]["clean"]
REVIEWS_TOPTWENTY = config["data.reviews.figure.toptwenty"]["clean"]
REVIEWS_HIGHEST = config["data.reviews.figure.highest"]["clean"]

# For cleaning Utilities

SA22019_TABLE_PATH = config["data"]["sa22019"]

START_DATE = pd.to_datetime(config["daterange"]["start_date"], format="ISO8601")
END_DATE = pd.to_datetime(config["daterange"]["end_date"], format="ISO8601")

API_KEY = config["api"]["key"]

# For combine_listings.py

NAMES = config["listings"]["names"].split()
DATES = config["listings"]["dates"].split()

def _get_SA22019_TA2019_WARD2019_table(filepath:str=SA22019_TABLE_PATH):
    """Generates lookup table to parse SA22019 codes to TA2019 and WARD2019 codes and names

    Args:
        filepath (str, optional): Path to SA22019_TA2019_WARD2019.json. Defaults to SA22019_TABLE_PATH.

    Returns:
        Any: json.load object.
    """
    with open(filepath, 'r', encoding='utf-8') as file:
        
        results = json.load(file)

    return results

SA22019_TABLE = _get_SA22019_TA2019_WARD2019_table()