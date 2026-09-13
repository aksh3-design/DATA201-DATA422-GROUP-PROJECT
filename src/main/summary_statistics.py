import pandas as pd
import pandera as pa
from src.main.lib.schema.data_schema import schema
from datetime import datetime

class SummaryStatistics:

    def __init__(self, df):
        
        self.df:pd.DataFrame = df
    
    # basics stats by type
    
    def category_stats(self, column:str) -> dict[str: int]:
        """ basic categorical type statistics

        Returns:
            dict[str: int]: Dictionary with categories as keys and occurences as values
        """

        result = dict()

        categories = list(self.df[column].cat.categories)
        
        for category in categories:
        
            result[category] = (self.df[column] == category).sum()
            
        return result
        
    def numerical_stats(self, column:str) -> tuple[float, float, float, float]:
        """ basic numerical type statistics

        Args:
            column (str): column name

        Returns:
            tuple[float, float, float, float]: (min, max, mean, std)
        """
        
        min = self.df[column].min()
        max = self.df[column].max()
        mean = self.df[column].mean()
        std = self.df[column].std()

        return (min, max, mean, std)

    def string_stats(self, column:str) -> dict[str: int]: # basically category stats, seperated just in case
        
        result = dict()
        
        unique_strings = list(self.df[column].unique())
        
        for string_value in unique_strings:
        
            result[string_value] = (self.df[column] == string_value).sum()
            
        return result
  
    def datetime_stats(self, column:str) -> tuple[datetime, datetime, datetime]:
        """ basic datetime type statistics
        
        Args:
            column (str): column name
        
        Returns:
            tuple[float, float, float, float]: (first, last, count, range)
        """
        
        dates:pd.DatetimeIndex = pd.DatetimeIndex(self.df[column]) 
        
        # print(dates.day_name())
        
        days = dates.day_name().value_counts(dropna=False).to_dict()
        months = dates.month_name().value_counts(dropna=False).to_dict()
        years = dates.year.value_counts(dropna=False).to_dict()
        
        first = dates.min()
        last = dates.max()
        
        range = last - first
            
        return (days, months, years, first, last, range)
    
    def key_stats(self, column:str) -> dict[str: int]:
        """ Assuming that the row values are key-identifiers, returns the total occurences of each key.
        """
        
        # for now, completely indistinguishable from string_stats
            
        return self.string_stats(column)
    
    def missing_values(self, column:str) -> int:
        """total number of missing values in that column"""
        return self.df[column].isna().sum()
    
    def num_unique(self, column:str) -> int:
        """total number of unique values in that column"""
        return self.df[column].nunique()
    
    def num_rows(self, column:str) -> int:
        """return number of rows"""
        return len(self.df)
    
    def complete_rate(self, column:str)-> float:
        return 1 - self.missing_values / self.num_rows
    
    def all_category_stats(self):
        
        result = dict()
        
        category_columns = self.df.select_dtypes(["category"])
        
        for column_name in category_columns.keys():
            result[column_name] = self.category_stats(column_name)
            
        return result
    
    def all_numerical_stats(self):
        
        result = dict()
        
        numerical_columns = self.df.select_dtypes(["Int64", float])
        
        for column_name in numerical_columns.keys():
            result[column_name] = self.numerical_stats(column_name)
            
        return result

    def all_string_stats(self):
        
        result = dict()
        
        string_columns = self.df.select_dtypes([str])
        
        for column_name in string_columns.keys():
            result[column_name] = self.string_stats(column_name)
            
        return result

    def all_datetime_stats(self):
        
        result = dict()
        
        datetime_columns = self.df.select_dtypes(["datetime64"])
        
        for column_name in datetime_columns.keys():
            result[column_name] = self.datetime_stats(column_name)
            
        return result
