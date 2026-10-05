import pandas as pd
import matplotlib.pyplot as plt

from src.lib.log import log
from src.lib.plots import plot_box_plot
from config import LISTINGS_SA22026_PATH, BONDS_CLEANED_PATH, JOINED_PATH, DATA_FIG
# TODO: move these filepaths to congif.ini. (maybe, possibly not necessary)

airbnb = pd.read_csv(f"{LISTINGS_SA22026_PATH}")
bonds = pd.read_csv(f"{BONDS_CLEANED_PATH}")

airbnb["month_year"] = pd.to_datetime(airbnb["month_year"])
bonds["TimeFrame"] = pd.to_datetime(bonds["TimeFrame"])

airbnb["quarter"] = airbnb["month_year"].dt.to_period("Q")
bonds["quarter"] = bonds["TimeFrame"].dt.to_period("Q")

airbnb = airbnb[["price", "SA22026_code", "SA22026_name", "quarter", "neighbourhood", "month_year", "id"]]
# airbnb = airbnb.groupby(["SA22026_code", "quarter"]).mean()

bonds_all = bonds[
    (bonds["Dwelling Type"] == "ALL") &
    (bonds["Number Of Beds"] == "ALL") &
    (bonds["TA2019"] == "Christchurch City")
].copy()


bonds_all = bonds_all.rename(
    columns={"Location Id": "SA22026_code"}
)

bonds_all = bonds_all[
    [
        "SA22026_code",
        "quarter",
        "Median Rent",
        "Total Bonds",
        "Active Bonds",
        "Closed Bonds"
    ]
]

merged = airbnb.merge(
    bonds_all,
    on=["SA22026_code", "quarter"],
    how="left"
)

log("Airbnb rows:", len(airbnb))
log("Merged rows:", len(merged))

log()
log(
    "Missing Median Rent price:",
    merged["Median Rent"].isna().sum()
)

log()
log("Example Christchurch Central:")

log(
    merged[
        merged["SA22026_code"] == 326600
    ][
        [
            "month_year",
            "SA22026_code",
            "SA22026_name",
            "price",
            "Median Rent",
            "Total Bonds"
        ]
    ].head(10).to_string(index=False)
)

central = merged[
    merged["SA22026_code"] == 326600
]

median_price = central["price"].median()

log()
log("Christchurch Central")
log("Number of observations:", len(central))
log("Median Airbnb price: $", median_price)

merged["long_term_nightly"] = (
    merged["Median Rent"] / 7
)

merged["price_gap"] = (
    merged["price"] -
    merged["long_term_nightly"]
)

gap_data = merged.dropna(
    subset=["price_gap"]
).copy()

log()
log(
    "Number of Airbnb observations with rental data:",
    len(gap_data)
)

log()
log("Example price gaps:")

log(
    gap_data[
        [
            "SA22026_code",
            "SA22026_name",
            "price",
            "long_term_nightly",
            "price_gap"
        ]
    ]
    .head(10)
    .sort_values("price_gap", ascending=False)
    .to_string(index=False)
)

location_gap = (
    gap_data
    .groupby(
        ["SA22026_code", "SA22026_name"]
    )["price_gap"]
    .agg(
        count="count",
        mean="mean",
        median="median"
    )
    .reset_index()
)

location_gap_median = (
    location_gap
    .sort_values(
        "median",
        ascending=False
    )
)

log()
log("Locations with the largest median price gaps:")

log(
    location_gap_median
    .head(10)
    .sort_values("median", ascending=False)
    .to_string(index=False)
)

top_locations = (
    location_gap_median
    .head(10)["SA22026_code"]
)

plot_data = gap_data[
    gap_data["SA22026_code"].isin(top_locations)
].copy()

location_order = (
    location_gap_median[
        location_gap_median["SA22026_code"]
        .isin(top_locations)
    ]
    .sort_values("median")
    ["SA22026_name"]
    .tolist()
)

plot_data["SA22026_name"] = pd.Categorical(
    plot_data["SA22026_name"],
    categories=location_order,
    ordered=True
)

plot_box_plot(
    plot_data,
    "price_gap",
    "SA22026_name",
    False,
    (10, 7),
    "Distribution of Airbnb Price Gaps for Top 10 Locations",
    "",
    "Price Gap ($ per night)",
    "Christchurch Location",
    DATA_FIG+"Distribution of Airbnb Price Gaps for Top 10 Locations"
)

airbnb_counts = (
    airbnb
    .groupby(
        ["SA22026_code", "SA22026_name"]
    )["id"]
    .nunique()
    .reset_index(
        name="Airbnb_Count"
    )
)

latest_quarter = bonds_all["quarter"].max()

rental_counts = (
    bonds_all[
        bonds_all["quarter"] == latest_quarter
    ][
        [
            "SA22026_code",
            "Total Bonds"
        ]
    ]
    .rename(
        columns={
            "Total Bonds": "Rental_Count"
        }
    )
)

location_counts = airbnb_counts.merge(
    rental_counts,
    on="SA22026_code",
    how="left"
)

location_counts["Rental_Count"] = (
    location_counts["Rental_Count"]
    .fillna(0)
)

location_counts["Airbnb_to_Rental_Ratio"] = (
    location_counts["Airbnb_Count"] /
    location_counts["Rental_Count"].replace(0, pd.NA)
)

location_counts = location_counts.sort_values(
    "Airbnb_Count",
    ascending=False
)

log()
log("Airbnb vs Rental Properties:")

log(
    location_counts
    .head(20)
    .to_string(index=False)
)

merged.to_csv(
    JOINED_PATH,
    index=False
)

log()
log("Saved: airbnb_bonds_merged.csv")