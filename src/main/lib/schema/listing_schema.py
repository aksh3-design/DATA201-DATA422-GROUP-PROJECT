import numpy as np
import pandas as pd

class ListingSchema:
    """
    Details the types and columns expected of a listings flie.
    The purpose of this class is to handle file imports.
    """

    def __init__(self, filepath:str):

        self.filepath = filepath

        self.data_types = {
            "id"                              : int,
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
            "number_of_reviews"               : int,
            "reviews_per_month"               : float,
            "calculated_host_listings_count"  : "Int64",
            "availability_365"                : int,
            "number_of_reviews_ltm"           : int,
            "license"                         : str
        }
    
        self.parse_dates = ["last_review"]
    
        self.empty = {
            "string": pd.NA,
            "float": np.nan,
            "int64": np.nan,
            "datetime": pd.NaT,
        }
    
        self.na_values = {
            "name":
                [
                    "",
                    self.empty["string"]
                ],
            "host_id" :
                [
                    "",
                    self.empty["int64"]
                ],
            "host_name" :
                [
                    "",
                    self.empty["string"]
                ],
            "price":
                [
                    "",
                    self.empty["float"]
                ],
            "minimum_nights":
                [
                    "",
                    self.empty["int64"]
                ],
            "last_review":
                [
                    "",
                    self.empty["datetime"]
                ],
            "reviews_per_month":
                [
                    "",
                    self.empty["int64"]
                ],
            "calculated_host_listings_count":
                [
                    "",
                    self.empty["int64"]
                ],
            "license":
                [
                    "",
                    self.empty["string"
                ]]
            }

    def read_csv(self) -> pd.DataFrame:
        return pd.read_csv(
            filepath_or_buffer=self.filepath,
            dtype=self.data_types,
            parse_dates=self.parse_dates,
            na_values=self.na_values)