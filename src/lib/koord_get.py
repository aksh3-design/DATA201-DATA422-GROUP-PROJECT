import requests
import json
from typing import Literal, Self
from config import API_KEY

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

if __name__ == "__main__":

    query_object = VectorResponse(
        API_KEY,
        123515
    )

    url = query_object.get_url(172.57088, -43.47002)

    name = query_object.query(url).get_name()
    code = query_object.get_code()