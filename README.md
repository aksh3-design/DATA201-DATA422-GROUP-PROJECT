# DATA201-DATA422-GROUP-PROJECT

## Team Members

- Aksh Doshi
- Sophie Dance
- Rehutai Rapira-Davies
- Koushika Mani

## Introduction

The [Inside Airbnb](https://insideairbnb.com/get-the-data/) website compiles listing data for a number
of different cities and countries around the world.

## Data Recorded for New Zealand

| Field                                 | Type           | Categorical | Calculated | Description
| ------------------------------------- | -------------- | :---------: | :--------: | ------------
| ```id```                              | ```integer```  |             |            | Airbnb's unique identifier for the listing.
| ```name```                            | ```string```   |             |            | Taken from the title of the Airbnb listing.
| ```host_id```                         | ```integer```  |             |            | Airbnb's unique identifier for a host.
| ```host_name```                       | ```string```   |             |            | The user/display name of the host. This name is displayed to Airbnb users, just below the listing.
| ```neighbourhood_group```             | ```text```     | yes         | yes        | The neighbourhood group as geocoded using the latitude and longitude against neighborhoods as defined by open or public digital shapefiles.
| ```neighbourhood```                   | ```text```     | yes         | yes        | The neighbourhood as geocoded using the latitude and longitude against neighborhoods as defined by open or public digital shapefiles.
| ```latitude```                        | ```numeric```  |             |            | Uses the World Geodetic System (WGS84) projection for latitude and longitude.
| ```longitude```                       | ```numeric```  |             |            | Uses the World Geodetic System (WGS84) projection for latitude and longitude.
| ```room_type```                       | ```string```   | yes         |            | Categorises rooms into the different types, ```"Private room"```, ```"Entire home/apt"```, ```"Shared room"```, and ```"Hotel room"```.
| ```price```                           | ```currency``` |             |            | daily price in local currency. Note, $ sign may be used despite locale.
| ```minimum_nights```                  | ```integer```  |             |            | minimum number of night stay for the listing (calendar rules may be different).
| ```number_of_reviews```               | ```integer```  |             |            | The number of reviews the listing has.
| ```last_review```                     | ```date```     |             | yes        | The date of the last/newest review written in __ISO-8601__ ```yyyy-mm-dd``` format. 
| ```reviews_per_month```               | ```numeric```  |             |            | The number of reviews the listing has in total over the lifetime of the listing.
| ```calculated_host_listings_count```  | ```integer```  |             | yes        | The number of listings the host has in the current scrape, in the city/region geography.
| ```availability_365```                | ```integer```  |             | yes        | avaliability_x. The availability of the listing x days in the future as determined by the calendar. Note a listing may be available because it has been booked by a guest or blocked by the host.
| ```number_of_reviews_ltm```           | ```integer```  |             | yes        | The number of reviews the listing has (in the last 12 months)
| ```license```                         | ```string```   |             |            | The licence/permit/registration number

## In the case of the New Zealand Dataset, and other clarifications

### ```id``` :
The id field is unique to each listing, but a listing is not necessarily unique to a room. There are many 'duplicate' listings, which are differentiated by other fields in the dataset. This is because listings may be deleted, reinstated, or edited. There may also be multiple rooms for the same property listed.

### ```host_name``` :
The name of a host is not neccessarily written in with the english-latin alphabet.

### ```neighbourhood_group``` :
The ```neighbourhood_group``` field represents the Territorial authorities of New Zealand; her 53 district councils, 12 city councils, and 2 sui generis (Auckland Council and Chatham Islands Council). This makes for a total of 67 different neighbourhood groupings.

### ```neighbourhood``` :
Neighbourhood names for each listing are compiled by comparing the listing's geographic coordinates with a city's definition of neighbourhoods. Airbnb neighbourhood names are not used because of their inaccuracies. In the case of the New Zealand dataset the neighbourhood field represents New Zealand's general wards defined under the Local Electoral Act.
__Interestingly only__ ***210 of 224*** __general wards are present in the summary dataset.__

### ```latitude``` and ```longtitude```:
Location information for listings are anonymized by Airbnb.

- In practice, this means the location for a listing on the map, or in the data will be from 0-450 feet (150 metres) of the actual address.
- Listings in the same building are anonymized by Airbnb individually, and therefore may appear "scattered" in the area surrounding the actual address.

### ```room_type``` :
Categorises rooms into the different types:

| Field                     | Reference     |
| ------------------------- | ------------- | 
| ```"Private room"```      | Private rooms |
| ```"Entire home/apt"```   | Entire Places |
| ```"Shared room"```       | Shared Rooms  |
| ```"Hotel room"```        | Hotel Rooms   |

These room types are described in the following, provided by Inside Airbnb following their [assuumptions](https://insideairbnb.com/data-assumptions/).

#### __Entire homes__
Entire homes are best if you're seeking a home away from home. With an entire place, you'll have the whole space to yourself. This usually includes a bedroom, a bathroom, a kitchen, and a separate, dedicated entrance. Hosts should note in the description if they'll be on the property or not (ex: "Host occupies first floor of the home"), and provide further details on the listing.

#### __Private rooms__
Private rooms are great for when you prefer a little privacy, and still value a local connection. When you book a private room, you'll have your own private room for sleeping and may share some spaces with others. You might need to walk through indoor spaces that another host or guest may occupy to get to your room.

#### __Shared rooms__
Shared rooms are for when you don't mind sharing a space with others. When you book a shared room, you'll be sleeping in a space that is shared with others and share the entire space with other people. Shared rooms are popular among flexible travelers looking for new friends and budget-friendly stays.

### ```last_review``` :
If the listing has no reviews, then the ```last_review``` and ```reviews_per_month``` fields will be __empty__.

### ```availability_365``` :
The Airbnb calendar for a listing does not differentiate between a booked night vs an unavailable night, therefore these bookings have been counted as "unavailable". This serves to understate the Availability metric because popular listings will be "booked" rather than being "blacked out" by a host.

## Sources:

- [Inside Airbnb - Datasets](https://insideairbnb.com/get-the-data/)
- [Inside Airbnb - Data Dictionary](https://docs.google.com/spreadsheets/d/1iWCNJcSutYqpULSQHlNyGInUvHg2BoUGoNRIGa6Szc4/edit?gid=1322284596#gid=1322284596)
- [Inside Airbnb - Data Assumptions](https://insideairbnb.com/data-assumptions/)