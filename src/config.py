import tomllib
import pandas as pd
import json

with open("data.toml", "rb") as f:
    __config_data = tomllib.load(f)

# resolve paths to data directories

DATA_IN = __config_data["path"]["dir"]["in"]
DATA_OUT = __config_data["path"]["dir"]["out"]
DATA_TMP = __config_data["path"]["dir"]["tmp"]
DATA_FIG = __config_data["path"]["dir"]["fig"]

# resolve path to lookup tables for location codes

__sa22019_table_path = __config_data["path"]["location"]["name"]+__config_data["path"]["location"]["type"]

def _get_SA22019_TA2019_WARD2019_table(filepath:str=__sa22019_table_path):
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

# resolve path to airbnb listings data

__airbnb_basename = __config_data["path"]["airbnb"]["base_name"]
__airbnb_combine = __config_data["path"]["airbnb"]["combine_ext"]
__airbnb_clean = __config_data["path"]["airbnb"]["clean_ext"]
__airbnb_type = __config_data["path"]["airbnb"]["type"]

LISTINGS_COMBINED_PATH = DATA_TMP + __airbnb_basename + __airbnb_combine + __airbnb_type
LISTINGS_CLEANED_PATH = DATA_TMP + __airbnb_basename + __airbnb_combine + __airbnb_clean + __airbnb_type

def get_listings():
    """generates listings names and scrapedate from ./data.toml file

    Yields:
        tuple[str, datetime]: _description_
    """
    for __airbnb_listings_name, __scrape_date in __config_data["path"]["airbnb"]["data"]["listings"]:
        yield (DATA_IN + __airbnb_listings_name + __airbnb_type, __scrape_date)

# resolve path to listings data converted by koordinates queries

__airbnb_sa22026_basename = __config_data["path"]["airbnb"]["data"]["query"]["base_name"]
__airbnb_sa22026_query = __config_data["path"]["airbnb"]["data"]["query"]["query_ext"]
__airbnb_sa22026_type = __config_data["path"]["airbnb"]["data"]["query"]["type"]

LISTINGS_SA22026_PATH = DATA_TMP + __airbnb_sa22026_basename + __airbnb_sa22026_query + __airbnb_sa22026_type

# resolve path to tenancy services rental bond data

__bonds_basename = __config_data["path"]["bonds"]["name"]
__bonds_clean = __config_data["path"]["bonds"]["clean_ext"]
__bonds_type = __config_data["path"]["bonds"]["type"]

BONDS_CLEANED_PATH = DATA_TMP + __bonds_basename + __bonds_clean + __bonds_type

BONDS_PATH = DATA_IN + __bonds_basename + __bonds_type

# TODO: resolve path to joined data

__joined_basename = __config_data["path"]["joined"]["name"]
__joined_type = __config_data["path"]["joined"]["type"]

JOINED_PATH = DATA_OUT + __joined_basename + __joined_type

# resolve data processing constraints 

with open("config.toml", "rb") as f:
    __config_settings = tomllib.load(f)

END_DATE = pd.to_datetime(__config_settings["daterange"]["end_date"])
START_DATE = pd.to_datetime(__config_settings["daterange"]["start_date"])

API_KEY = __config_settings["api"]["key"]

OPENFIG = __config_settings["config"]["openfig"]
SAVEFIG = __config_settings["config"]["savefig"]
VERBOSE = __config_settings["config"]["verbose"]

def load_csv(filepath_or_buffer, dtype, na_values):
    try:
        return pd.read_csv(filepath_or_buffer=filepath_or_buffer, dtype=dtype, na_values=na_values)
    except FileNotFoundError:
        if VERBOSE:
            print(f"Warning. {filepath_or_buffer} not found or does not exist.")

