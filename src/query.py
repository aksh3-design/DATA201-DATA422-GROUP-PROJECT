import pandas as pd
from pandarallel import pandarallel
import time

from src.lib.schema.listings.dtypes import dtypes, na_values

PROCESSES = 8
CHUNKSIZE = 2
    
def process_apply(x:pd.Series):

    from config import API_KEY
    from src.lib.koord_get import VectorResponse

    LAYER = 123515
    RADIUS = 200
    MAX_RESULT = 1
    GEOMETRY = "false"

    # ["id","neighbourhood","latitude","longitude","room_type","price","minimum_nights","number_of_reviews","calculated_host_listings_count","availability_365","number_of_reviews_ltm","month_year"] # do some stuff to data here

    longitude = x["longitude"]
    latitude = x["latitude"]

    query_obj = VectorResponse(API_KEY, LAYER, MAX_RESULT, RADIUS, GEOMETRY)
    url = query_obj.get_url(longitude, latitude)
    query_obj.query(url)

    match query_obj.status:
        case 1: # Good
            pass
        case 0: # Bad -> see koord_get.py
            pass
            return x
        case _: # should never occur
            print(f"WARNING Uknown VectorResponse Status Code: {query_obj.status}")
            return x
    
    x["SA22026_name"] = query_obj.get_name()
    x["SA22026_code"] = query_obj.get_code()

    return x

def process(df):
    df = df.apply(process_apply, axis=1)
    return df

def split_dataframe(df, chunk_size = 10000): 
    chunks = list()
    num_chunks = len(df) // chunk_size + 1
    for i in range(num_chunks):
        chunks.append(df[i*chunk_size:(i+1)*chunk_size])
    return chunks

def main():

    from config import LISTINGS_CLEANED_PATH, LISTINGS_SA22026_PATH
    
    # load dataset
    
    print(LISTINGS_CLEANED_PATH)

    data = pd.read_csv(LISTINGS_CLEANED_PATH, dtype=dtypes, na_values=na_values)
    data["SA22026_code"] = 0
    data["SA22026_name"] = ""
    
    data.astype({
        "SA22026_code" : int,
        "SA22026_name" : str
     })

    pandarallel.initialize(progress_bar=True)

    start_time = time.perf_counter()
    data:pd.DataFrame = data.parallel_apply(process_apply, axis=1)
    end_time = time.perf_counter()

    data.drop(columns=["latitude","longitude"], inplace=True)

    data.to_csv(LISTINGS_SA22026_PATH, index=False)

    data = pd.read_csv(LISTINGS_SA22026_PATH, dtype=dtypes, na_values=na_values, index_col=False)    

    minutes = (end_time - start_time) // 60
    seconds = (end_time - start_time) % 60

    print(f"\n\n{int(minutes)} minutes, {int(seconds)} seconds ...")

if __name__ == "__main__":

    main()
    pass

