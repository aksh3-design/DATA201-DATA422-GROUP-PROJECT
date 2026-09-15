import argparse
import pandas as pd
from src.main.lib.schema.bonds.dtypes import dtypes
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

if __name__ == "__main__":
    pass

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
            data = pd.read_csv(f"{args.input_filename}.csv")
        except FileNotFoundError:
            print(f"No such file or directory: '{args.input_filename}'")
            exit()

    print("cleaning csv ...")
    data = clean(data)

    print("writing csv ...")
    if args.output:
        data.to_csv(f"{args.output}.csv")
    else:
        data.to_csv(f"{default_output}")

    print("cleaning completed.")

