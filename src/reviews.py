import pandas as pd

from config import LISTINGS_COMBINED_PATH, DATA_FIG, DATA_OUT
from lib.plots import plot_bar, plot_line
from lib.log import print_bordered, log
from lib.schema.listings.dtypes import dtypes, na_values

# TODO: integrate statistics summary

def get_monthly_results(data:pd.DataFrame):
    """Returns a list of dictionaries.

    Each dictionary records specific statistics on airbnb listings for each month in the
    combined dataset.

    - Month.
    - Number of unique listings.
    - Top 10 percent of listings by number of reviews.
    - Number of listings in the top 10 percent of listings by number of reviews.
    - Listings with the highest number of reviews.
    - name, neighbourhood, and room_type of the top listing.

    Args:
        data (pd.DataFrame): Combined listings dataset.

    Returns:
        list[dict[]]: monthly results.
    """

    monthly_results = []

    for month in sorted(data["month_year"].unique()): # Select data for one month

        month_data = data[data["month_year"] == month].copy()
        month_data = month_data.drop_duplicates(subset="id") # Remove duplicate property IDs within that month
        
        number_properties = len(month_data) # Number of unique properties
        highest_reviews = month_data["number_of_reviews"].max() # Highest number of reviews

        highest_property = month_data[ # Find the property with the highest number of reviews
            month_data["number_of_reviews"] == highest_reviews
        ].iloc[0]
    
        top_10_cutoff = month_data["number_of_reviews"].quantile(0.90) # Calculate the 90th percentile

        top_10 = month_data[ # Find properties in the top 10%
            month_data["number_of_reviews"] >= top_10_cutoff
        ]
    
        # Store the results
        monthly_results.append({
            "month": month,
            "unique_properties": number_properties,
            "top_10_cutoff": top_10_cutoff,
            "top_10_properties": len(top_10),
            "highest_reviews": highest_reviews,
            "highest_property": highest_property["name"],
            "neighbourhood": highest_property["neighbourhood"],
            "room_type": highest_property["room_type"]
        })

    return monthly_results


if __name__ == "__main__":

    # 1. LOAD THE COMBINED CHRISTCHURCH DATASET

    data = pd.read_csv(LISTINGS_COMBINED_PATH, dtype=dtypes, na_values=na_values)
    log(f"Dataset loaded successfully.\nTotal records: {len(data)}")

    # 3. ANALYSE HIGHEST REVIEWS FOR EACH MONTH
    # 4. CREATE A RESULTS TABLE    
    # 5. SAVE THE MONTHLY RESULTS

    monthly_results = get_monthly_results(data)
    results = pd.DataFrame(monthly_results)
    results.to_csv(DATA_OUT+"highest_reviews_monthly_results.csv", index=False)

    print_bordered("MONTHLY HIGHEST REVIEW RESULTS")
    log(results.to_string(index=False))
    log(f"\nMonthly results saved to: {DATA_OUT}highest_reviews_monthly_results.csv")

    plot_line( # 6. PLOT HIGHEST NUMBER OF REVIEWS BY MONTH
        results["month"],
        results["highest_reviews"],
        "Month",
        "Highest Number of Reviews",
        "Highest Number of Airbnb Reviews in Christchurch\nOctober 2025 to August 2026",
        save_path=DATA_FIG+"highest_number_of_airbnb_reviews_in_christchurch"
        )    

    plot_line( # 7. PLOT TOP 10% REVIEW CUTOFF BY MONTH
        results["month"],
        results["top_10_cutoff"],
        "Month",
        "Top 10% Review Cutoff",
        "Top 10% Number of Reviews Cutoff in Christchurch\nOctober 2025 to August 2026",
        save_path=DATA_FIG+"top_10_percent_number_of_reviews_cutoff_in_christchurch"
        )

        # 8.GET THE LATEST MONTH AUTOMATICALLY

    latest_month = sorted(data["month_year"].unique())[-1]
    latest_data = data[data["month_year"] == latest_month].copy()

    latest_date = pd.to_datetime(latest_month)
    latest_label = latest_date.strftime("%B %Y")

    columns = ["id", "name", "number_of_reviews", "neighbourhood", "room_type"]

    print_bordered(f"{latest_label.upper()} RESULTS")
    log(
        f"{latest_label} records: {len(latest_data)}\n"
        f"Unique {latest_label} properties: {latest_data['id'].nunique()}"
    )

    # 9. FIND HIGHEST REVIEWED PROPERTY IN LATEST MONTH

    highest_reviews = latest_data["number_of_reviews"].max()

    highest_property = latest_data[
        latest_data["number_of_reviews"] == highest_reviews
    ]

    log(
        f"\nHighest number of reviews in {latest_label}:\n"
        f"{highest_reviews}\n"
        f"Highest reviewed property in {latest_label}:"
    )

    log(highest_property[columns].to_string(index=False))

    # 10. FIND LATEST MONTH TOP 10%

    latest_cutoff = latest_data["number_of_reviews"].quantile(0.90)

    latest_top_10 = latest_data[
        latest_data["number_of_reviews"] >= latest_cutoff
    ]

    log(f"\n{latest_label} top 10% cutoff: {latest_cutoff}")
    log(
        f"\nNumber of properties in {latest_label} top 10%: "
        f"{len(latest_top_10)}"
    )

    # 11. FIND TOP 20 PROPERTIES IN LATEST MONTH

    top_20 = (
        latest_data[columns]
        .sort_values("number_of_reviews", ascending=False)
        .head(20)
    )

    print_bordered(f"TOP 20 PROPERTIES - {latest_label.upper()}")
    log(top_20)

    # 12. PLOT TOP 20 PROPERTIES

    plot_bar(
        top_20["name"],
        top_20["number_of_reviews"],
        "Number of Reviews",
        "Property",
        f"Top 20 Christchurch Airbnb Properties by Number of Reviews\n{latest_label}",
        xticks_rotation=0,
        figsize=(10, 8),
        save_path=DATA_FIG+"top_20_christchurch_airbnb_properties"
    )
    # 13. BAR CHART - HIGHEST REVIEWS BY MONTH

    plot_bar(
        results["month"],
        results["highest_reviews"],
        "Highest Number of Reviews",
        "Month",
        "Highest Number of Airbnb Reviews in Christchurch\nOctober 2025 to August 2026",
        figsize=(10, 6),
        save_path=DATA_FIG+"highest_reviews_by_month_bar"
    )
