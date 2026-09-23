# Collection of basic print-log helper functions
import pandas as pd

def print_clean_simple(message:str):
    print(f"{' ':10}|{' ':10}| {message}")

def print_clean_log(data:pd.DataFrame, initial_rows:int, message:str):
    """prints a simple log message, detailing the number of rows

    Args:
        data (pd.DataFrame): _description_
        message (str): _description_
    """
    print(f"{data.shape[0]:10}|{initial_rows-data.shape[0]:10}| {message}")

def print_clean_cascade(messages:list[str], indent=4):
    """prints a cascade of logs, identical formatting to print_log, without information
    on number of rows left/removed.

    Args:
        messages (list[str]): messages to cascade
        indent (int, optional): Number of ' ' whitespace characters to indent log message by. Defaults to 4.
    """
    for message in messages:
        print(f"{'':10}|{'':10}|{indent*' '}- {message}")

def print_bordered(message:str):
    print("\n========================================")
    print(message.upper())
    print("========================================\n")

print_clean_log.calls = 0