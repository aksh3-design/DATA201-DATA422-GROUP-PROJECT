import pandas as pd
import matplotlib.pyplot as plt

# Load the combined Christchurch dataset
df = pd.read_csv("listings_combined.csv")

# Highest number of reviews for each month
highest = df.groupby("month_year")["number_of_reviews"].max()

# Top 10% cutoff for each month
cutoff = df.groupby("month_year")["number_of_reviews"].quantile(0.90)

# Print results
print("Highest reviews:")
print(highest)

print("\nTop 10% cutoff:")
print(cutoff)


# LINE CHART - HIGHEST REVIEWS
highest.plot(marker="o")

plt.xlabel("Month")
plt.ylabel("Highest Number of Reviews")
plt.title("Highest Number of Reviews in Christchurch")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# BAR CHART - HIGHEST REVIEWS
highest.plot(kind="bar")

plt.xlabel("Month")
plt.ylabel("Highest Number of Reviews")
plt.title("Highest Number of Reviews in Christchurch")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# LINE CHART - TOP 10% CUTOFF
cutoff.plot(marker="o")

plt.xlabel("Month")
plt.ylabel("Number of Reviews")
plt.title("Top 10% Review Cutoff in Christchurch")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# BAR CHART - TOP 10% CUTOFF
cutoff.plot(kind="bar")

plt.xlabel("Month")
plt.ylabel("Number of Reviews")
plt.title("Top 10% Review Cutoff in Christchurch")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()