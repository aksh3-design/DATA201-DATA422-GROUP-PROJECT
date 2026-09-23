import pandas as pd
from pandarallel import pandarallel
import time

from src.lib.schema.listings.dtypes import dtypes, na_values

PROCESSES = 8
CHUNKSIZE = 2
    
def process_apply(x:pd.Series):

    from config import API_KEY  
    from typing import Literal, Self
    import requests
    import json

    LAYER = 123515
    RADIUS = 200
    MAX_RESULT = 1
    GEOMETRY = "false"

    class VectorResponse():
    
        def __init__(self, key:str, layer:int, max_results:int=3, radius:int=10000, geometry:Literal["true", "false"]="true", with_field_names:Literal["true", "false"]="true"):
    
            self.key:str = key
            self.layer:int = layer
            self.max_results:int = max_results
            self.radius:int = radius        
            self.geometry:str = geometry
            self.with_field_names:str = with_field_names
    
            self.response:requests.Response = None
            self.status:Literal[1, 0, -1] = -1 # Null Status, 1 is a success
    
        def get_url(self, longitude:float, latitude:float):            
            return f"https://koordinates.com/services/query/v1/vector.json?key={self.key}&layer={self.layer}&x={longitude}&y={latitude}&max_results={self.max_results}&radius={self.radius}&geometry={self.geometry}&with_field_names={self.with_field_names}"
    
        def query(self, url:str, max_attempts:int=4):
    
            if not self.response is None:
                return self 
    
            attempts = 0
    
            while self.response is None:
    
                response:requests.Response = requests.get(url)
    
                match response.status_code:
                    case 200:
                        self.status = 1
                        self.response = response
                    case 400:
                        self.status = 1
                        self.response = response 
                    case 401: #Unauthorised
                        self.status = 0
                        print("401 Unauthorized: invalid credentials")
                    case 404: # Not found
                        self.status = 0
                        print("404 Not Found")
                    case 429: # too many attempts
                        self.status = 0
                        print(f"429 Too Many Attempts: try again {response.headers["Retry-After"]}")
                    case _:
                        self.status = 0
                        print(json.dumps(response.json(), indent=4))
    
                if attempts >= max_attempts:
                    print(f"WARNING Exceeded Max Requests: {max_attempts}")
                    print(f"{url}")
                    self.status = 0
                    return self
    
            return self
                
        def get_code(data:Self):
            
            datajson = data.response.json()
            
            return datajson["vectorQuery"]["layers"]["123515"]["features"][0]["properties"]["SA22026_V1_00"]
        
        def get_name(data:Self):
        
            datajson = data.response.json()
            
            return datajson["vectorQuery"]["layers"]["123515"]["features"][0]["properties"]["SA22026_V1_00_NAME"]

    # ["id","neighbourhood","latitude","longitude","room_type","price","minimum_nights","number_of_reviews","calculated_host_listings_count","availability_365","number_of_reviews_ltm","month_year"] # do some stuff to data here

    longitude = x["longitude"]
    latitude = x["latitude"]

    query_obj = VectorResponse(API_KEY, LAYER)
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
    
    # load dataset
    
    data = pd.read_csv("out/listings_combined.csv", dtype=dtypes, na_values=na_values)
    data["SA22026_code"] = 0
    data["SA22026_name"] = ""
    
    data.astype({
        "SA22026_code" : int,
        "SA22026_name" : str
     })
    
    # split_data = split_dataframe(data, 2)
    # rows = [f"{','.join(data.columns)}\n"] 

    pandarallel.initialize(progress_bar=True)

    start_time = time.perf_counter()
    data:pd.DataFrame = data.parallel_apply(process_apply, axis=1)
    end_time = time.perf_counter()

    data.to_csv("out.csv")

    # pd.DataFrame(columns=data.columns).astype(data.dtypes)
    
    # user inputs API key
    
    # pool = mp.Pool(processes=PROCESSES)
    # for row in tqdm.tqdm(pool.imap(process, split_data, chunksize=CHUNKSIZE), total=len(split_data)):
        # print(row)
        # rows.append(data.to_csv(index=False, header=False, lineterminator="\n"))
    
    # with open("out.csv", "w") as file:
        # file.write("".join(rows))
    
    # pool.close()
    # pool.join()
    
    
    data = pd.read_csv("out.csv", dtype=dtypes, na_values=na_values, index_col=False)    

    hours = (end_time - start_time) // 60
    seconds = (end_time - start_time) % 60

    print(f"\n\n{int(hours)} hours, {int(seconds)} seconds ...")

    # merging parts processed by different processes
    # parts = pd.concat(pool_results, axis=0)
    
    # print(parts)
    
    # # merging newly calculated parts to data
    # data = pd.concat([data, parts], axis=1)
    
    # pdt.assert_series_equal(parts["id"], data["id"])
    
    # print(data)

if __name__ == "__main__":

    main()
    pass

