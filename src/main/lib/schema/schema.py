"""
Internal-Pandas-Dataframe-Handling Schema

compatibility: Inside Airbnb listings-summary V.2 (exclusive)
"""

import pandas as pd
import numpy as np

from pandera.pandas import DataFrameModel, Field, dataframe_check
from datetime import datetime

import pandera.typing as ptp

import json

DISTRICT_WARD_HIERARCHY: list

with open("src/main/lib/schema/neighbourhoods_heirarchy.json", encoding="utf-8") as neighbourhoods_heirarchy:
    DISTRICT_WARD_HIERARCHY = json.load(neighbourhoods_heirarchy)

# listings summary v.2 schema

class ListingsModel(DataFrameModel):
    id                              : int                   = Field(gt=0) 
    name                            : str                                 
    host_id                         : int                   = Field(gt=0, nullable=True) 
    host_name                       : str                   = Field(nullable=True)
    neighbourhood_group             : str                   
    neighbourhood                   : str                   
    latitude                        : float                 = Field(ge=-90, le=90) 
    longitude                       : float                 = Field(ge=-180, le=180) 
    room_type                       : str                   = Field(isin=["Private room", "Entire home/apt", "Shared room", "Hotel room"]) 
    price                           : float                 = Field(ge=0, nullable=True)
    minimum_nights                  : int                   = Field(ge=1, nullable=True) 
    number_of_reviews               : int                   = Field(ge=0) 
    last_review                     : datetime              = Field(nullable=True)
    reviews_per_month               : float                 = Field(gt=0, nullable=True)
    calculated_host_listings_count  : int                   = Field(ge=1, nullable=True) 
    availability_365                : int                   = Field(ge=0) 
    number_of_reviews_ltm           : int                   = Field(ge=0) 
    license                         : str                   = Field(nullable=True) 
    # month_year                      : DatetimeIndex # TODO: reconfigure row-wise formatting to ISO-8601

    @dataframe_check
    def valid_neighbour_heirarchy(
        cls,
        data_frame: pd.DataFrame,
        name = "valid_neighbour_heirarchy") -> ptp.Series[bool]:

        """
        check that ward belongs in district
        """
        return data_frame.apply(
            lambda row: row["neighbourhood"] in DISTRICT_WARD_HIERARCHY.get(row["neighbourhood_group"], []),
            axis = 1
        )

if __name__ == "__main__":
    """testing"""

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

    df = pd.read_csv(
        input("file_path"),
        delimiter=",",
        na_values={
            "name": ["", empty["string"]],
            "host_id" : {"", empty["int64"]},
            "host_name" : {"", empty["string"]},
            "price": ["", empty["float"]],
            "minimum_nights": ["", empty["int64"]],
            "last_review": ["", empty["datetime"]],
            "reviews_per_month": ["", empty["int64"]],
            "calculated_host_listings_count": ["", empty["int64"]],
            "license": ["", empty["string"]]
        },
        dtype=data_types,
        parse_dates=parse_dates
    )

    ListingsModel.validate(df)

    print(df)

    pass