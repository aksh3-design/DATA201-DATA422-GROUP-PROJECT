
import pandas as pd
import matplotlib.pyplot as plt

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

combined = pd.concat(
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

combined["last_review"] = pd.to_datetime(
    combined["last_review"],
    dayfirst=True,
    errors="coerce"
)

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