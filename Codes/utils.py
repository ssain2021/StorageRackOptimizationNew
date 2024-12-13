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
        sheet_name (int): Index of the sheet in the Excel file.
    
    Returns:
        pandas.DataFrame: A DataFrame containing the data from the specified Excel sheet.
    
    Raises:
        FileNotFoundError: If the specified file does not exist.
        pd.errors.EmptyDataError: If the file is empty.
        pd.errors.ParserError: If there's an error parsing the file.
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


def getSpecialtyStorage(pdesc, depth, width, height) -> str:
    """
    Determines if an item requires special storage and assigns appropriate storage type.
    
    Args:
        pdesc (str): Part description.
        depth (int): Depth of the item.
        width (int): Width of the item.
        height (int): Height of the item.
    
    Returns:
        tuple: (isSpec, storageType, subStorage, raw_bin_dim)
    """
    isSpec, storageType, subStorage, raw_bin_dim = _getSpecialtyStorage(pdesc, depth, width, height)
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
        if (depth <= 96) & (height >= 12) & (width <= 96):
            storageType = "Bulk Storage" # Set Storage Type accordingly
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

    for width, depth in [[width, depth], [depth, width]]:
        if (depth <= 24) & (height <= 15) & (width <= 48): # For Clip Shelving:
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

    # For BULK STORAGE
    for width, depth in [[width, depth], [depth, width]]:
        if (depth <= 96) & (height >= 12) & (width <= 96): # For Bulk Shelving
            storageType = "Bulk Storage" # Set Storage Type accordingly
            raw_bin_dim = "B_48_"
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
    
    # For Bulk Shelving
    for width, depth in [[width, depth], [depth, width]]:
        if (depth <= 96) & (height >= 12) & (width <= 96): # For Bulk Shelving
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
    
        # For Clip Shelving:
    for width, depth in [[width, depth], [depth, width]]:
        if (depth <= 24) & (height <= 15) & (width <= 48): # For Clip Shelving:
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

    return storageType, subStorage, raw_bin_dim # Return the Values





def _getSpecialtyStorage(pdesc, depth, width, height):
    # Initialize the empty Variables
    storageType = ""
    subStorage = ""
    raw_bin_dim = ""

    # Parsing for Battery
    if pdesc.split("-")[-1].strip().lower() == "battery":
        storageType = "Battery Specialty Storage"
        subStorage = "48-inch Deep- 48-inch Wide- 3-Level Sloped Shelving"
        raw_bin_dim = f"BR_16_48_48"
    # Parsing for Tire   TIRE  has Liner Stacking. Only Width Of Rack and Width Of Tire Considered
    elif pdesc.split("-")[-1].strip().lower() == "tire":
        storageType = "Tire Specialty Storage"
        raw_bin_dim = f"TR_0_0_0"
        if depth > 33:
            subStorage = "33-inches Dia"
        elif depth <= 28:
            subStorage = "28-inches Dia"
        else:
            subStorage = "28-33-inches Dia"
    # Parsing for Bumper Cover    bulk rack size of 72" deep, x 96" wide x height 48
    #elif ("Bumper" in pdesc) & ("Cover" in pdesc):
    elif (pdesc.split("-")[-1].strip().lower() == "cover"):
        storageType = "Bumper Cover Specialty Storage"
        subStorage = ""
        raw_bin_dim = f"BC_48_96_72"       ## BC_Height_Width_Depth 
    # For Hanging Storage
    elif ((depth >= 24) & (width <= 4) & (height <= 4)) | ((depth <= 4) & (width <= 4) & (height >= 24)) | ((depth <= 4) & (height <= 4) & (width >= 24)) :
        storageType = "Hanging Specialty Storage"
        raw_bin_dim = f"HS_0_0_0"
        # TODO: Clarify to get the SKU Count and Fix this
        skuCount = 10
        if skuCount <= 10: 
            subStorage = "6-inch Hooks"
        elif 10 < skuCount <= 20:
            subStorage = "12-inch Hooks"
    else:
        return False, storageType, subStorage, raw_bin_dim

    return True, storageType, subStorage, raw_bin_dim





########  OLD CODE HERE

# def calculate_max_parts(shelf_depth, shelf_width, shelf_height, part_depth, part_width, part_height):
#     print(f"Initial call: shelf_depth={shelf_depth}, shelf_width={shelf_width}, shelf_height={shelf_height}, "
#           f"part_depth={part_depth}, part_width={part_width}, part_height={part_height}")

#     if (part_depth * part_width * part_height) > (shelf_depth * shelf_width * shelf_height):
#         print("Returning 0 due to invalid dimensions")
#         return 0, None

#     def calculate_parts_for_orientation(orientation):
#         print(f"Calculating for orientation: {orientation}")
#         if orientation == 'depth':
#             if (part_depth > shelf_depth) or (part_width > shelf_width) or (part_height > shelf_height): return 0
#             base_parts = ((shelf_depth // part_depth) * (shelf_width // part_width)) * (shelf_height // part_height)
#             print(f"Base parts for depth: {base_parts}")
#             additional_parts1, best_orient = calculate_max_parts(shelf_depth % part_depth, shelf_width, shelf_height, part_depth, part_width, part_height)
#             additional_parts2, best_orient = calculate_max_parts(shelf_depth, shelf_width % part_width, shelf_height, part_depth, part_width, part_height)
#             additional_parts3, best_orient = calculate_max_parts(shelf_depth, shelf_width, shelf_height % part_height, part_depth, part_width, part_height)
#             print(f"Additional parts for depth: {additional_parts1}, {additional_parts2}, {additional_parts3}")
#             return base_parts + max(additional_parts1, additional_parts2, additional_parts3)
#         elif orientation == 'height':
#             if (part_height > shelf_depth) or (part_width > shelf_width) or (part_depth > shelf_height): return 0
#             base_parts = ((shelf_depth // part_height) * (shelf_width // part_width)) * (shelf_height // part_depth)
#             print(f"Base parts for height: {base_parts}")
#             additional_parts1, best_orient = calculate_max_parts(shelf_depth % part_height, shelf_width, shelf_height, part_depth, part_width, part_height)
#             additional_parts2, best_orient = calculate_max_parts(shelf_depth, shelf_width % part_width, shelf_height, part_depth, part_width, part_height)
#             additional_parts3, best_orient = calculate_max_parts(shelf_depth, shelf_width, shelf_height % part_depth, part_depth, part_width, part_height)
#             print(f"Additional parts for height: {additional_parts1}, {additional_parts2}, {additional_parts3}")
#             return base_parts + max(additional_parts1, additional_parts2, additional_parts3)
#         elif orientation == 'width':
#             if (part_width > shelf_depth) or (part_depth > shelf_width) or (part_height > shelf_height): return 0
#             base_parts = ((shelf_depth // part_width) * (shelf_width // part_depth)) * (shelf_height // part_height)
#             print(f"Base parts for width: {base_parts}")
#             additional_parts1, best_orient = calculate_max_parts(shelf_depth % part_width, shelf_width, shelf_height, part_depth, part_width, part_height)
#             additional_parts2, best_orient = calculate_max_parts(shelf_depth, shelf_width % part_depth, shelf_height, part_depth, part_width, part_height)
#             additional_parts3, best_orient = calculate_max_parts(shelf_depth, shelf_width, shelf_height % part_height, part_depth, part_width, part_height)
#             print(f"Additional parts for width: {additional_parts1}, {additional_parts2}, {additional_parts3}")
#             return base_parts + max(additional_parts1, additional_parts2, additional_parts3)
#         elif orientation == 'depth_height':
#             if (part_depth > shelf_depth) or (part_height > shelf_width) or (part_width > shelf_height): return 0
#             base_parts = ((shelf_depth // part_depth) * (shelf_width // part_height)) * (shelf_height // part_width)
#             print(f"Base parts for depth_height: {base_parts}")
#             additional_parts1, best_orient = calculate_max_parts(shelf_depth % part_depth, shelf_width, shelf_height, part_depth, part_width, part_height)
#             additional_parts2, best_orient = calculate_max_parts(shelf_depth, shelf_width % part_height, shelf_height, part_depth, part_width, part_height)
#             additional_parts3, best_orient = calculate_max_parts(shelf_depth, shelf_width, shelf_height % part_width, part_depth, part_width, part_height)
#             print(f"Additional parts for depth_height: {additional_parts1}, {additional_parts2}, {additional_parts3}")
#             return base_parts + max(additional_parts1, additional_parts2, additional_parts3)
#         elif orientation == 'depth_width':
#             if (part_height > shelf_depth) or (part_depth > shelf_width) or (part_width > shelf_height): return 0
#             base_parts = ((shelf_depth // part_height) * (shelf_width // part_depth)) * (shelf_height // part_width)
#             print(f"Base parts for depth_width: {base_parts}")
#             additional_parts1, best_orient = calculate_max_parts(shelf_depth % part_height, shelf_width, shelf_height, part_depth, part_width, part_height)
#             additional_parts2, best_orient = calculate_max_parts(shelf_depth, shelf_width % part_height, shelf_height, part_depth, part_width, part_height)
#             additional_parts3, best_orient = calculate_max_parts(shelf_depth, shelf_width, shelf_height % part_width, part_depth, part_width, part_height)
#             print(f"Additional parts for depth_width: {additional_parts1}, {additional_parts2}, {additional_parts3}")
#             return base_parts + max(additional_parts1, additional_parts2, additional_parts3)
#         elif orientation == 'height_width':
#             if (part_width > shelf_depth) or (part_height > shelf_width) or (part_depth > shelf_height): return 0
#             base_parts = ((shelf_depth // part_width) * (shelf_width // part_height)) * (shelf_height // part_depth)
#             print(f"Base parts for height_width: {base_parts}")
#             additional_parts1, best_orient = calculate_max_parts(shelf_depth % part_width, shelf_width, shelf_height, part_depth, part_width, part_height)
#             additional_parts2, best_orient = calculate_max_parts(shelf_depth, shelf_width % part_height, shelf_height, part_depth, part_width, part_height)
#             additional_parts3, best_orient = calculate_max_parts(shelf_depth, shelf_width, shelf_height % part_depth, part_depth, part_width, part_height)
#             print(f"Additional parts for height_width: {additional_parts1}, {additional_parts2}, {additional_parts3}")
#             return base_parts + max(additional_parts1, additional_parts2, additional_parts3)

#     orientations = ['depth', 'height', 'width', 'depth_height', 'depth_width', 'height_width']
    
#     max_parts = 0
#     best_orientation = None
    
#     for orientation in orientations:
#         parts = calculate_parts_for_orientation(orientation)
#         print(f"Total parts for {orientation}: {parts}")
#         if parts > max_parts:
#             max_parts = parts
#             best_orientation = orientation
    
#     print(f"Final result: Max parts = {max_parts}, Best orientation = {best_orientation}")
#     return max_parts, best_orientation

# # Example usage
# shelf_depth = 12
# shelf_width = 48
# shelf_height = 12
# part_depth = 8
# part_width = 8
# part_height = 2

# max_parts, best_orientation = calculate_max_parts(shelf_depth, shelf_width, shelf_height, part_depth, part_width, part_height)

# print(f"\nMaximum number of parts: {max_parts}")
# print(f"Best orientation: {best_orientation}")




# def calculate_max_parts(shelf_depth, shelf_width, shelf_height, part_depth, part_width, part_height):
#     def calculate_base_parts(orientation):
#         if orientation == 'depth':
#             return ((shelf_depth // part_depth) * (shelf_width // part_width)) * (shelf_height // part_height)
#         elif orientation == 'height':
#             return ((shelf_depth // part_height) * (shelf_width // part_width)) * (shelf_height // part_depth)
#         elif orientation == 'width':
#             return ((shelf_depth // part_width) * (shelf_width // part_depth)) * (shelf_height // part_height)
#         elif orientation == 'depth_height':
#             return ((shelf_depth // part_depth) * (shelf_width // part_height)) * (shelf_height // part_width)
#         elif orientation == 'depth_width':
#             return ((shelf_depth // part_depth) * (shelf_width // part_width)) * (shelf_height // part_height)
#         elif orientation == 'height_width':
#             return ((shelf_depth // part_height) * (shelf_width // part_width)) * (shelf_height // part_depth)
#         elif orientation == 'width_depth':
#             return ((shelf_depth // part_width) * (shelf_width // part_depth)) * (shelf_height // part_height)
#         elif orientation == 'width_height':
#             return ((shelf_depth // part_width) * (shelf_width // part_height)) * (shelf_height // part_depth)
    
        
#     orientations = ['depth', 'height', 'width', 'depth_height', 'depth_width', 'height_width']
    
#     max_parts = 0
#     best_orientation = None
    
#     for orientation in orientations:
#         base_parts = calculate_base_parts(orientation)
        
#         total_parts = base_parts
        
#         if total_parts > max_parts:
#             max_parts = total_parts
#             best_orientation = orientation
    
#     return max_parts, best_orientation








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