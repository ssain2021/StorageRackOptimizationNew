################################  utils.py  ####################################
# Author: Sukhendu Sain
# Description: Utils file of codebase. Houses main utility functions
# Data: 22-Nov-2024
#################################################################################


import pandas as pd
from tabulate import tabulate



def read_excel(file_path: str, sheet_name:int=0) -> pd.DataFrame:
    """
    Reads an Excel file and returns a Pandas DataFrame.

    Args:
        file_path (str): Path to the Excel file.
        sheet_name (str): Name or index of the sheet in the Excel file.

    Returns:
        pandas.DataFrame: A DataFrame containing the data from the specified Excel sheet if no Error.

    Prints:
        "File not found": If the specified file does not exist.
        "The file is empty": If the file is empty.
        "The file could not be parsed": If there's an error parsing the file.
    """
    df = _read_excel(file_path, sheet_name)
    return df


def print_df(df: pd.DataFrame, rows: int=None, style: str="fancy_grid") -> None:
    """
    Prints a formatted representation of a DataFrame.
    
    Args:
        df (pandas.DataFrame): The DataFrame to print.
        rows (int): Number of rows to display. Defaults to All.
        style (str): Table format style. Defaults to "fancy_grid".
    """
    _print_df(df, rows, style)
    


##################### FUNCTION INITS ##############################

def _read_excel(file_path, sheet_name):
    try:
        df = pd.read_excel(file_path, sheet_name)
        return df
    # except FileNotFoundError:
    #     print(file_path.split('/')[0] + ": File not found")
    #     return None
    except pd.errors.EmptyDataError:
        print(file_path.split('/')[0] + ": The file is empty")
        return None
    except pd.errors.ParserError:
        print(file_path.split('/')[0] + ": The file could not be parsed")
        return None
    

def _print_df(df, rows, style):
    if rows:
        print(tabulate(df.head(rows), headers = 'keys', tablefmt = style))
    else:
        print(tabulate(df, headers = 'keys', tablefmt = style))
