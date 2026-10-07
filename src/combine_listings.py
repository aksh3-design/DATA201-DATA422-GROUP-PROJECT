from src.lib.csvconcatenator import CSVConcatenator
from src.lib.schema.listings.dtypes import dtypes, na_values
from src.config import LISTINGS_SA22026_PATH, LISTINGS_PREPROCESSED_PATH, LISTINGS_COMBINED_PATH, LISTINGS_ALL, get_listings
import pandas as pd
import os


def load_data(data_parser: CSVConcatenator, filename: str, date: str):
    """Adds csv data to CSVConcatenator.
    Args:
         data_parser (CSVConcatenator): CSVConcatenator object.
         dir_path (str): Path to directory of listing.csv data.
         filename (str): Listings data filename.
         date (str): Publish date of listings data.
     """
    data_parser.load_csv(f"{filename}").filter_rows("neighbourhood_group", "Christchurch City").add_column("month_year", f"{date}").create()
    
def combine_pre_processed_data():
    
    previous_path = LISTINGS_PREPROCESSED_PATH # data that has already been through query process
    current_path = LISTINGS_SA22026_PATH # combine after querying
    
    print("loading previous listings data ...")
    
    if not os.path.exists(previous_path):
        print(f"No such file or directory: '{previous_path}'")
        exit()

    preprocessed_data = CSVConcatenator(dtypes=dtypes, na_values=na_values).load_csv(previous_path)
    preprocessed_data.create()

    all_data = preprocessed_data.load_csv(current_path)
    all_data.create()

    all_data:pd.DataFrame = all_data.concatenate()

    all_data.to_csv(LISTINGS_ALL, index=False)

if __name__ == "__main__":
    
    data_parser = CSVConcatenator(dtypes={}, na_values={})

    for filename, date in get_listings():
        try:
            load_data(data_parser, filename, date)
        except FileNotFoundError:
            print(f"No such file or directory: '{filename}'")
            exit()

    print("combining csv ...")
    data_parser = data_parser.concatenate()

    print("writing csv ...")

    data_parser.to_csv(f"{LISTINGS_COMBINED_PATH}", index=False, date_format="%Y-%m-%d")

    print("combining completed ...")