# DATA201-DATA422-GROUP-PROJECT

## Team Members

- Aksh Doshi
- Sophie Dance
- Rehutai Rapira-Davies
- Koushika Mani

## Setup

Clone this repository.

```bash
git clone https://github.com/aksh3-design/DATA201-DATA422-GROUP-PROJECT .
```

Run ```setup.py```

```bash
py setup.py
```

## Setup Alternatives

Move this repository into a virtual environment. (You can do this by changing the root directory into a virtual environment).

```bash
python -m venv .
```

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install required modules.

```bash
pip install - r requirements.txt
```

## Usage

### Initialise Pipeline.

You must first point the project modules to the paths of your data.
List only the filenames, omit extensions.

Raw airbnb listings data must be pointed to with a scrape date in ISO8601-format, with the day set to 01.

There are options for Tenancy Services rental bonds data, and you may also reconfigure the data-in and data-out directories 
in ```data.toml``` as well.

[See ```data.toml``` for more info.](data.toml)

The data pipeline will strip away data outside of a range of time specified in ```config.toml```. If the resulting
filtered data contains no entries, the pipeline will throw unhandled exceptions.

You are required to provide a Koordinates api key here as well.

You may also specify whether or not matplotlib figures are to be displayed and saved, and whether or not any
output is printed to the terminal.

[See ```config.toml``` for more info.](config.toml)

### Execute Pipeline

This will process any data specified as detailed above. Querying the Koordinates databases takes a lot of time, therefore if there
are any files that are output via this query process still present in ```tmp/```, the pipeline will skip this step.

Please keep note of this if re-executing this pipeline on new data.

```bash
py run.py
```

### Combining InsideAirbnb Listings Datasets

```
py src\combine_listings.py
```

The default output filename is ```./tmp/listings_combined.csv```. See options in ```data.toml```.

### Statistics

```
py src\reviews_per_month.py
```

This script takes ```./tmp/listings_combined.csv```. See options in ```data.toml```.

Calculates and outputs a number of statistics on reviews for Airbnb Listings in Christchurch.
By default, generated figures are saved to the ```figures/``` directory. Sumamry results are
sent to the ```out/``` directory.

### [Cleaning InsideAirbnb Listings Data](docs/listings.md)

```
py src\listclean.py
```

This script takes ```./tmp/listings_combined.csv```. See options in ```data.toml```.

The default output filename is ```./tmp/listings_combined_cleaned.csv``` defined in ```data.toml```.

### [Cleaning TenancyServices Rental Bond Data](docs/bonds.md)

```
py src\bondclean.py
```

The default output filename is ```./out/Detailed-Quarterly-Tenancy-Q1-2020-Q3-2026_cleaned.csv.csv```. See options in ```data.toml```.

### Koordinates Querying

```
py src\query.py
```

Place you Koordinates API key into the ```config.toml``` file, under ```[api]```.

### Dataset Joining

```
py src\join.py
```

This script takes ```./tmp/listings_combined_sa22026.csv.csv``` and ```./tmp/Detailed-Quarterly-Tenancy-Q1-2020-Q3-2026_cleaned.csv```,
joins them on date and location, and outputs a number of statistics on price for Airbnb Listings in Christchurch.
By default, generated figures are saved to the ```.out/``` directory. See options in ```config.toml```.

## Credits

[Statistical Area 2 2026 by Stats NZ](https://datafinder.stats.govt.nz/layer/123515-statistical-area-2-2026/) is licensed under CC BY 4.0

[Geographic Areas File by Stats NZ](https://datafinder.stats.govt.nz/table/98778-geographic-areas-file-2019/) is licensed under CC BY 4.0
