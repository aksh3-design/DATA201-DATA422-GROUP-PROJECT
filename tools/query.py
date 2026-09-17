import requests
import json
import pandas as pd
import numpy as np
import multiprocessing as mp

import multiprocessing as mp
import pandas.util.testing as pdt

def default_query(key:str, layer:int, x:float, y:float, max_results:int=3, radius:int=10000, geometry="true", with_field_names="true"):
    
    return f"https://koordinates.com/services/query/v1/vector.json?key={key}&layer={layer}&x={x}&y={y}&max_results={max_results}&radius={radius}&geometry={geometry}&with_field_names={with_field_names}"

def get_code(data:requests.Response):
    
    datajson = data.json()
    
    return datajson["vectorQuery"]["layers"]["123515"]["features"][0]["properties"]["SA22026_V1_00"]

def get_name(data:requests.Response):

    datajson = data.json()
    
    return datajson["vectorQuery"]["layers"]["123515"]["features"][0]["properties"]["SA22026_V1_00_NAME"]

def process_apply(x):
    # do some stuff to data here
    pass

def process(df):
    res = df.apply(process_apply, axis=1)
    return res
    
if __name__ == "__main__":
    
    # key = input("key")
    
    # p = mp.Pool(processes=8)
    # split_dfs = np.array_split(big_df,8)
    # pool_results = p.map(aoi_proc, split_dfs)
    # p.close()
    # p.join()

    # # merging parts processed by different processes
    # parts = pd.concat(pool_results, axis=0)

    # # merging newly calculated parts to big_df
    # big_df = pd.concat([big_df, parts], axis=1)

    # # checking if the dfs were merged correctly
    # pdt.assert_series_equal(parts['id'], big_df['id'])
    
    pass