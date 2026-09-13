"""
Deliverable 5
"""
from src.main.lib.schema.listings.schema import schema
from src.main.get_listings import load_csv
from src.main.lib.statistics.summary_statistics import SummaryStatistics
import pandas as pd
import matplotlib.pyplot as plt

combined = load_csv("listings_combined.csv")

schema.validate(combined) # All validated

# Generate plots

def generate_plots():

    # =====================================================
    # 1. LOAD THE COMBINED CHRISTCHURCH DATASET
    # =====================================================

    print("Dataset loaded successfully.")
    print("Total records:", len(combined))

    # =====================================================
    # 2. CHECK THE MONTHS IN THE DATASET
    # =====================================================

    print("\nMonths in dataset:")
    print(sorted(combined["month_year"].unique()))

    # =====================================================
    # 3. ANALYSE HIGHEST REVIEWS FOR EACH MONTH
    # =====================================================

    monthly_results = []

    for month in sorted(combined["month_year"].unique()):

        # Select data for one month
        month_data = combined[combined["month_year"] == month].copy()

        # Remove duplicate property IDs within that month
        month_data = month_data.drop_duplicates(subset="id")

        # Number of unique properties
        number_properties = len(month_data)

        # Highest number of reviews
        highest_reviews = month_data["number_of_reviews"].max()

        # Find the property with the highest number of reviews
        highest_property = month_data[
            month_data["number_of_reviews"] == highest_reviews
        ].iloc[0]

        # Calculate the 90th percentile
        top_10_cutoff = month_data["number_of_reviews"].quantile(0.90)

        # Find properties in the top 10%
        top_10 = month_data[
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

    # =====================================================
    # 4. CREATE A RESULTS TABLE
    # =====================================================

    results = pd.DataFrame(monthly_results)

    print("\n========================================")
    print("MONTHLY HIGHEST REVIEW RESULTS")
    print("========================================\n")

    print(results.to_string(index=False))

    # =====================================================
    # 5. SAVE THE MONTHLY RESULTS
    # =====================================================

    results.to_csv(
        "highest_reviews_monthly_results.csv",
        index=False
    )

    print("\nMonthly results saved as:")
    print("highest_reviews_monthly_results.csv")

    # =====================================================
    # 6. PLOT HIGHEST NUMBER OF REVIEWS BY MONTH
    # =====================================================

    plt.figure(figsize=(10, 6))

    plt.plot(
        results["month"],
        results["highest_reviews"],
        marker="o"
    )

    plt.xlabel("Month")
    plt.ylabel("Highest Number of Reviews")

    plt.title(
        "Highest Number of Airbnb Reviews in Christchurch\n"
        "October 2025 to June 2026"
    )

    plt.xticks(rotation=45)

    plt.tight_layout()

    plt.show()

    # =====================================================
    # 7. PLOT TOP 10% REVIEW CUTOFF BY MONTH
    # =====================================================

    plt.figure(figsize=(10, 6))

    plt.plot(
        results["month"],
        results["top_10_cutoff"],
        marker="o"
    )

    plt.xlabel("Month")
    plt.ylabel("Top 10% Review Cutoff")

    plt.title(
        "Top 10% Number of Reviews Cutoff in Christchurch\n"
        "October 2025 to June 2026"
    )

    plt.xticks(rotation=45)

    plt.tight_layout()

    plt.show()

    # =====================================================
    # 8. GET THE LATEST MONTH - JUNE 2026
    # =====================================================

    june = combined[combined["month_year"] == "2026-06"].copy()

    # Remove duplicate property IDs
    june_unique = june.drop_duplicates(subset="id")

    print("\n========================================")
    print("JUNE 2026 RESULTS")
    print("========================================")

    print("June records:", len(june))
    print("Unique June properties:", len(june_unique))

    # =====================================================
    # 9. FIND HIGHEST REVIEWED PROPERTY IN JUNE
    # =====================================================

    highest_reviews_june = june_unique["number_of_reviews"].max()

    highest_property_june = june_unique[
        june_unique["number_of_reviews"] == highest_reviews_june
    ]

    print("\nHighest number of reviews in June:")
    print(highest_reviews_june)

    print("\nHighest reviewed property in June:")

    print(
        highest_property_june[
            [
                "id",
                "name",
                "number_of_reviews",
                "neighbourhood",
                "room_type"
            ]
        ].to_string(index=False)
    )

    # =====================================================
    # 10. FIND JUNE TOP 10%
    # =====================================================

    june_cutoff = june_unique[
        "number_of_reviews"
    ].quantile(0.90)

    june_top_10 = june_unique[
        june_unique["number_of_reviews"] >= june_cutoff
    ]

    print("\nJune top 10% cutoff:")
    print(june_cutoff)

    print("\nNumber of properties in June top 10%:")
    print(len(june_top_10))

    # =====================================================
    # 11. FIND TOP 20 JUNE PROPERTIES
    # =====================================================

    top_20 = june_unique[
        [
            "id",
            "name",
            "number_of_reviews",
            "neighbourhood",
            "room_type"
        ]
    ].sort_values(
        "number_of_reviews",
        ascending=False
    ).head(20)

    print("\n========================================")
    print("TOP 20 PROPERTIES - JUNE 2026")
    print("========================================\n")

    print(top_20.to_string(index=False))

    # =====================================================
    # 12. PLOT TOP 20 JUNE PROPERTIES
    # =====================================================

    plt.figure(figsize=(10, 8))

    plt.barh(
        top_20["name"],
        top_20["number_of_reviews"]
    )

    plt.xlabel("Number of Reviews")
    plt.ylabel("Property")

    plt.title(
        "Top 20 Christchurch Airbnb Properties "
        "by Number of Reviews - June 2026"
    )

    plt.gca().invert_yaxis()

    plt.tight_layout()

    plt.show()

    # =====================================================
    # 13. BAR CHART - HIGHEST REVIEWS BY MONTH
    # =====================================================

    plt.figure(figsize=(10, 6))

    plt.bar(
        results["month"],
        results["highest_reviews"]
    )

    plt.xlabel("Month")
    plt.ylabel("Highest Number of Reviews")

    plt.title(
        "Highest Number of Airbnb Reviews in Christchurch\n"
        "October 2025 to June 2026"
    )

    plt.xticks(rotation=45)

    plt.tight_layout()

    plt.show()

generate_plots()
# Generate Summary Statistics

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
