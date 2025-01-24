################################  utils.py  ####################################
# Author: Sukhendu Sain
# Description: Utils file of Zone Mapping and Storage Assignment of Warehouse Parts.
# Data: 22-Nov-2024
#################################################################################


import pandas as pd
from tabulate import tabulate



def read_excel(file_path: str, sheet_name:int=0, header:int=0) -> pd.DataFrame:
    """
    Reads an Excel file and returns a Pandas DataFrame.
    
    Args:
        file_path (str): Path to the Excel file.
        sheet_name (int): Index of the sheet in the Excel file.
    
    Returns:
        pandas.DataFrame: A DataFrame containing the data from the specified Excel sheet.
    
    Raises:
        FileNotFoundError: If the specified file does not exist.
        pd.errors.EmptyDataError: If the file is empty.
        pd.errors.ParserError: If there's an error parsing the file.
    """
    df = _read_excel(file_path, sheet_name, header)
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
    Determines the storage type for Red Hot zone items.
    
    Args:
        depth (int): Depth of the item.
        width (int): Width of the item.
        height (int): Height of the item.
    
    Returns:
        tuple: (storageType, subStorage, raw_bin_dim)
    """
    storageType, subStorage, raw_bin_dim = _getRedHotStorage(depth, width, height)
    return storageType, subStorage, raw_bin_dim

def getOrangeYellowStorage(depth: int, width: int, height: int) -> str:
    """
    Determines the storage type for Orange and Yellow zone items.
    
    Args:
        depth (int): Depth of the item.
        width (int): Width of the item.
        height (int): Height of the item.
    
    Returns:
        tuple: (storageType, subStorage, raw_bin_dim)
    """
    storageType, subStorage, raw_bin_dim = _getOrangeYellowStorage(depth, width, height)
    return storageType, subStorage, raw_bin_dim


def getGreenBlueStorage(depth: int, width: int, height: int) -> str:
    """
    Determines the storage type for Green and Blue zone items.
    
    Args:
        depth (int): Depth of the item.
        width (int): Width of the item.
        height (int): Height of the item.
    
    Returns:
        tuple: (storageType, subStorage, raw_bin_dim)
    """
    storageType, subStorage, raw_bin_dim = _getGreenBlueStorage(depth, width, height)
    return storageType, subStorage, raw_bin_dim


def getSpecialtyStorage(pcate, depth, width, height) -> str:
    """
    Determines if an item requires special storage and assigns appropriate storage type.
    
    Args:
        pcate (str): Part Category.
        depth (int): Depth of the item.
        width (int): Width of the item.
        height (int): Height of the item.
    
    Returns:
        tuple: (isSpec, storageType, subStorage, raw_bin_dim)
    """
    isSpec, storageType, subStorage, raw_bin_dim = _getSpecialtyStorage(pcate, depth, width, height)
    return isSpec, storageType, subStorage, raw_bin_dim

def checkIfPartCanFitInBin(partHeight, partWidth, partDepth, binHeight, binWidth, binDepth):
    """
    """
    canFit = _checkIfPartCanFitInBin(partHeight, partWidth, partDepth, binHeight, binWidth, binDepth)
    return canFit

##################### FUNCTION INITS ##############################

def _read_excel(file_path, sheet_name, header):
    try:
        df = pd.read_excel(file_path, sheet_name, header=header)
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


def _getRedHotStorage(depth, width, height):         ## @ For Both Zones - Red Hot, and Red
    # Initialize the empty Variables
    storageType = ""
    subStorage = ""
    # ^  Client Rack Label - [D/C/B/BFR/TR/HS] Width-Depth-Height
    # ^ Raw_Bin_Dim has this format :-  Height_Depth_Width
    raw_bin_dim = ""

    for width, depth in [[width, depth], [depth, width]]:
        # Start of High Density Drawers 
        if (depth <= 24) & (height <= 6) & (width <= 12):
            storageType = "High Density Drawers" # Set Storage Type accordingly
            raw_bin_dim = "D_06_24_"
            if (width <= 8): # If the width is less than 8
                subStorage = "48-inch Wide Drawer - 6 Compart"
                raw_bin_dim += "48"
            elif (width <= 9): 
                subStorage = "36-inch Wide Drawer - 4 Compart"
                raw_bin_dim += "36"
            elif (width <= 12):
                subStorage = "48-inch Wide Drawer - 4 Compart"
                raw_bin_dim += "48"
        if raw_bin_dim != "":
            return storageType, subStorage,  raw_bin_dim
       
    for width, depth in [[width, depth], [depth, width]]:
        # Start of Clip Shelving
        if (depth <= 24) & (height <= 15) & (width <= 48):
            storageType = "Clip Shelving" # Set Storage Type accordingly
            raw_bin_dim = "C_15_"
            if (depth <= 12):  # If the depth is less than 12
                subStorage = "12-inch Deep - "
                raw_bin_dim += "12_"
            elif (depth <= 18):
                subStorage = "18-inch Deep - "
                raw_bin_dim += "18_"
            elif (depth <= 24):
                subStorage = "24-inch Deep - "
                raw_bin_dim += "24_"
            if (width <= 36):
                subStorage += "36-inch Wide Shelf"
                raw_bin_dim += "36"
            elif (width <= 48):
                subStorage += "48-inch Wide Shelf"
                raw_bin_dim += "48"
        if raw_bin_dim != "":
            return storageType, subStorage,  raw_bin_dim
 
    # Start of Bulk Storage        
    for width, depth in [[width, depth], [depth, width]]:
        #if (depth <= 96) & (height >= 12) & (width <= 96):         ### Removed Minimum Height criteria - 15-Dec
        if (depth <= 96) & (width <= 96):
            storageType = "Bulk Storage" # Set Storage Type accordingly
    # ^ Raw_Bin_Dim has this format :-  Height_Depth_Width
            raw_bin_dim = "B_48_"      ### ~  ASSUMPTION: BULK RACK HEIGHT LIMIT 48 Inches
            if (depth <= 24): # If the depth is less than 24
                subStorage = "24-inch Deep - "
                raw_bin_dim += "24_"
            elif (depth <= 36):
                subStorage = "36-inch Deep - "
                raw_bin_dim += "36_"
            elif (depth <= 42):
                subStorage = "42-inch Deep - "
                raw_bin_dim += "42_"
            elif (depth <= 48):
                subStorage = "48-inch Deep - "
                raw_bin_dim += "48_"
            elif (depth <= 72):
                subStorage = "72-inch Deep - "
                raw_bin_dim += "72_"
            elif (depth <= 96):
                subStorage = "96-inch Deep - "
                raw_bin_dim += "96_"
            if (width <= 48):
                subStorage += "48-inch Wide Shelf"
                raw_bin_dim += "48"
            elif (width <= 72):
                subStorage += "72-inch Wide Shelf"
                raw_bin_dim += "72"
            elif (width <= 96):
                subStorage += "96-inch Wide Shelf"
                raw_bin_dim += "96"
        if raw_bin_dim != "":
            return storageType, subStorage,  raw_bin_dim
        
    return storageType, subStorage,  raw_bin_dim # Return the Values


def _getOrangeYellowStorage(depth, width, height):
    # Initialize the empty Variables
    storageType = ""
    subStorage = ""
    raw_bin_dim = ""
# ^  Client Rack Label - [D/C/B/BFR/TR/HS] Width-Depth-Height
# ^ Raw_Bin_Dim has this format :-  Height_Depth_Width

        # ^ For Clip Shelving Storage 
    for width, depth in [[width, depth], [depth, width]]:
        if (depth <= 24) & (height <= 15) & (width <= 48): 
            storageType = "Clip Shelving" # Set Storage Type accordingly
            raw_bin_dim = "C_15_"
            if (depth <= 12):  # If the depth is less than equal to 12
                subStorage = "12-inch Deep - "
                raw_bin_dim += "12_"
            elif (depth <= 18):
                subStorage = "18-inch Deep - "
                raw_bin_dim += "18_"
            elif (depth <= 24):
                subStorage = "24-inch Deep - "
                raw_bin_dim += "24_"
            if (width <= 36):
                subStorage += "36-inch Wide Shelf"
                raw_bin_dim += "36"
            elif (width <= 48):
                subStorage += "48-inch Wide Shelf"
                raw_bin_dim += "48"
        if raw_bin_dim != "":
            return storageType, subStorage,  raw_bin_dim

    # ^ For BULK STORAGE
    for width, depth in [[width, depth], [depth, width]]:
    #    if (depth <= 96) & (height >= 12) & (width <= 96): # For Bulk Shelving
        if (depth <= 96)  & (width <= 96): # For Bulk Shelving  ## * Remove Minimum Height Checking - 15-Dec
            storageType = "Bulk Storage" # Set Storage Type accordingly
            raw_bin_dim = "B_48_"           ##  Height of BULK 
            if (depth <= 24): # If the depth is less than 24
                subStorage = "24-inch Deep - "
                raw_bin_dim += "24_"
            elif (depth <= 36):
                subStorage = "36-inch Deep - "
                raw_bin_dim += "36_"
            elif (depth <= 42):
                subStorage = "42-inch Deep - "
                raw_bin_dim += "42_"
            elif (depth <= 48):
                subStorage = "48-inch Deep - "
                raw_bin_dim += "48_"
            elif (depth <= 72):
                subStorage = "72-inch Deep - "
                raw_bin_dim += "72_"
            elif (depth <= 96):
                subStorage = "96-inch Deep - "
                raw_bin_dim += "96_"
            if (width <= 48):
                subStorage += "48-inch Wide Shelf"
                raw_bin_dim += "48"
            elif (width <= 72):
                subStorage += "72-inch Wide Shelf"
                raw_bin_dim += "72"
            elif (width <= 96):
                subStorage += "96-inch Wide Shelf"
                raw_bin_dim += "96"
        if raw_bin_dim != "":
            return storageType, subStorage,  raw_bin_dim

    return storageType, subStorage, raw_bin_dim # Return the Values



def _getGreenBlueStorage(depth, width, height):
    # Initialize the empty Variables
    storageType = ""
    subStorage = ""
    raw_bin_dim = ""
# ^  Client Rack Label - [D/C/B/BFR/TR/HS] Width-Depth-Height
# ^ Raw_Bin_Dim has this format :-  Height_Depth_Width
    
    # ^ For Bulk Shelving   ###   For GREEN  and BLUE Zone Parts - Only Assign BULK STorage  (No Need to Check Part Height)
#     for width, depth in [[width, depth], [depth, width]]:
#         if (depth <= 96) & (height >= 12) & (width <= 96): # For Bulk Shelving
#     #    if (depth <= 96)  & (width <= 96): # *  For Bulk Shelving  ##  Remove Minimum Height Checking - 15-Dec
#             storageType = "Bulk Storage" # Set Storage Type accordingly
#             raw_bin_dim = f"B_48_"
#             if (depth <= 24): # If the depth is less than 24
#                 subStorage = "24-inch Deep - "
#                 raw_bin_dim += "24_"
#             elif (depth <= 36):
#                 subStorage = "36-inch Deep - "
#                 raw_bin_dim += "36_"
#             elif (depth <= 42):
#                 subStorage = "42-inch Deep - "
#                 raw_bin_dim += "42_"
#             elif (depth <= 48):
#                 subStorage = "48-inch Deep - "
#                 raw_bin_dim += "48_"
#             elif (depth <= 72):
#                 subStorage = "72-inch Deep - "
#                 raw_bin_dim += "72_"
#             elif (depth <= 96):
#                 subStorage = "96-inch Deep - "
#                 raw_bin_dim += "96_"
#             if (width <= 48):
#                 subStorage += "48-inch Wide Shelf"
#                 raw_bin_dim += "48"
#             elif (width <= 72):
#                 subStorage += "72-inch Wide Shelf"
#                 raw_bin_dim += "72"
#             elif (width <= 96):
#                 subStorage += "96-inch Wide Shelf"
#                 raw_bin_dim += "96"
#         if raw_bin_dim != "":
#             return storageType, subStorage,  raw_bin_dim
    
# # ^ Raw_Bin_Dim has this format :-  Height_Depth_Width
#         # For Clip Shelving:
#     for width, depth in [[width, depth], [depth, width]]:
#         if (depth <= 24) & (height <= 15) & (width <= 48): # For Clip Shelving:
#             storageType = "Clip Shelving" # Set Storage Type accordingly
#             raw_bin_dim = "C_15_"
#             if (depth <= 12):  # If the depth is less than 12
#                 subStorage = "12-inch Deep - "
#                 raw_bin_dim += "12_"
#             elif (depth <= 18):
#                 subStorage = "18-inch Deep - "
#                 raw_bin_dim += "18_"
#             elif (depth <= 24):
#                 subStorage = "24-inch Deep - "
#                 raw_bin_dim += "24_"
#             if (width <= 36):
#                 subStorage += "36-inch Wide Shelf"
#                 raw_bin_dim += "36"
#             elif (width <= 48):
#                 subStorage += "48-inch Wide Shelf"
#                 raw_bin_dim += "48"
#         if raw_bin_dim != "":
#             return storageType, subStorage,  raw_bin_dim

    # ^ For Bulk Shelving - For parts not stacked in Clip Shelving--  Without  Minimum Height Checking - 15-Dec
    for width, depth in [[width, depth], [depth, width]]:
    #    if (depth <= 96) & (height >= 12) & (width <= 96): # For Bulk Shelving
        if (depth <= 96)  & (width <= 96): # *  For Bulk Shelving  ##  Remove 
            storageType = "Bulk Storage" # Set Storage Type accordingly
            raw_bin_dim = f"B_48_"
            if (depth <= 24): # If the depth is less than 24
                subStorage = "24-inch Deep - "
                raw_bin_dim += "24_"
            elif (depth <= 36):
                subStorage = "36-inch Deep - "
                raw_bin_dim += "36_"
            elif (depth <= 42):
                subStorage = "42-inch Deep - "
                raw_bin_dim += "42_"
            elif (depth <= 48):
                subStorage = "48-inch Deep - "
                raw_bin_dim += "48_"
            elif (depth <= 72):
                subStorage = "72-inch Deep - "
                raw_bin_dim += "72_"
            elif (depth <= 96):
                subStorage = "96-inch Deep - "
                raw_bin_dim += "96_"
            if (width <= 48):
                subStorage += "48-inch Wide Shelf"
                raw_bin_dim += "48"
            elif (width <= 72):
                subStorage += "72-inch Wide Shelf"
                raw_bin_dim += "72"
            elif (width <= 96):
                subStorage += "96-inch Wide Shelf"
                raw_bin_dim += "96"
        if raw_bin_dim != "":
            return storageType, subStorage,  raw_bin_dim

    return storageType, subStorage, raw_bin_dim # Return the Values





def _getSpecialtyStorage(pcate, depth, width, height):
    # Initialize the empty Variables
    storageType = ""
    subStorage = ""
    raw_bin_dim = ""

    # Parsing for Battery
    if pcate.lower() == "battery":
        storageType = "Battery Specialty Storage"
        subStorage = "48-inch Deep- 48-inch Wide- 3-Level Sloped Shelving"
        raw_bin_dim = f"BR_16_48_48"
    # Parsing for Tire   TIRE  has Liner Stacking. Only Width Of Rack and Width Of Tire Considered
    elif pcate.lower() == "tire":
        storageType = "Tire Specialty Storage"
        raw_bin_dim = f"TR_0_0_0"
        if depth > 33:
            subStorage = "33-inches Dia"
        elif depth <= 28:
            subStorage = "28-inches Dia"
        else:
            subStorage = "28-33-inches Dia"
    # Parsing for Bumper Cover    bulk rack size of 72" deep, x 96" wide x height 48
    elif (pcate.lower() == "bumper cover"):
        storageType = "Bumper Cover Specialty Storage"
        subStorage = "72-inch Deep- 96-inch Wide Bulk"
        raw_bin_dim = f"BC_48_72_96"       ## B_Height_Depth_Width 
    elif (pcate.lower() == "hood"):
        storageType = "Hood Assembly Specialty Storage"
        subStorage = "72-inch Deep- 96-inch Wide, 80-inch High Bulk"
        raw_bin_dim = f"BH_80_72_96"       ## B_Height_Depth_Width 
    # For Hanging Storage
    elif (pcate.lower() == "wiper blade") | (pcate.lower() == "wiper arm") | (pcate.lower() == "v-belt"):
        storageType = "Hanging Specialty Storage"
        raw_bin_dim = f"HS_0_0_0"  

    elif ((depth >= 24) & (width <= 4) & (height <= 4)) | ((depth <= 4) & (width <= 4) & (height >= 24)) | ((depth <= 4) & (height <= 4) & (width >= 24)) :
        storageType = "Hanging Specialty Storage"
        raw_bin_dim = f"HS_0_0_0"
    else:
        return False, storageType, subStorage, raw_bin_dim

    return True, storageType, subStorage, raw_bin_dim


def _checkIfPartCanFitInBin(partHeight, partWidth, partDepth, binHeight, binWidth, binDepth):
    for width, depth in [[binWidth, binDepth], [binDepth, binWidth]]:
        if (partDepth <= width) & (partHeight <= binHeight) & (partWidth <= depth): # For Clip Shelving:
            return True
    return False




