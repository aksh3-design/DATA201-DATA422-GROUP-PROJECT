import pandas as pd
import numpy as np

# TODO convert to TOML (maybe)

dtypes = {
    "Location Id"                       : "Int64",
    "Dwelling Type"                     : "category",
    "Number Of Beds"                    : "Int64",
    "Total Bonds"                       : "Int64",
    "Active Bonds"                      : "Int64",
    "Closed Bonds"                      : "Int64",
    "Median Rent"                       : float,
    "Geometric Mean Rent"               : float,
    "Upper Quartile Rent"               : float,
    "Lower Quartile Rent"               : float,
    "Log Std Dev Weekly Rent"           : float
}

date_fields = [ # datetime
    "TimeFrame"
]

empty = {
    str: pd.NA,
    float: np.nan,
    "Int64": np.nan,
    "datetime": pd.NaT,
}
    
na_values = {
    "TimeFrame"                         : empty["datetime"],
    "Location Id"                       : empty["Int64"],
    "Dwelling Type"                     : empty["category"],
    "Number Of Beds"                    : empty["Int64"],
    "Total Bonds"                       : empty["Int64"],
    "Active Bonds"                      : empty["Int64"],
    "Closed Bonds"                      : empty["Int64"],
    "Median Rent"                       : empty[float],
    "Geometric Mean Rent"               : empty[float],
    "Upper Quartile Rent"               : empty[float],
    "Lower Quartile Rent"               : empty[float],
    "Log Std Dev Weekly Rent"           : empty[float],
}