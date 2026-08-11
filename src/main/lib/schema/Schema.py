"""
Details the types and columns expected of a listings flie.
The purpose of this file is to handle missing values.
"""

import numpy as np
import pandas as pd
import pandera.pandas as pa
from datetime import datetime
import json

with open("src/main/lib/schema/neighbourhoods_heirarchy.json", 'r', encoding='utf-8') as file:
    
    heirarchy = json.load(file)
    
    neighbourhood_groups = list(heirarchy.keys())
    neighbourhoods = []
    
    for neighbourhood_group in neighbourhood_groups:
        neighbourhoods += heirarchy[neighbourhood_group]

room_types = [
    "Private room",
    "Entire home/apt",
    "Shared room",
    "Hotel room"
]

schema = pa.DataFrameSchema({
    "id"                                : pa.Column(
        int
        ),
    "name"                              : pa.Column(
        str
        ),
    "host_id"                           : pa.Column(
        int
        ),
    "host_name"                         : pa.Column(
        str,
        nullable=True # this can be determined with host_id
        ),
    "neighbourhood_group"               : pa.Column(
        pa.Category,
        checks=pa.Check.isin(neighbourhood_groups)
        ),
    "neighbourhood"                     : pa.Column(
        pa.Category,
        checks=pa.Check.isin(neighbourhoods)
        ),
    "latitude"                          : pa.Column(
        float,
        checks=pa.Check(
            lambda x: -90 <= x <= 90,
            element_wise = True
            )
        ),
    "longitude"                         : pa.Column(
        float,
        checks=pa.Check(
            lambda x: -180 <= x < 180,
            element_wise = True
            )
        ),
    "room_type"                         : pa.Column(
        pa.Category,
        checks=pa.Check.isin(room_types)
        ),
    "price"                             : pa.Column(
        float,
        nullable=True, # price is null for many reasons, thus it will not be defaulted to zero
        ),
    "minimum_nights"                    : pa.Column(
        int,
        nullable=True
        ),
    "number_of_reviews"                 : pa.Column(
        int
        ),
    "last_review"                       : pa.Column(
        "datetime",
        nullable=True # if number of reviews is 0, missing value
        ),
    "reviews_per_month"                 : pa.Column(
        float,
        default=0 # if number of reviews is 0, division by zero gives Nan, thus default is 0
        ),
    "calculated_host_listings_count"    : pa.Column(
        int,
        ),
    "availability_365"                  : pa.Column(
        int,
        ),
    "number_of_reviews_ltm"             : pa.Column(
        int,
        ),
    "license"                           : pa.Column(
        str,
        nullable=True # idk what this does.
        ),
    "month_year"                        : pa.Column(
        "datetime"
        )
})