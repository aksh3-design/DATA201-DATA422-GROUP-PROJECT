import pandas as pd
import matplotlib.pyplot as plt

from config import AIRBNB_RAW, DATA_OUT_PATH, REVIEWS_RESULTS, REVIEWS_NUMBER, REVIEWS_TOPTEN, REVIEWS_TOPTWENTY, REVIEWS_HIGHEST 
from lib.log import print_bordered

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

def plot_line(
        scalex:pd.DataFrame, 
        scaley:pd.DataFrame, 
        xlabel:str, 
        ylabel:str, 
        title:str, 
        show:bool=True, 
        save:bool=True, 
        save_path:str="",
        figsize:tuple[int, int]=(10, 6), 
        xticks_rotation:int=45, 
        marker:str='o'
        ):

    plt.figure(figsize=figsize)
    plt.plot(scalex, scaley, marker=marker)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.xticks(rotation=xticks_rotation)
    plt.tight_layout()
    if save: plt.savefig(save_path)
    if show: plt.show()

def plot_bar(
        y,
        width,
        xlabel:str,
        ylabel:str,
        title:str,
        figsize:tuple[int, int],
        show:bool=True,
        save:bool=True,
        save_path:str="",
        xticks_rotation:int=45
        ):
    plt.figure(figsize=figsize)
    plt.barh(y, width)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.xticks(rotation=xticks_rotation)
    plt.tight_layout()
    if save: plt.savefig(save_path)
    if show: plt.show()

if __name__ == "__main__":

    # 1. LOAD THE COMBINED CHRISTCHURCH DATASET

    data = AIRBNB_RAW
    print(f"Dataset loaded successfully.\nTotal records: {len(data)}")

    # 3. ANALYSE HIGHEST REVIEWS FOR EACH MONTH
    # 4. CREATE A RESULTS TABLE    
    # 5. SAVE THE MONTHLY RESULTS

    monthly_results = get_monthly_results(data)
    results = pd.DataFrame(monthly_results)
    results.to_csv(DATA_OUT_PATH+REVIEWS_RESULTS, index=False)

    print_bordered("MONTHLY HIGHEST REVIEW RESULTS")
    print(results.to_string(index=False))
    print(f"\nMonthly results saved to: {DATA_OUT_PATH+REVIEWS_RESULTS}")

    plot_line( # 6. PLOT HIGHEST NUMBER OF REVIEWS BY MONTH
        results["month"],
        results["highest_reviews"],
        "Month",
        "Highest Number of Reviews",
        "Highest Number of Airbnb Reviews in Christchurch\nOctober 2025 to June 2026",
        save_path=DATA_OUT_PATH+REVIEWS_NUMBER
        )    

    plot_line( # 7. PLOT TOP 10% REVIEW CUTOFF BY MONTH
        results["month"],
        results["top_10_cutoff"],
        "Month",
        "Top 10% Review Cutoff",
        "Top 10% Number of Reviews Cutoff in Christchurch\nOctober 2025 to June 2026",
        save_path=DATA_OUT_PATH+REVIEWS_TOPTEN
        )

    # 8. GET THE LATEST MONTH - JUNE 2026
    
    june = data[data["month_year"] == "2026-06-01"].copy()

    columns = [ "id", "name", "number_of_reviews", "neighbourhood", "room_type"]

    print_bordered("JUNE 2026 RESULTS")
    print(f"June records: {len(june)}\nUnique June properties: {len(june)}")

    # 9. FIND HIGHEST REVIEWED PROPERTY IN JUNE
    
    highest_reviews_june = june["number_of_reviews"].max()
    highest_property_june = june[june["number_of_reviews"] == highest_reviews_june]
    
    print(f"\nHighest number of reviews in June:\n{highest_reviews_june}\nHighest reviewed property in June:")
    print(highest_property_june[columns].to_string(index=False))

    # 10. FIND JUNE TOP 10%
    
    june_cutoff = june["number_of_reviews"].quantile(0.90)
    june_top_10 = june[june["number_of_reviews"] >= june_cutoff]
    
    print(f"\nJune top 10% cutoff: {june_cutoff}")
    print(f"\nNumber of properties in June top 10%: {len(june_top_10)}")

    # 11. FIND TOP 20 JUNE PROPERTIES
    
    top_20 = june[columns].sort_values("number_of_reviews",ascending=False).head(20)

    print_bordered("TOP 20 PROPERTIES - JUNE 2026")
    print(top_20.to_string(index=False))

    plot_bar( # 12. PLOT TOP 20 JUNE PROPERTIES
        top_20["name"],
        top_20["number_of_reviews"],
        "Number of Reviews",
        "Property",
        "Top 20 Christchurch Airbnb Properties by Number of Reviews\nJune 2026",
        xticks_rotation=0,
        figsize=(10, 8),
        save_path=DATA_OUT_PATH+REVIEWS_TOPTWENTY
        )

    plot_bar( # 13. BAR CHART - HIGHEST REVIEWS BY MONTH
        results["month"],
        results["highest_reviews"],
        "Highest Number of Reviews",
        "Month",
        "Highest Number of Airbnb Reviews in Christchurch\nOctober 2025 to June 2026",
        figsize=(10, 6),
        save_path=DATA_OUT_PATH+REVIEWS_HIGHEST
    )