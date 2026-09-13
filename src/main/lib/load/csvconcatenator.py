import pandas as pd

class CSVConcatenator:
    
    def __init__(self, dtypes, na_values):

        self.dfs:list[pd.DataFrame] = []
        self.current_csv:pd.DataFrame = None
        self.dtypes = dtypes
        self.na_values = na_values
    
    def concatenate(self):
        return pd.concat(
                    self.dfs,
                    ignore_index=True
                )
    
    def add_column(self, column_name:str, row_values:str):
        self.current_csv[column_name] = row_values
        
        return self
    
    def load_csv(self, filename:str):
        
        df = pd.read_csv(
            filepath_or_buffer=filename,
            dtype=self.dtypes,
            na_values=self.na_values)
        
        self.current_csv = df
        
        return self
    
    def filter_rows(self, column_name, row_value):
        self.current_csv = self.current_csv[self.current_csv[column_name].str.contains(
            row_value, case=False, na=False
        )]
        return self
    
    def create(self):
        
        self.dfs.append(self.current_csv)