"""
Details the types and columns expected of a listings flie.
The purpose of this file is to handle missing values.
"""

import numpy as np
import pandas as pd
import pandera.pandas as pa
from datetime import datetime

dwelling_types = [
    "ALL",
    "Apartment",
    "Boarding House",
    "Flat",
    "House",
    "Room"
]

schema = pa.DataFrameSchema({
        "TimeFrame"                         : pa.Column(
            "datetime"
            ),
        "Location Id"                       : pa.Column(
            int
            ),
        "Dwelling Type"                     : pa.Column(
            pa.Category,
            pa.Check.isin(dwelling_types),
            nullable=False
            ),
        "Number Of Beds"                    : pa.Column(
            pa.Category,
            nullable=True # null values indicate availability
            ),
        "Total Bonds"                       : pa.Column(
            int
            ),
        "Active Bonds"                      : pa.Column(
            int
            ),
        "Closed Bonds"                      : pa.Column(
            int
            ),
        "Median Rent"                       : pa.Column(
            float
            ),
        "Geometric Mean Rent"               : pa.Column(
            float
            ),
        "Upper Quartile Rent"               : pa.Column(
            float
            ),
        "Lower Quartile Rent"               : pa.Column(
            float
            ),
        "Log Std Dev Weekly Rent"           : pa.Column(
            float,
            default = 0 # if there is no variation in weekly rent across bonds, std_dev will be 0, log(0) undefined.
            )
})
