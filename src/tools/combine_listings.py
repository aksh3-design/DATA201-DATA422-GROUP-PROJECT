from src.main.lib.load.csvconcatenator import CSVConcatenator
from src.main.lib.config import DATA_IN_PATH, DATA_OUT_PATH, NAMES, DATES

def load_data(data_parser:CSVConcatenator, filename:str, date:str):
    """Adds csv data to CSVConcatenator.

    Args:
        data_parser (CSVConcatenator): CSVConcatenator object.
        dir_path (str): Path to directory of listing.csv data.
        filename (str): Listings data filename.
        date (str): Publish date of listings data.
    """
    data_parser.load_csv(f"{DATA_IN_PATH}{filename}").filter_rows("neighbourhood_group", "Christchurch City").add_column("month_year", f"{date}").create()

if __name__ == "__main__":

    fileout = "listings_combined.csv"

    data_parser = CSVConcatenator(dtypes={}, na_values={})

    for filename, date in zip(NAMES, DATES):
        try:
            load_data(data_parser, filename, date)
        except FileNotFoundError:
            print(f"No such file or directory: '{DATA_IN_PATH}{filename}'")
            exit()

    print("combining csv ...")
    data_parser = data_parser.concatenate()

    print("writing csv ...")

    data_parser.to_csv(f"{DATA_OUT_PATH}{fileout}", index=False, date_format="%Y-%m-%d")
    
    print("combining completed ...")