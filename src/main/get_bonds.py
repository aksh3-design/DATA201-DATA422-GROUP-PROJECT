from src.main.lib.schema.bonds.dtypes import dtypes, na_values
import pandas as pd

def load_csv(filename:str):
    """loads csv to spec"""
    
    df = pd.read_csv(
        filepath_or_buffer=filename,
        dtype=dtypes,
        na_values=na_values
    )
    
    return df
