import requests
import json

def default_query(key:str, layer:int, x:float, y:float, max_results:int=3, radius:int=10000, geometry="true", with_field_names="true"):
    
    return f"https://koordinates.com/services/query/v1/vector.json?key={key}&layer={layer}&x={x}&y={y}&max_results={max_results}&radius={radius}&geometry={geometry}&with_field_names={with_field_names}"


if __name__ == "__main__":
    
    key = input("key")
    
    query = default_query(
        key,
        123515,
        172.5709,
        -43.47,
    )
    
    print(query)
    
    data = requests.get(query)
    # https://koordinates.com/services/query/v1/vector.json?key=59891e1c37c4492eb441d3a962387b22&layer=3936&x=172.5709&y=-43.47&max_results=3&radius=10000&geometry=true&with_field_names=true
    # https://koordinates.com/services/query/v1/vector.json?key=59891e1c37c4492eb441d3a962387b22&layer=123515&x=172.5709&y=-43.47&max_results=3&radius=10000&geometry=true&with_field_names=true
    
    print(data.status_code)
    
    print(data.json())
    
    with open("out.json", "w") as file:
        json.dump(data.json(), file)