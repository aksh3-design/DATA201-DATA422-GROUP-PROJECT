import pandas as pd
import numpy as np

dtypes = {
    "id"                              : "Int64",
    "name"                            : str,
    "host_id"                         : "Int64", # built-in int data types do not support nullification, pandas explicitly declared types are required here.
    "host_name"                       : str,
    "neighbourhood_group"             : "category",
    "neighbourhood"                   : "category",
    "latitude"                        : float,
    "longitude"                       : float,
    "room_type"                       : "category",
    "price"                           : float,
    "minimum_nights"                  : "Int64",
    "number_of_reviews"               : "Int64",
    "reviews_per_month"               : float,
    "calculated_host_listings_count"  : "Int64",
    "availability_365"                : "Int64",
    "number_of_reviews_ltm"           : "Int64",
    "license"                         : str,
}

date_fields = [ # datetime
    "last_review",
    "month_year"
]

empty = {
    str: pd.NA,
    float: np.nan,
    "Int64": np.nan,
    "datetime": pd.NaT,
}
    
na_values = {
    "name":
        [
            "",
            empty[str]
        ],
    "host_id" :
        [
            "",
            empty["Int64"]
        ],
    "host_name" :
        [
            "",
            empty[str]
        ],
    "price":
        [
            "",
            empty[float]
        ],
    "minimum_nights":
        [
            "",
            empty["Int64"]
        ],
    "last_review":
        [
            "",
            empty["datetime"]
        ],
    "reviews_per_month":
        [
            "",
            empty["Int64"]
        ],
    "calculated_host_listings_count":
        [
            "",
            empty["Int64"]
        ],
    "license":
        [
            "",
            empty[str
        ]]
}

def load_csv(filename:str):
    """loads csv to spec"""
    
    df = pd.read_csv(
        filepath_or_buffer=filename,
        dtype=dtypes,
        na_values=na_values
    )
    
    df["neighbourhood"] = df["neighbourhood"].astype("category")
    
    df["last_review"] = pd.to_datetime(df["last_review"], format="ISO8601")
    
    df["month_year"] = pd.to_datetime(df["month_year"], format="ISO8601")
    
    return df

class CSVConcatenator:
    
    def __init__(self):

        self.dfs:list[pd.DataFrame] = []
        self.current_csv:pd.DataFrame = None
    
    def concatenate(self):
        return pd.concat(
                    self.dfs,
                    ignore_index=True
                )
    
    def add_column(self, column_name:str, row_values:str):
        self.current_csv[column_name] = row_values
        
        return self
    
    def load_csv(self, filename:str):
        
        df = pd.read_csv(
            filepath_or_buffer=filename,
            dtype=dtypes,
            na_values=na_values)
        
        self.current_csv = df
        
        return self
    
    def filter_rows(self, column_name, row_value):
        self.current_csv = self.current_csv[self.current_csv[column_name].str.contains(
            row_value, case=False, na=False
        )]
        return self
    
    def create(self):
        
        self.dfs.append(self.current_csv)
        
