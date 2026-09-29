# DATA201-DATA422-GROUP-PROJECT

## Team Members

- Aksh Doshi
- Sophie Dance
- Rehutai Rapira-Davies
- Koushika Mani

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install required modules.

```bash
pip install - r requirements.txt
```

## Usage

### Combining InsideAirbnb Listings Datasets

```
py src\combine_listings.py
```

The default output filename is ```./out/listings_combined.csv``` defined in ```config.ini```.

### Statistics

```
py src\reviews_per_month.py
```

This script takes ```./data/listings_combined.csv```

Calculates and outputs a number of statistics on reviews for Airbnb Listings in Christchurch.
By default, generated figures are saved to the ```.out/``` directory.

### [Cleaning InsideAirbnb Listings Data](docs/listings.md)

```
py src\listclean.py
```

This script takes ```./data/listings_combined.csv```

The default output filename is ```./out/listings_combined_cleaned.csv``` defined in ```config.ini```.

### [Cleaning TenancyServices Rental Bond Data](docs/bonds.md)

```
py src\bondclean.py
```

The default output filename is ```./out/Detailed-Quarterly-Tenancy-Q1-2020-Q3-2026_cleaned.csv.csv``` defined in ```config.ini```.

### Koordinates Querying

```
py src\query.py
```

Place you Koordinates API key into the config.ini file, under ```[config]```.

### Dataset Joining

```
py src\join.py
```

This script takes ```./data/listings_combined_sa22026.csv.csv``` and ```./data/Detailed-Quarterly-Tenancy-Q1-2020-Q3-2026_cleaned.csv```,
joins them on date and location, and outputs a number of statistics on price for Airbnb Listings in Christchurch.
By default, generated figures are saved to the ```.out/``` directory.

## Credits

[Statistical Area 2 2026 by Stats NZ](https://datafinder.stats.govt.nz/layer/123515-statistical-area-2-2026/) is licensed under CC BY 4.0
[Geographic Areas File by Stats NZ](https://datafinder.stats.govt.nz/table/98778-geographic-areas-file-2019/) is licensed under CC BY 4.0