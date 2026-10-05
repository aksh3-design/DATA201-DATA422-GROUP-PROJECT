# executes pipeline

import os

os.system("py src\\combine_listings.py")

os.system("py src\\listclean.py")

os.system("py src\\bondclean.py")

os.system("py src\\reviews_per_month.py")

os.system("py src\\query.py")