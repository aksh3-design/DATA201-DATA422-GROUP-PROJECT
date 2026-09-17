import multiprocessing as mp
import pandas as pd
import tqdm
import time

import pandas.testing as pdt

if __name__ == "__main__":
    # Use a context manager to manage the pool and collect results explicitly
    
    infile = pd.read_csv("cleaned_listing_data.csv")
    outfile = pd.read_csv("out.csv")

    pdt.assert_series_equal(infile["id"], outfile["id"])