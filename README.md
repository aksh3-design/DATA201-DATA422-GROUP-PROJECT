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

## Missing Values





## Christchurch Listing Data Cleaning

The Christchurch listing dataset created in Deliverable 3 was cleaned using a reproducible Python script[cite: 3]. The original dataset was kept unchanged in the `data/raw` folder, while the cleaned dataset was saved in the `data/processed` folder[cite: 3].

### Columns Removed

The following columns were removed[cite: 3]:
* `name` – listing names were not required for the planned quantitative analysis[cite: 3].
* `host_id` – host-level identification was not required for the planned analysis[cite: 3].
* `host_name` – host names were not required for the planned analysis[cite: 3].
* `neighbourhood_group` – all observations belong to Christchurch City, so this column does not provide useful variation[cite: 3].
* `last_review` – not required for the planned rental price and availability analysis[cite: 3].
* `reviews_per_month` – not required for the planned analysis[cite: 3].
* `license` – the column contained no values in the dataset and therefore provided no useful information[cite: 3].

The following columns were retained because they are useful for the planned analysis[cite: 3]:  
`id`, `neighbourhood`, `latitude`, `longitude`, `room_type`, `price`, `minimum_nights`, `number_of_reviews`, `calculated_host_listings_count`, `availability_365`, `number_of_reviews_ltm`, and `month_year`[cite: 3].

Latitude and longitude were retained as required and may also be useful for geographical analysis[cite: 3].

### Missing Values

Rows with missing `id`, `latitude`, `longitude`, `neighbourhood`, `room_type`, or `month_year` were removed because these variables are required to identify, locate and analyse listings[cite: 3].

The `price` column contains missing values[cite: 3]. These were not replaced with estimated values because imputing a rental price could introduce artificial information into the dataset[cite: 3]. The rows were retained because they may still provide useful information for other analyses, particularly availability[cite: 3]. Rows without a price can be excluded when calculating rental-price statistics[cite: 3].

The other columns containing missing values that were not required for the analysis were removed as described above[cite: 3].

### Duplicate Observations

Exact duplicate rows were removed[cite: 3].

The dataset also contains some very large listing IDs represented in scientific notation[cite: 3]. Because this can cause different IDs to appear identical after numeric conversion, `id` + `month_year` was not used as a duplicate-removal rule[cite: 3]. This avoids accidentally removing potentially different listings[cite: 3]. The cleaning process therefore removes only exact duplicate rows[cite: 3].

### Invalid Values

Prices equal to or below zero were treated as invalid and removed[cite: 3]. Missing prices were retained[cite: 3].

Availability values outside the range of 0–365 were treated as invalid and removed[cite: 3]. The dataset contained no invalid availability values[cite: 3].

Latitude and longitude were checked for valid geographic ranges[cite: 3]. No invalid coordinates were identified[cite: 3].

### Reproducibility

The cleaning was performed using `clean_listings.py`[cite: 3]. The script reads the raw dataset and produces the cleaned dataset using the same predefined steps each time[cite: 3]. This allows all team members to rerun the code and reproduce the same preprocessing process[cite: 3].

The cleaning script also produces a cleaning report showing the number of rows before and after each cleaning step[cite: 3].

---

## Tenancy Services Rental Bond Data

### Data Source

The rental bond dataset was downloaded from the New Zealand Tenancy Services website[cite: 3].

* **Source:** [Tenancy Services – Rental bond data](https://www.tenancy.govt.nz/about-tenancy-services/data-and-statistics/rental-bond-data/)[cite: 3]
* **Dataset:** Detailed quarterly report, 2020–2026[cite: 3]

The dataset contains rental bond information for New Zealand and provides information about rental market activity[cite: 3]. The data is reported by geographic location, dwelling type and number of beds, together with information about rental bonds and weekly rent[cite: 3].

The dataset used for this project is:  
`Detailed-Quarterly-Tenancy-Q1-2020-Q3-2026.csv`[cite: 3]

The data was downloaded from the Tenancy Services rental bond data webpage[cite: 3].

### Dataset Columns

The original dataset contains 12 columns[cite: 3].

| Column | Description |
| :--- | :--- |
| `TimeFrame` | The time period for the rental bond data. The dataset is reported by quarter.[cite: 3] |
| `Location Id` | Identifier for the geographic location associated with the rental bond records.[cite: 3] |
| `Dwelling Type` | The type of dwelling associated with the rental bond records.[cite: 3] |
| `Number Of Beds` | The number of bedrooms/beds in the dwelling. The dataset also contains aggregate categories such as ALL and categories such as 5+.[cite: 3] |
| `Total Bonds` | Total number of rental bonds recorded for the relevant time period, location, dwelling type and number of beds.[cite: 3] |
| `Active Bonds` | Number of rental bonds that were active for the relevant category and time period.[cite: 3] |
| `Closed Bonds` | Number of rental bonds closed for the relevant category and time period.[cite: 3] |
| `Median Rent` | Median weekly rent for the relevant category.[cite: 3] |
| `Geometric Mean Rent` | Geometric mean of weekly rent for the relevant category.[cite: 3] |
| `Upper Quartile Rent` | Upper quartile of weekly rent. Approximately 75% of observations are at or below this value.[cite: 3] |
| `Lower Quartile Rent` | Lower quartile of weekly rent. Approximately 25% of observations are at or below this value.[cite: 3] |
| `Log Std Dev Weekly Rent` | Logarithmic standard deviation of weekly rent, describing variation in weekly rents.[cite: 3] |

### Original Dataset

The original dataset contains 226,080 rows and 12 columns[cite: 3].  
The dataset covers quarterly rental bond information from 2020 through 2026[cite: 3].  
The original file is retained without modification so that the cleaning process can be reproduced[cite: 3].

### Cleaning Decisions

The cleaning was performed using Python so that all team members can reproduce the same preprocessing steps[cite: 3].

#### Timeframe
The listing dataset used in this project is recorded monthly, while the Tenancy Services dataset is recorded quarterly[cite: 3].

The listing dataset covers October 2025 to June 2026[cite: 3]. Therefore, the corresponding quarters from the bond dataset were retained[cite: 3]:
* **Q4 2025** – represented by `2025-10-01`[cite: 3]
* **Q1 2026** – represented by `2026-01-01`[cite: 3]
* **Q2 2026** – represented by `2026-04-01`[cite: 3]

The bond dataset cannot distinguish individual months within a quarter[cite: 3]. Therefore, the October–December 2025 listing observations correspond to Q4 2025 bond data, January–March 2026 correspond to Q1 2026, and April–June 2026 correspond to Q2 2026[cite: 3].

This difference in time resolution will be considered when combining and comparing the two datasets[cite: 3].

#### Location Id
`Location Id` was retained because it is required for identifying the geographic area and is important for the future combination and comparison of the datasets[cite: 3].

Rows with a missing `Location Id` were removed because they cannot be reliably associated with a geographic location[cite: 3].

Rows with `Location Id = -99` were also removed because this value does not provide a specific usable geographic location for the planned location-based comparison[cite: 3].

#### Other Columns
No other original columns were removed[cite: 3].

The remaining variables may be useful when comparing rental prices, rental activity and property characteristics[cite: 3]. In particular, `Median Rent`, `Geometric Mean Rent`, `Total Bonds`, `Active Bonds`, `Closed Bonds`, `Dwelling Type` and `Number Of Beds` may be useful for the planned analysis[cite: 3].

Keeping these variables also avoids removing potentially useful information before the datasets are combined[cite: 3].

#### Missing Rental Values
Rows with missing rental statistics were not automatically removed[cite: 3].

Missing values can occur in columns such as `Median Rent`, `Geometric Mean Rent`, `Upper Quartile Rent`, `Lower Quartile Rent` and `Log Std Dev Weekly Rent`[cite: 3].

These missing values were retained because the row may still contain useful information about rental bond activity, location or dwelling characteristics[cite: 3].

Missing rental values will be excluded only when calculating a particular rental-price statistic that requires a non-missing rent value[cite: 3].

#### Duplicate Rows
Exact duplicate rows were checked[cite: 3].  
No exact duplicate rows were identified in the original dataset[cite: 3].  
Therefore, no observations were removed for exact duplication[cite: 3].

### Consequences of Cleaning

The cleaning process reduces the dataset to the relevant quarterly timeframe and removes records that cannot be associated with a usable geographic location[cite: 3].

The exact number of rows removed at each stage is recorded by the Python cleaning script[cite: 3].

The cleaned dataset is saved separately from the original dataset so that the original data remains available for verification and reproducibility[cite: 3].

### Reproducibility

The cleaning process is performed using the Python script[cite: 3]:
`clean_bonds.py`[cite: 3]

The script reads the original Tenancy Services CSV, applies the documented cleaning decisions, sorts the data consistently and creates the cleaned dataset[cite: 3].

All team members can run the same script using the same original dataset to reproduce the preprocessing[cite: 3].

### Data Limitations

There are several limitations to consider[cite: 3]:
* The Tenancy Services dataset is quarterly, while the listing dataset is monthly[cite: 3].
* The bond data therefore cannot provide separate rental bond figures for individual months within a quarter[cite: 3].
* Some rental statistics contain missing values[cite: 3].
* `Location Id` is used as a geographic identifier, so records without a usable location identifier cannot be used for location-based comparisons[cite: 3].
* The bond dataset and listing dataset measure different aspects of the rental market[cite: 3]. Rental bond records and online property listings should therefore not be assumed to represent exactly the same population of properties[cite: 3].

These limitations will be considered when combining and comparing the datasets[cite: 3].

## Sources:

- [Inside Airbnb - Datasets](https://insideairbnb.com/get-the-data/)
- [Inside Airbnb - Data Dictionary](https://docs.google.com/spreadsheets/d/1iWCNJcSutYqpULSQHlNyGInUvHg2BoUGoNRIGa6Szc4/edit?gid=1322284596#gid=1322284596)
- [Inside Airbnb - Data Assumptions](https://insideairbnb.com/data-assumptions/)
