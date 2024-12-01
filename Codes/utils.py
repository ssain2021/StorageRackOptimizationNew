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
    

def getRedHotStorage(depth: int, width: int, height: int) -> str:
    """

    """
    storageType, subStorage = _getRedHotStorage(depth, width, height)
    return storageType, subStorage

def getOrangeStorage(depth: int, width: int, height: int) -> str:
    """

    """
    storageType, subStorage = _getOrangeStorage(depth, width, height)
    return storageType, subStorage


def getYellowStorage(depth: int, width: int, height: int) -> str:
    """

    """
    storageType, subStorage = _getYellowStorage(depth, width, height)
    return storageType, subStorage


def getGreenStorage(depth: int, width: int, height: int) -> str:
    """

    """
    storageType, subStorage = _getGreenStorage(depth, width, height)
    return storageType, subStorage


def getBlueStorage(depth: int, width: int, height: int) -> str:
    """

    """
    storageType, subStorage = _getBlueStorage(depth, width, height)
    return storageType, subStorage

##################### FUNCTION INITS ##############################

def _read_excel(file_path, sheet_name):
    try:
        df = pd.read_excel(file_path, sheet_name)
        return df
    # except FileNotFoundError:
    #     print(file_path.split('/')[0] + ": File not found")
    #     return None
    except pd.errors.EmptyDataError:
        print(file_path.split('/')[-1] + ": The file is empty")
        return None
    except pd.errors.ParserError:
        print(file_path.split('/')[-1] + ": The file could not be parsed")
        return None
    

def _print_df(df, rows, style):
    if rows:
        print(tabulate(df.head(rows), headers = 'keys', tablefmt = style))
    else:
        print(tabulate(df, headers = 'keys', tablefmt = style))


def _getRedHotStorage(depth, width, height):
    # Initialize the empty Variables
    storageType = ""
    subStorage = ""

    # Start of High Density Drawers
    if (depth <= 24) & (height <= 6) & (width <= 12):
        storageType = "High Density Drawers" # Set Storage Type accordingly
        if (width <= 8): # If the depth is less than 8
            subStorage = "48-inch Drawer - 6 Compart"
        elif (width <= 9): 
            subStorage = "36-inch Drawer - 4 Compart"
        elif (width <= 12):
            subStorage = "48-inch Drawer - 4 Compart"
    # Start of Clip Shelving
    elif (depth <= 24) & (height <= 15) & (width <= 48):
        storageType = "Clip Shelving" # Set Storage Type accordingly
        if (depth <= 12):  # If the depth is less than 12
            subStorage = "12-inch Deep - "
        elif (depth <= 18):
            subStorage = "18-inch Deep - "
        elif (depth <= 24):
            subStorage = "24-inch Deep - "
        if (width <= 36):
            subStorage += "36-inch Wide Shelf"
        elif (width <= 48):
            subStorage += "48-inch Wide Shelf"
    # Start of Bulk Storage        
    elif (depth <= 96) & (height >= 12) & (width <= 96):
        storageType = "Bulk Storage" # Set Storage Type accordingly
        if (depth <= 24): # If the depth is less than 24
            subStorage = "24-inch Deep - "
        elif (depth <= 36):
            subStorage = "36-inch Deep - "
        elif (depth <= 42):
            subStorage = "42-inch Deep - "
        elif (depth <= 48):
            subStorage = "48-inch Deep - "
        elif (depth <= 72):
            subStorage = "72-inch Deep - "
        elif (depth <= 96):
            subStorage = "96-inch Deep - "
        if (width <= 48):
            subStorage += "48-inch Wide Shelf"
        elif (width <= 72):
            subStorage += "96-inch Wide Shelf"
        elif (width <= 96):
            subStorage += "96-inch Wide Shelf"

    return storageType, subStorage # Return the Values


def _getOrangeStorage(depth, width, height):
    # Initialize the empty Variables
    storageType = ""
    subStorage = ""

    if (depth <= 24) & (height <= 15) & (width <= 48): # For Clip Shelving:
        storageType = "Clip Shelving" # Set Storage Type accordingly
        if (depth <= 12):  # If the depth is less than 12
            subStorage = "12-inch Deep - "
        elif (depth <= 18):
            subStorage = "18-inch Deep - "
        elif (depth <= 24):
            subStorage = "24-inch Deep - "
        if (width <= 36):
            subStorage += "36-inch Wide Shelf"
        elif (width <= 48):
            subStorage += "48-inch Wide Shelf"
    elif (depth <= 96) & (height > 12) & (width <= 96): # For Bulk Shelving
        storageType = "Bulk Storage" # Set Storage Type accordingly
        if (depth <= 24): # If the depth is less than 24
            subStorage = "24-inch Deep - "
        elif (depth <= 36):
            subStorage = "36-inch Deep - "
        elif (depth <= 42):
            subStorage = "42-inch Deep - "
        elif (depth <= 48):
            subStorage = "48-inch Deep - "
        elif (depth <= 72):
            subStorage = "72-inch Deep - "
        elif (depth <= 96):
            subStorage = "96-inch Deep - "
        if (width <= 48):
            subStorage += "48-inch Wide Shelf"
        elif (width <= 72):
            subStorage += "96-inch Wide Shelf"
        elif (width <= 96):
            subStorage += "96-inch Wide Shelf"

    return storageType, subStorage # Return the Values


def _getYellowStorage(depth, width, height):
    # Initialize the empty Variables
    storageType = ""
    subStorage = ""
    
    if (depth <= 24) & (height <= 15) & (width <= 48): # For Clip Shelving:
        storageType = "Clip Shelving" # Set Storage Type accordingly
        if (depth <= 12):  # If the depth is less than 12
            subStorage = "12-inch Deep - "
        elif (depth <= 18):
            subStorage = "18-inch Deep - "
        elif (depth <= 24):
            subStorage = "24-inch Deep - "
        if (width <= 36):
            subStorage += "36-inch Wide Shelf"
        elif (width <= 48):
            subStorage += "48-inch Wide Shelf"
    elif (depth <= 96) & (height > 12) & (width <= 96): # For Bulk Shelving
        storageType = "Bulk Storage" # Set Storage Type accordingly
        if (depth <= 24): # If the depth is less than 24
            subStorage = "24-inch Deep - "
        elif (depth <= 36):
            subStorage = "36-inch Deep - "
        elif (depth <= 42):
            subStorage = "42-inch Deep - "
        elif (depth <= 48):
            subStorage = "48-inch Deep - "
        elif (depth <= 72):
            subStorage = "72-inch Deep - "
        elif (depth <= 96):
            subStorage = "96-inch Deep - "
        if (width <= 48):
            subStorage += "48-inch Wide Shelf"
        elif (width <= 72):
            subStorage += "96-inch Wide Shelf"
        elif (width <= 96):
            subStorage += "96-inch Wide Shelf"

    return storageType, subStorage # Return the Values


def _getGreenStorage(depth, width, height):
    # Initialize the empty Variables
    storageType = ""
    subStorage = ""
    
    if (depth <= 96) & (height > 12) & (width <= 96): # For Bulk Shelving
        storageType = "Bulk Storage" # Set Storage Type accordingly
        if (depth <= 24): # If the depth is less than 24
            subStorage = "24-inch Deep - "
        elif (depth <= 36):
            subStorage = "36-inch Deep - "
        elif (depth <= 42):
            subStorage = "42-inch Deep - "
        elif (depth <= 48):
            subStorage = "48-inch Deep - "
        elif (depth <= 72):
            subStorage = "72-inch Deep - "
        elif (depth <= 96):
            subStorage = "96-inch Deep - "
        if (width <= 48):
            subStorage += "48-inch Wide Shelf"
        elif (width <= 72):
            subStorage += "96-inch Wide Shelf"
        elif (width <= 96):
            subStorage += "96-inch Wide Shelf"
    elif (depth <= 24) & (height <= 15) & (width <= 48): # For Clip Shelving:
        storageType = "Clip Shelving" # Set Storage Type accordingly
        if (depth <= 12):  # If the depth is less than 12
            subStorage = "12-inch Deep - "
        elif (depth <= 18):
            subStorage = "18-inch Deep - "
        elif (depth <= 24):
            subStorage = "24-inch Deep - "
        if (width <= 36):
            subStorage += "36-inch Wide Shelf"
        elif (width <= 48):
            subStorage += "48-inch Wide Shelf"

    return storageType, subStorage # Return the Values


def _getBlueStorage(depth, width, height):
    # Initialize the empty Variables
    storageType = ""
    subStorage = ""
    
    if (depth <= 96) & (height > 12) & (width <= 96): # For Bulk Shelving
        storageType = "Bulk Storage" # Set Storage Type accordingly
        if (depth <= 24): # If the depth is less than 24
            subStorage = "24-inch Deep - "
        elif (depth <= 36):
            subStorage = "36-inch Deep - "
        elif (depth <= 42):
            subStorage = "42-inch Deep - "
        elif (depth <= 48):
            subStorage = "48-inch Deep - "
        elif (depth <= 72):
            subStorage = "72-inch Deep - "
        elif (depth <= 96):
            subStorage = "96-inch Deep - "
        if (width <= 48):
            subStorage += "48-inch Wide Shelf"
        elif (width <= 72):
            subStorage += "96-inch Wide Shelf"
        elif (width <= 96):
            subStorage += "96-inch Wide Shelf"
    elif (depth <= 24) & (height <= 15) & (width <= 48): # For Clip Shelving:
        storageType = "Clip Shelving" # Set Storage Type accordingly
        if (depth <= 12):  # If the depth is less than 12
            subStorage = "12-inch Deep - "
        elif (depth <= 18):
            subStorage = "18-inch Deep - "
        elif (depth <= 24):
            subStorage = "24-inch Deep - "
        if (width <= 36):
            subStorage += "36-inch Wide Shelf"
        elif (width <= 48):
            subStorage += "48-inch Wide Shelf"

    return storageType, subStorage # Return the Values