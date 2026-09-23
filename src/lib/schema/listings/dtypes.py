import pandas as pd
import numpy as np

# TODO convert to TOML (maybe)

dtypes = {
    "id"                              : "Int64",
    "neighbourhood"                   : "category",
    "latitude"                        : float,
    "longitude"                       : float,
    "room_type"                       : "category",
    "price"                           : float,
    "minimum_nights"                  : "Int64",
    "number_of_reviews"               : "Int64",
    "calculated_host_listings_count"  : "Int64",
    "availability_365"                : "Int64",
    "number_of_reviews_ltm"           : "Int64",
}

date_fields = [ # datetime
    "month_year"
]

empty = {
    str: pd.NA,
    float: np.nan,
    "Int64": np.nan,
    "datetime": pd.NaT,
}
    
na_values = {
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

    "calculated_host_listings_count":
        [
            "",
            empty["Int64"]
        ],
}