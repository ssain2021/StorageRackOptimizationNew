################################  utils.py  ####################################
# Author: Sukhendu Sain
# Description: Utils file of Zone Mapping and Storage Assignment of Warehouse Parts.
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
    
#def getTireCarouselModel():


def getRedHotStorage(depth: int, width: int, height: int) -> str:
    """

    """
    storageType, subStorage, raw_bin_dim = _getRedHotStorage(depth, width, height)
    return storageType, subStorage, raw_bin_dim

def getOrangeStorage(depth: int, width: int, height: int) -> str:
    """

    """
    storageType, subStorage, raw_bin_dim = _getOrangeStorage(depth, width, height)
    return storageType, subStorage, raw_bin_dim


def getYellowStorage(depth: int, width: int, height: int) -> str:
    """

    """
    storageType, subStorage, raw_bin_dim = _getYellowStorage(depth, width, height)
    return storageType, subStorage, raw_bin_dim


def getGreenStorage(depth: int, width: int, height: int) -> str:
    """

    """
    storageType, subStorage, raw_bin_dim = _getGreenStorage(depth, width, height)
    return storageType, subStorage, raw_bin_dim


def getBlueStorage(depth: int, width: int, height: int) -> str:
    """

    """
    storageType, subStorage, raw_bin_dim = _getBlueStorage(depth, width, height)
    return storageType, subStorage, raw_bin_dim


def getSpecialityStorage(pdesc, depth, width, height) -> str:
    """

    """
    isSpec, storageType, subStorage, raw_bin_dim = _getSpecialityStorage(pdesc, depth, width, height)
    return isSpec, storageType, subStorage, raw_bin_dim

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
    # ^ Raw Bin Dimensions has this format :-  Height_Depth_Width
    raw_bin_dim = ""

    # Start of High Density Drawers 
    if (depth <= 24) & (height <= 6) & (width <= 12):
        storageType = "High Density Drawers" # Set Storage Type accordingly
        raw_bin_dim = "06_24_"
        if (width <= 8): # If the width is less than 8
            subStorage = "48-inch Wide Drawer - 6 Compart"
            raw_bin_dim += "48"
        elif (width <= 9): 
            subStorage = "36-inch Wide Drawer - 4 Compart"
            raw_bin_dim += "36"
        elif (width <= 12):
            subStorage = "48-inch Wide Drawer - 4 Compart"
            raw_bin_dim += "48"
    # Start of Clip Shelving
    elif (depth <= 24) & (height <= 15) & (width <= 48):
        storageType = "Clip Shelving" # Set Storage Type accordingly
        raw_bin_dim = "15_"
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
    # Start of Bulk Storage        
    elif (depth <= 96) & (height >= 12) & (width <= 96):
        storageType = "Bulk Storage" # Set Storage Type accordingly
        raw_bin_dim = f"{height}_"
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

    return storageType, subStorage,  raw_bin_dim # Return the Values


def _getOrangeStorage(depth, width, height):
    # Initialize the empty Variables
    storageType = ""
    subStorage = ""
    raw_bin_dim = ""

    if (depth <= 24) & (height <= 15) & (width <= 48): # For Clip Shelving:
        storageType = "Clip Shelving" # Set Storage Type accordingly
        raw_bin_dim = "15_"
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
    elif (depth <= 96) & (height >= 12) & (width <= 96): # For Bulk Shelving
        storageType = "Bulk Storage" # Set Storage Type accordingly
        raw_bin_dim = f"{height}_"
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

    return storageType, subStorage, raw_bin_dim # Return the Values


def _getYellowStorage(depth, width, height):
    # Initialize the empty Variables
    storageType = ""
    subStorage = ""
    raw_bin_dim = ""

    if (depth <= 24) & (height <= 15) & (width <= 48): # For Clip Shelving:
        storageType = "Clip Shelving" # Set Storage Type accordingly
        raw_bin_dim = "15_"
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
    elif (depth <= 96) & (height >= 12) & (width <= 96): # For Bulk Shelving
        storageType = "Bulk Storage" # Set Storage Type accordingly
        raw_bin_dim = f"{height}_"
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

    return storageType, subStorage, raw_bin_dim # Return the Values


def _getGreenStorage(depth, width, height):
    # Initialize the empty Variables
    storageType = ""
    subStorage = ""
    raw_bin_dim = ""
    
    if (depth <= 96) & (height >= 12) & (width <= 96): # For Bulk Shelving
        storageType = "Bulk Storage" # Set Storage Type accordingly
        raw_bin_dim = f"{height}_"
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
    elif (depth <= 24) & (height <= 15) & (width <= 48): # For Clip Shelving:
        storageType = "Clip Shelving" # Set Storage Type accordingly
        raw_bin_dim = "15_"
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

    return storageType, subStorage, raw_bin_dim # Return the Values


def _getBlueStorage(depth, width, height):
    # Initialize the empty Variables
    storageType = ""
    subStorage = ""
    raw_bin_dim = ""
    
    if (depth <= 96) & (height >= 12) & (width <= 96): # For Bulk Shelving
        storageType = "Bulk Storage" # Set Storage Type accordingly
        raw_bin_dim = f"{height}_"
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
    elif (depth <= 24) & (height <= 15) & (width <= 48): # For Clip Shelving:
        storageType = "Clip Shelving" # Set Storage Type accordingly
        raw_bin_dim = "15_"
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

    return storageType, subStorage, raw_bin_dim # Return the Values


def _getSpecialityStorage(pdesc, depth, width, height):
    # Initialize the empty Variables
    storageType = ""
    subStorage = ""
    raw_bin_dim = ""

    # Parsing for Battery
    if pdesc.split("-")[-1].strip() == "Battery":
        storageType = "Battery Specialty Storage"
        subStorage = "48-inch Deep- 48-inch Wide- 3-Level Sloped Shelving"
        raw_bin_dim = f"{height}_48_48"
    # Parsing for Tire
    elif pdesc.split("-")[-1].strip() == "Tire":
        storageType = "Tire Specialty Storage"
        if depth > 33:
            subStorage = ">33-inches Wide"
           # raw_bin_dim = f""
        elif depth <= 28:
            subStorage = "<=28-inches Wide"
           # raw_bin_dim = f""
        else:
            subStorage = "28-33-inches Wide"
           # raw_bin_dim = f""
    # Parsing for Bumper Cover
    elif ("Bumper" in pdesc) & ("Cover" in pdesc):
        storageType = "Bumper Cover Specialty Storage"
        subStorage = ""
    # For Hanging Storage
    elif ((depth >= 24) & (width <= 4) & (height <= 4)) | ((depth <= 4) & (width <= 4) & (height >= 24)) | ((depth <= 4) & (height <= 4) & (width >= 24)) :
        storageType = "Hanging Speciality Storage"
        # TODO: Clarify to get the SKU Count and Fix this
        skuCount = 10
        if skuCount <= 10: 
            subStorage = "6-inch Hooks"
        elif 10 < skuCount <= 20:
            subStorage = "12-inch Hooks"
    else:
        return False, storageType, subStorage, raw_bin_dim

    return True, storageType, subStorage, raw_bin_dim







# ## BELOW IS OLD FUNCTION -- Main Function for Apply Zoning
# def Apply_Zoning(df_toBeZoned, Zones=['Red Hot', 'Orange', 'Yellow', 'Green', 'Blue'], thresMultiplier=0.2, soldColName='Sold', zoneColName='Zone', dataTDays=365):
#     # Initialize Variables
#     sold_sum = 0 # Keep sum of all Sold until now in the current zone
#     threshold = thresMultiplier * df_toBeZoned[soldColName].sum() # Threshold of Sum of Sold of each Zone
#     zoneIndex = 0 # Current Zone Index
#     zoneStartIndex = 0 # Current Zone Start Index of the Data

#     # Main Loop
#     for ind in range(df_toBeZoned.shape[0]): # Loop through each Data
#         if sold_sum > threshold: # Check if the Sum exceeds the threshold
#             df_toBeZoned.loc[zoneStartIndex:ind, zoneColName] = Zones[zoneIndex] # Set all the Rows from Current zoneStartIndex to now the Current Zone
#             zoneStartIndex = ind # Set the zoneStartIndex for next zone to the End of current zone
#             zoneIndex = zoneIndex + 1 # Increment the Zone Index
#             sold_sum = 0 # Reset the Sold Sum when the current zone ends
#         else: 
#             sold_sum = sold_sum + df_toBeZoned[soldColName].iloc[ind] # If not exceeding add Sold Sum to the Sold of the current row
#     df_toBeZoned.loc[df_toBeZoned[zoneColName] == "", zoneColName] = Zones[-1] #  Set all the leftoever empty zone Rows, to the Last Zone


# def oldDfMainMerge():

#     # It will have the Columns - 'Part Number', 'Part Desc.', 'Active', 'Sold (Pcs.)', '0Dimensions', 'Length/Depth', 'Width', 'Height', 'Zone', 'Storage Type', 'Sub Storage', 'Number of Storage needed'
#     # It will have all the rows with common part nos. from all 4 Files, having Appropriate Sold Pcs. Values, and Dimensions

#     main_list = []

#     gParts_PartNos = set(df_Gparts['Svc Part Number'])

#     # common_part_numbers = gParts_PartNos & set(df_Akins['Part#'])
#     # for pn, pddesc, ac, s, ld, w, h in zip(common_part_numbers, df_Gparts["Svc Part Number Description"], df_Gparts['Is Active?'], df_Akins['Sold Pcs '], df_Gparts['Prod Att - Length'], df_Gparts['Prod Att- Width'], df_Gparts['Prod Att - Height']):
#     #     main_list.append([pn, pddesc, "Akins", ac, s, False, ld, w, h, "", "", "", "",""])

#     common_part_numbers = gParts_PartNos & set(df_Wholesale['Part Number'])
#     for pn, pddesc, ac, s, ld, w, h in zip(common_part_numbers, df_Gparts["Svc Part Number Description"], df_Gparts['Is Active?'], df_Wholesale['Sold'], df_Gparts['Prod Att - Length'], df_Gparts['Prod Att- Width'], df_Gparts['Prod Att - Height']):
#         main_list.append([pn, pddesc, "", "Wholesale", ac, s, False, ld, w, h, "", "", "", "", ""])


#     common_part_numbers = gParts_PartNos & set(df_Service['* indicates a superseded part\nPart Number'])
#     for pn, pddesc, ac, s, ld, w, h in zip(common_part_numbers, df_Gparts["Svc Part Number Description"], df_Gparts['Is Active?'], df_Service['Qty Sold'], df_Gparts['Prod Att - Length'], df_Gparts['Prod Att- Width'], df_Gparts['Prod Att - Height']):
#         main_list.append([pn, pddesc, "", "Service", ac, s, False, ld, w, h, "", "", "", "", ""])

#     df_Main = pd.DataFrame(main_list)
#     df_Main.columns = ['Part#', 'Part Desc.', 'Part Category', 'DataSource', 'Active', 'Sold', '0Dimensions', 'Depth', 'Width', 'Height', 'Zone', 'StorageType', 'SubStorage', 'Num. Storage Required', "Bin Location"]
#     df_Main = df_Main.sort_values('Sold', ascending=False).reset_index()
#     df_Main["Zone"] = df_Main["Zone"].astype(str)
#     df_Main.loc[(df_Main["Depth"] == 0) | (df_Main["Height"] == 0) | (df_Main["Width"] == 0), "0Dimensions"] = True
#     df_Main = df_Main[df_Main["0Dimensions"] == False].reset_index()
#     df_Main.drop(['index', 'level_0'], axis=1, inplace=True)
#     #df_Main.drop(['index'], axis=1, inplace=True)

#     df_Main.shape[0], utils.print_df(df_Main)