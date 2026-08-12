"""
Deliverable 5
"""
from src.main.lib.schema.data_schema import schema
from src.main.lib.schema.load_csv import load_csv
from src.main.summary_statistics import SummaryStatistics
import pandas as pd
import matplotlib.pyplot as plt

combined = load_csv("listings_combined.csv") # load to spec

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
    
    # SOPH1E CODE
    
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