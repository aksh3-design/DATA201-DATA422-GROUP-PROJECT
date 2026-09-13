import pandas as pd
import numpy as np

        
def load_csv(filename:str, dtypes, na_values):
    """loads csv to spec"""
    
    df = pd.read_csv(
        filepath_or_buffer=filename,
        dtype=dtypes,
        na_values=na_values
    )
    
    df["neighbourhood"] = df["neighbourhood"].astype("category")
    
    df["last_review"] = pd.to_datetime(df["last_review"], format="ISO8601")
    
    df["month_year"] = pd.to_datetime(df["month_year"], format="ISO8601")
    
    return df