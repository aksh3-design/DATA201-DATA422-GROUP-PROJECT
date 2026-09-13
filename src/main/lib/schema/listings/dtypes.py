import pandas as pd
import numpy as np

# TODO convert to TOML (maybe)

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