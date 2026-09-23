# Collection of functions which loads variables from configfiles

import pandas as pd

CONFIG_INI_PATH = "src/data/config.ini"

import configparser
import json

config = configparser.ConfigParser()
config.read(CONFIG_INI_PATH)

SA22019_TABLE_PATH = config["data"]["sa22019"]
DATA_IN_PATH = config["dirpath"]["in"]
DATA_OUT_PATH = config["dirpath"]["out"]

START_DATE = pd.to_datetime(config["daterange"]["start_date"], format="ISO8601")
END_DATE = pd.to_datetime(config["daterange"]["end_date"], format="ISO8601")

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