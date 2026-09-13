"""
Deliverable 5
"""
from src.main.lib.schema.data_schema import schema
from src.main.lib.schema.load_csv import load_csv
from src.main.summary_statistics import SummaryStatistics
import pandas as pd
import matplotlib.pyplot as plt

# combined = load_csv("listings_combined.csv") # load to spec

def cncat_csv():
    #%%

    df_oct = pd.read_csv("listings_oct.csv")
    df_oct = df_oct[df_oct["neighbourhood_group"].str.contains(
        "Christchurch City", case=False, na=False
    )]
    df_oct["month_year"] = "2025-10-01"

    #%%

    df_nov = pd.read_csv("listings_nov.csv")
    df_nov = df_nov[df_nov["neighbourhood_group"].str.contains(
        "Christchurch City", case=False, na=False
    )]
    df_nov["month_year"] = "2025-11-01"

    #%%

    df_dec = pd.read_csv("listings_dec.csv")
    df_dec = df_dec[df_dec["neighbourhood_group"].str.contains(
        "Christchurch City", case=False, na=False
    )]
    df_dec["month_year"] = "2025-12-01"

    #%%

    df_jan = pd.read_csv("listings_jan.csv")
    df_jan = df_jan[df_jan["neighbourhood_group"].str.contains(
        "Christchurch City", case=False, na=False
    )]
    df_jan["month_year"] = "2026-01-01"

    #%%

    df_feb = pd.read_csv("listings_feb.csv")
    df_feb = df_feb[df_feb["neighbourhood_group"].str.contains(
        "Christchurch City", case=False, na=False
    )]
    df_feb["month_year"] = "2026-02-01"

    #%%

    df_mar = pd.read_csv("listings_mar.csv")
    df_mar = df_mar[df_mar["neighbourhood_group"].str.contains(
        "Christchurch City", case=False, na=False
    )]
    df_mar["month_year"] = "2026-03-01"

    #%%

    df_apr = pd.read_csv("listings_apr.csv")
    df_apr = df_apr[df_apr["neighbourhood_group"].str.contains(
        "Christchurch City", case=False, na=False
    )]
    df_apr["month_year"] = "2026-04-01"

    #%%

    df_may = pd.read_csv("listings_may.csv")
    df_may = df_may[df_may["neighbourhood_group"].str.contains(
        "Christchurch City", case=False, na=False
    )]
    df_may["month_year"] = "2026-05-01"

    #%%

    df_jun = pd.read_csv("listings_jun.csv")
    df_jun = df_jun[df_jun["neighbourhood_group"].str.contains(
        "Christchurch City", case=False, na=False
    )]
    df_jun["month_year"] = "2026-06-01"
    
    
    #%%

    return pd.concat(
        [
            df_oct, df_nov, df_dec,
            df_jan, df_feb, df_mar,
            df_apr, df_may, df_jun
        ],
        ignore_index=True
    )

    print(combined.shape)
    print(combined["month_year"].value_counts())

    #%%

combined = cncat_csv()

schema.validate(combined) # All validated

# Generate plots

def generate_plots():

    # AKSH CODE
    
    pass
    
    # Generate Summary Statistics

def summary_stats():

    stats = SummaryStatistics(combined)

    # print(stats.category_stats("neighbourhood"))

    line = "="*50

    for key, value in stats.all_category_stats().items():
        print(key)
        print(value)
        print(line)

    for key, value in stats.all_numerical_stats().items():
        print(key)
        print(value)
        print(line)

    # for key, value in stats.all_string_stats().items(): #NOTE: There are thousands of individual names, blanket stats for all string columns are not a great idea.
    #     print(key)
    #     print(value)
    #     print(line)

    for key, value in stats.all_datetime_stats().items():
        print(key)
        print(value)
        print(line)

# Calculate days since last review

def days_since_last_review():
    
    published_date = pd.Timestamp("2026-06-19")

    combined["days_since_review"] = (
        published_date - combined["last_review"]
    ).dt.days

    #%%
    bins = list(range(0, 1001, 30)) + [float("inf")]

    counts = pd.cut(
        combined["days_since_review"],
        bins=bins,
        right=False
    ).value_counts().sort_index()

    plt.figure(figsize=(12, 6))

    plt.bar(
        range(len(counts)),
        counts.values
    )

    plt.xlabel("Days since last review")
    plt.ylabel("Number of listings")
    plt.title("Distribution of Days Since Last Review")

    tick_positions = range(0, len(counts), 3)

    tick_labels = [
        f"{i*30}–{min(i*30+90, 1000)}"
        for i in tick_positions
    ]

    plt.xticks(tick_positions, tick_labels)

    plt.tight_layout()
    plt.show()


    #%%
    # Highest number of reviews for each month

    highest = combined.groupby("month_year")["number_of_reviews"].max()

    # Top 10% cutoff for each month

    cutoff = combined.groupby("month_year")["number_of_reviews"].quantile(0.90)

    # Print results

    print("Highest reviews:")
    print(highest)

    print("\nTop 10% cutoff:")
    print(cutoff)


    #%%
    # LINE CHART - HIGHEST REVIEWS

    highest.plot(marker="o")

    plt.xlabel("Month")
    plt.ylabel("Highest Number of Reviews")
    plt.title("Highest Number of Reviews in Christchurch")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


    #%%
    # BAR CHART - HIGHEST REVIEWS

    highest.plot(kind="bar")

    plt.xlabel("Month")
    plt.ylabel("Highest Number of Reviews")
    plt.title("Highest Number of Reviews in Christchurch")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


    #%%
    # LINE CHART - TOP 10% CUTOFF

    cutoff.plot(marker="o")

    plt.xlabel("Month")
    plt.ylabel("Number of Reviews")
    plt.title("Top 10% Review Cutoff in Christchurch")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


    #%%
    # BAR CHART - TOP 10% CUTOFF

    cutoff.plot(kind="bar")

    plt.xlabel("Month")
    plt.ylabel("Number of Reviews")
    plt.title("Top 10% Review Cutoff in Christchurch")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
    pass
    
# Distributions

def price_distributions():
    
    # KOUSHI DISTRRIBUTIONS
    
    pass
    
if __name__ == "__main__":
    
    generate_plots()
    summary_stats()
    days_since_last_review()
    price_distributions()