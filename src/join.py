import pandas as pd
import matplotlib.pyplot as plt

airbnb = pd.read_csv("data/out_2.csv")
bonds = pd.read_csv("out/Detailed-Quarterly-Tenancy-Q1-2020-Q3-2026.csv")

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
        "Geometric Mean Rent",
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

print("Airbnb rows:", len(airbnb))
print("Merged rows:", len(merged))

print()
print(
    "Missing Geometric Mean Rent price:",
    merged["Geometric Mean Rent"].isna().sum()
)

print()
print("Example Christchurch Central:")

print(
    merged[
        merged["SA22026_code"] == 326600
    ][
        [
            "month_year",
            "SA22026_code",
            "SA22026_name",
            "price",
            "Geometric Mean Rent",
            "Total Bonds"
        ]
    ].head(10).to_string(index=False)
)

central = merged[
    merged["SA22026_code"] == 326600
]

median_price = central["price"].median()

print()
print("Christchurch Central")
print("Number of observations:", len(central))
print("Median Airbnb price: $", median_price)

merged["long_term_nightly"] = (
    merged["Geometric Mean Rent"] / 7
)

merged["price_gap"] = (
    merged["price"] -
    merged["long_term_nightly"]
)

gap_data = merged.dropna(
    subset=["price_gap"]
).copy()

print()
print(
    "Number of Airbnb observations with rental data:",
    len(gap_data)
)

print()
print("Example price gaps:")

print(
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

print()
print("Locations with the largest median price gaps:")

print(
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

plot_data.boxplot(
    column="price_gap",
    by="SA22026_name",
    vert=False,
    figsize=(10, 7)
)

plt.title(
    "Distribution of Airbnb Price Gaps for Top 10 Locations"
)

plt.suptitle("")

plt.xlabel(
    "Price Gap ($ per night)"
)

plt.ylabel(
    "Christchurch Location"
)

plt.tight_layout()

plt.savefig("out/Distribution of Airbnb Price Gaps for Top 10 Locations")

plt.show()

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

print()
print("Airbnb vs Rental Properties:")

print(
    location_counts
    .head(20)
    .to_string(index=False)
)

merged.to_csv(
    "out/airbnb_bonds_merged.csv",
    index=False
)

print()
print("Saved: airbnb_bonds_merged.csv")