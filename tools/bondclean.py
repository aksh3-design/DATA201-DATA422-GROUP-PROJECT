import argparse
import pandas as pd
import src.main.lib.clean.bond_cleaner as cleaner

parser = argparse.ArgumentParser(
    prog="Datatools",
    description="working on the desc ... ")

parser.add_argument('input_filename')
parser.add_argument('-o', '--output')

args = parser.parse_args()

default_output = "cleaned_data.csv"
data = None

if args.input_filename:
    try:
        print("loading csv ...")
        data = pd.read_csv(f"{args.input_filename}.csv")
    except FileNotFoundError:
        print(f"No such file or directory: '{args.input_filename}'")
        exit()

print("cleaning csv ...")
data = cleaner.clean(data)

print("writing csv ...")
if args.output:
    data.to_csv(f"{args.output}.csv")
else:
    data.to_csv(f"{default_output}")

print("cleaning completed.")

