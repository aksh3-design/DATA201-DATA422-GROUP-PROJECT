"""
Internal-Pandas-Dataframe-Handling Schema

compatibility: Inside Airbnb listings-summary V.2 (exclusive)
"""

from pandera.pandas import DataFrameModel, Field, dataframe_check
from pandera.typing import Series
from pandas import CategoricalDtype
from datetime import datetime

from typing import Optional

# import pandas as pd
# import pandera.typing as ptp

import json

DISTRICT_WARD_HIERARCHY: list

with open("src/main/lib/schema/neighbourhoods_heirarchy.json", encoding="utf-8") as neighbourhoods_heirarchy:
    DISTRICT_WARD_HIERARCHY = json.load(neighbourhoods_heirarchy)

NEIGHBOURHOOD_GROUPS:list = DISTRICT_WARD_HIERARCHY.keys()

NEIGHBOURHOODS:list = []

for district in DISTRICT_WARD_HIERARCHY.items():
    NEIGHBOURHOODS += district # NOTE: there are duplicate names for neighbourhoods, in response I will simply ignore it

# listings summary v.2 schema

class ListingModel(DataFrameModel):
    id                              : Optional[int]                             = Field(gt = 0) 
    name                            : Optional[str]                             # somehow the only reliable data from Inside Airbnb
    host_id                         : Optional[int]                             = Field(nullable = True, gt = 0, ) 
    host_name                       : Optional[str]                             = Field(nullable = True)
    neighbourhood_group             : Optional[Series[CategoricalDtype]]        = Field(isin = NEIGHBOURHOOD_GROUPS)
    neighbourhood                   : Optional[Series[CategoricalDtype]]        = Field(isin = NEIGHBOURHOODS)
    latitude                        : Optional[float]                           = Field(ge = -90, le = 90) 
    longitude                       : Optional[float]                           = Field(ge = -180, le = 180) 
    room_type                       : Optional[Series[CategoricalDtype]]        = Field(isin = ["Private room", "Entire home/apt", "Shared room", "Hotel room"]) 
    price                           : Optional[float]                           = Field(nullable = True, ge = 0)
    minimum_nights                  : Optional[int]                             = Field(nullable = True, ge = 1) 
    number_of_reviews               : Optional[int]                             = Field(ge = 0) 
    last_review                     : Optional[datetime]                        = Field(nullable = True)
    reviews_per_month               : Optional[float]                           = Field(nullable = True, gt = 0)
    calculated_host_listings_count  : Optional[int]                             = Field(nullable = True, ge = 1) 
    availability_365                : Optional[int]                             = Field(ge = 0) 
    number_of_reviews_ltm           : Optional[int]                             = Field(ge = 0) 
    license                         : Optional[str]                             = Field(nullable = True) 
    # month_year                      : DatetimeIndex # TODO: reconfigure row-wise formatting to ISO-8601

    #NOTE: this is definitely too much for now, I will keep it here commented just in case

    # @dataframe_check
    # def valid_neighbour_heirarchy(
    #     cls,
    #     data_frame: pd.DataFrame,
    #     name = "valid_neighbour_heirarchy") -> ptp.Series[bool]:

    #     """
    #     check that ward belongs in district
    #     """
    #     return data_frame.apply(
    #         lambda row: row["neighbourhood"] in DISTRICT_WARD_HIERARCHY.get(row["neighbourhood_group"], []),
    #         axis = 1
    #     )

    #NOTE: this is definitely too much for now, I will keep it here commented just in case