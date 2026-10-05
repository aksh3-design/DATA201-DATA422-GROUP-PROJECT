import os

# This project does not work unless run inside of a virtual environment

os.system("python -m venv . --without-scm-ignore-files") # changes root directory into virtual environment
os.system("Scripts\\activate.bat")
os.system("pip install -r requirements.txt") # install requirements