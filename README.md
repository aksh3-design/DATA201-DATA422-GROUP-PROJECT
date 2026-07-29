# DATA201-DATA422-GROUP-PROJECT

## Team Members

- Aksh Doshi
- Sophie Dance
- Rehutai Rapira-Davies
- Koushika Mani

# Deliverable 2 - NZ June 2026 Dataset

## Introduction

The [Inside Airbnb](https://insideairbnb.com/get-the-data/) website compiles listing data for a number
of different cities and countries around the world. The data is released in a csv format under the name
```listing.csv```. 

## Data Recorded for New Zealand

### ```id``` :
Unique number which identifies each listing

### ```name``` :
Display-name for a listing in a catalogue. It may be brief, or lengthy and descriptive.
E.g. *Back-yard glamping in a hilly village hideaway*, *Family Room sleep 6*, *Flat 8C*.

### ```host_id``` :
Unique number for assigned to each host. One host id is assigned to a listing. If there are
more than one person hosting, they are considered one host and are assigned one host id.

### ```host_name``` :
The name/names of the host. *Note that* ```host_name``` *does not need to be written with the latin alphabet*

### ```neighbourhood_group``` :
The district location of the listing. **Is it the same thing as an electorate?**

### ```neighbourhood``` :
The ward in which the listing resides.

### ```latitude``` and ```longitude``` :
Geodata showing the exact location of the listing on earth.

### ```room_type``` :
Categorises rooms into the different types, ```"Private room"```, ```"Entire home/apt"```, ```"Shared room"```, ```"Hotel room"```.

### ```price``` :
The price of the room **per night? per day? check-in / check-out times?**

### ```minimum_nights``` :
The minimum length of stay **Follow up from previous questions**

### ```number_of_reviews``` :
The number of reviews that the listing has.

### ```last_review``` :
The date of the last review in ```yyyy-mm-dd``` format. *Note that it is not a string*.
If the listing has no reviews, then this field will be empty.

### ```reviews_per_month``` :
A float average, representing reviews per month. **average reviews in a month per month? average review-over-all-time per all-months**

### ```calculated_host_listings_count``` :
Total number of listings that the current host is hosting.

### ```availability_365``` :
The number of days out of the year which the listing is available.

### ```number_of_reviews_ltm``` :
*I have no idea*

### ```license``` :
*Most listings don't even have this filled*

Source: Inside Airbnb https://insideairbnb.com/get-the-data/