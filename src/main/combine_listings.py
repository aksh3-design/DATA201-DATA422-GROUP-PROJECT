from src.main.lib.load.csvconcatenator import CSVConcatenator
import pandas as pd

LISTING_DIRECTORY = "C:/Users/Rehutai/OneDrive - University of Canterbury/DATA201-DATA422-GROUP-PROJECT/datasets/listings"

from src.main.lib.schema.listings.dtypes import dtypes, na_values

data = CSVConcatenator(dtypes, na_values)

data.load_csv(f"{LISTING_DIRECTORY}/listings_oct.csv").filter_rows("neighbourhood_group", "Christchurch City").add_column("month_year", "2025-10-01").create()

data.load_csv(f"{LISTING_DIRECTORY}/listings_nov.csv").filter_rows("neighbourhood_group", "Christchurch City").add_column("month_year", "2025-11-01").create()

data.load_csv(f"{LISTING_DIRECTORY}/listings_dec.csv").filter_rows("neighbourhood_group", "Christchurch City").add_column("month_year", "2025-12-01").create()

data.load_csv(f"{LISTING_DIRECTORY}/listings_jan.csv").filter_rows("neighbourhood_group", "Christchurch City").add_column("month_year", "2026-01-01").create()

data.load_csv(f"{LISTING_DIRECTORY}/listings_feb.csv").filter_rows("neighbourhood_group", "Christchurch City").add_column("month_year", "2026-02-01").create()

data.load_csv(f"{LISTING_DIRECTORY}/listings_mar.csv").filter_rows("neighbourhood_group", "Christchurch City").add_column("month_year", "2026-03-01").create()

data.load_csv(f"{LISTING_DIRECTORY}/listings_apr.csv").filter_rows("neighbourhood_group", "Christchurch City").add_column("month_year", "2026-04-01").create()

data.load_csv(f"{LISTING_DIRECTORY}/listings_may.csv").filter_rows("neighbourhood_group", "Christchurch City").add_column("month_year", "2026-05-01").create()

data.load_csv(f"{LISTING_DIRECTORY}/listings_jun.csv").filter_rows("neighbourhood_group", "Christchurch City").add_column("month_year", "2026-06-01").create()

combined = data.concatenate()
# print(combined.shape)
# print(combined["month_year"].value_counts())

combined.to_csv("listings_combined.csv")