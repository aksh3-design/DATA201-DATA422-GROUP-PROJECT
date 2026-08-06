import numpy as np
import pandas as pd

# These specify the exact datatypes to be interpreted for the listing schema for each column, as well as their default values.

data_types = {
    "id"                              : int,
    "name"                            : str,
    "host_id"                         : "Int64", # built-in int data types do not support nullification, pandas explicitly declared types are required here.
    "host_name"                       : str,
    "neighbourhood_group"             : str,
    "neighbourhood"                   : str,
    "latitude"                        : float,
    "longitude"                       : float,
    "room_type"                       : str,
    "price"                           : float,
    "minimum_nights"                  : "Int64",
    "number_of_reviews"               : int,
    "reviews_per_month"               : float,
    "calculated_host_listings_count"  : "Int64",
    "availability_365"                : int,
    "number_of_reviews_ltm"           : int,
    "license"                         : str
}

parse_dates = ["last_review"]

empty = {
    "string": pd.NA,
    "float": np.nan,
    "int64": np.nan,
    "datetime": pd.NaT,
}

na_values = {
    "name":
        [
            "",
            empty["string"]
        ],
    "host_id" :
        [
            "",
            empty["int64"]
        ],
    "host_name" :
        [
            "",
            empty["string"]
        ],
    "price":
        [
            "",
            empty["float"]
        ],
    "minimum_nights":
        [
            "",
            empty["int64"]
        ],
    "last_review":
        [
            "",
            empty["datetime"]
        ],
    "reviews_per_month":
        [
            "",
            empty["int64"]
        ],
    "calculated_host_listings_count":
        [
            "",
            empty["int64"]
        ],
    "license":
        [
            "",
            empty["string"
        ]]
    }