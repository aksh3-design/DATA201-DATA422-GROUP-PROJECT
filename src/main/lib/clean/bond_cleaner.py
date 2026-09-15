from src.main.lib.clean.clean import DataFrameCleaner
from src.main.lib.schema.bonds.dtypes import dtypes, na_values
import pandas as pd
import numpy as np
import json

sa22019_table_path = "src/data/SA22019_TA2019_WARD2019.json"

SA22019_TABLE = None

with open(sa22019_table_path, 'r', encoding='utf-8') as file:
    
    SA22019_TABLE = json.load(file)
    
def clean(data:pd.DataFrame):

    data["TimeFrame"] = pd.to_datetime(data["TimeFrame"], format="ISO8601")

    # remove -99 + NULL

    data = data[~(data["Location Id"] == -99)] # not a valid SA22019 id num

    data = data.dropna(subset=["Location Id"])
    data["Location Id"] = data["Location Id"].astype("int64")

    data["TA2019"] = data["Location Id"].apply(parse_TA2019)
    data["WARD2019"] = data["Location Id"].apply(parse_WARD2019)

    data = data.astype(dtype=dtypes)

    return data

def parse_TA2019(code:int|str):
    """
    Takes SA2-2019 location codes and converts them into TA2019 names.

    Args:
        code (int): SA2-2019 area code
    Returns:
            str: TA2019 name. 
    """
    return SA22019_TABLE[str(code)]["TA2019_name"]

def parse_WARD2019(code:int|str):
    """
    Takes SA2-2019 location codes and converts them into WARD2019 names.

    Args:
        code (int): SA2-2019 area code
    Returns:
            str: WARD2019 name. 
    """
    return SA22019_TABLE[str(code)]["WARD2019_name"]
    # return result

def parse_num_beds(value:str):
    """
    Takes a string value and categorises it into; 1, 2, 3, 4, 5, 5+, NA;
    based on the definitions given by the market-rent API.

    Args:
        value (str): Number of Beds string value entry.

    Returns:
        str: categorised value
    """
    err_entries = {
        "5+", # set any integer greater than 5 to 5+
        "NA", # set to negative one, statistic not available
        "ALL" # statistics across all categories of bedroom count. (Either lump all bedroom count into)
    }

    # NOTE: may not be implemented

    pass
    # return result



if __name__ == "__main__":
    pass