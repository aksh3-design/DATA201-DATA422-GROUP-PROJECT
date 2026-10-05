# executes pipeline

import os
from src.lib.log import print_bordered, log

print_bordered("COMBINING AIRBNB LISTINGS DATA")

os.system("py src\\combine_listings.py")

print_bordered("CLEANING AIRBNB LISTINGS DATA")

os.system("py src\\listclean.py")

print_bordered("CLEANING TENANCY SERVICE BOND DATA ")

os.system("py src\\bondclean.py")

print_bordered("LISTINGS REVIEWS STATISTICS")

os.system("py src\\reviews.py")

print_bordered("PARSE SA22026 CODES FROM LISTING CO-ORDINATES")

from src.config import LISTINGS_SA22026_PATH
from pathlib import Path

filepath = Path(LISTINGS_SA22026_PATH)

if filepath.exists():
    log(f"Query data already exists at {LISTINGS_SA22026_PATH}")
else:
    os.system("py src\\query.py")

print_bordered("JOIN AIRBNB LISTINGS DATA AND TENANCY SERVICES DATA, RETRIEVE STATISTICS")

os.system("py src\\join.py")