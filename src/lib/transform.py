# Collection of basic dataframe-transformation helper functions

import pandas as pd
from collections.abc import Callable

def filter_row_by_value(data:pd.DataFrame, column:str, value:str, keep_matching=False):
    """filters rows the match value. If keep_matching is False, then it will remove those
    rows whose column entry matches value.

    Args:
        data (pd.DataFrame): Pandas dataframe.
        column (str): Column name.
        value (str): Conditional value.
        keep_matching (bool, optional): Whether to keep rows that match. Defaults to False.

    Returns:
        (pd.DataFrame): Transformed Data with filtered rows.
    """

    if keep_matching:
        data = data[(data[column] == value)]
    else:
        data = data[~(data[column] == value)]


    return data

def parse_column_entries(data:pd.DataFrame, column:str, f:Callable[[any], any], append_column:bool=False, appended_column_name:str=None):
    """Applies a parsing function to column of data table.

    Args:
        data (pd.DataFrame): Pandas dataframe.
        column (str): Column name.
        f (Callable[[any], any]): Parsing function.
        append_column (str): If True, places parsed values into new column. Defaults to False.
        appended_column_names (str): If append_column is True, this is the name of the new column. Defaults to {column}_parsed.

    Returns:
        (pd.Dataframe): Transformed Data with parsed values.
    """

    if append_column:
        if appended_column_name is None:
            appended_column_name = f"{column}_parsed"
    else:
        appended_column_name = column

    data[appended_column_name] = data[column].apply(f)

    return data

def to_numerical_specific(data:pd.DataFrame, column:str, type):
    """Converts numerical columns to 'type'

    Args:
        data (pd.DataFrame): Pandas dataframe.
        column (str): Column name.
        type (_type_): Literal, float or int.

    Returns:
        (pd.Datafram): Transformed data with column as type: 'type'.
    """

    data[column] = pd.to_numeric(data[column], errors='coerce')
    data[column] = data[column].astype(type)

    return data

def one_hot_encode(data:pd.DataFrame, column:str, dtype=int, axis=1):
    """One-Hot encodes a categorical column and appends dummy columns to end of dataset

    Args:
        data (pd.DataFrame): Pandas dataframe.
        column (str): Column name.
        dtype (_type_): Datatype for the dummy columns. Defaults to int.
        axis (int, optional): The axis to concatenate along. Defaults to 1.

    Returns:
        (pd.Dataframe): Data with concatenated, one-hot encoded columns for given categorical column.
    """

    data = pd.concat([data, pd.get_dummies(data[[column]], dtype=dtype)], axis=axis)

    return data