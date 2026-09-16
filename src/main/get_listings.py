from src.main.lib.schema.listings.dtypes import dtypes, na_values
import pandas as pd

def load_csv(filename:str):
    """loads csv to spec"""
    
    df = pd.read_csv(
        filepath_or_buffer=filename,
        dtype=dtypes,
        na_values=na_values
    )
    
    df["neighbourhood"] = df["neighbourhood"].astype("category")
    
    df["last_review"] = pd.to_datetime(df["last_review"], format="mixed", dayfirst=True, errors="coerce")
    
    df["month_year"] = pd.to_datetime(df["month_year"], format="ISO8601")
    
    return df