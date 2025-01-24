from tqdm import tqdm
import pandas as pd
import numpy as np
import math
import openpyxl
import utilsExe

totalDaysOfData = 300    # Total Days in Dataset
redHot1SaleTP = 1        # 1 Sell per 1 day
red1SaleTP =  7          # 1 sell per 7 days (1 week)   
orange1SaleTP = 14       # 1 sell per 14 days  (2 weeks) 
yellow1SaleTP = 21       # 1 sell per 21 days  (3 weeks)
green1SaleTP = 30        # 1 sell per 30 days  (1 month)
blue1SaleTP = float("inf")     # 1 sell per 300 Days (~Rest of Data)

zones = {
    'Red Hot': totalDaysOfData/redHot1SaleTP,
    'Red': totalDaysOfData/red1SaleTP,
    'Orange': totalDaysOfData/orange1SaleTP,
    'Yellow': totalDaysOfData/yellow1SaleTP,
    'Green': totalDaysOfData/green1SaleTP,
    'Blue': totalDaysOfData/blue1SaleTP
}

fillFactor = 0.7
tirePercent = 0.5
vendor = 'FOR'

def readFiles(dimenFile, soldFile1, soldFile2, invenFile, dimenVendorCol, sold1VendorCol, sold2VendorCol, invenVendorCol, filterVendor):
    df_dimenFile = utilsExe.read_excel(dimenFile)      
    if filterVendor: df_dimenFile = df_dimenFile[(df_dimenFile[dimenVendorCol] == filterVendor)].reset_index()
    df_soldFile1 = utilsExe.read_excel(soldFile1)
    if filterVendor: df_soldFile1 = df_soldFile1[(df_soldFile1[sold1VendorCol] == filterVendor)].reset_index()
    df_soldFile2 = utilsExe.read_excel(soldFile2)
    if filterVendor: df_soldFile2 = df_soldFile2[(df_soldFile2[sold2VendorCol] == filterVendor)].reset_index()
    df_Inven = utilsExe.read_excel(invenFile)
    if filterVendor: df_Inven = df_Inven[(df_Inven[invenVendorCol] == filterVendor)].reset_index()
    return df_dimenFile, df_soldFile1, df_soldFile2, df_Inven

def makeFinalData(df_dimenFile, df_soldFile1, df_soldFile2, df_Inven, dimenCols, sold1Cols, sold2Cols, invenCols, drop0Dims):
    df_Main = pd.DataFrame({
        'Part#': df_dimenFile[dimenCols['Part# Column']],
        'Part Desc.': df_dimenFile[dimenCols['Desc. Column']],
        'Part Category': "",
        'Sold 1': 0,
        'Sold 2': 0,
        'Total Sold': 0,
        'OH Inventory': 0,
        'SKU Count': 0,
        '0Dimensions': False,
        'Depth': df_dimenFile[dimenCols['Depth Column']],
        'Width': df_dimenFile[dimenCols['Width Column']],
        'Height': df_dimenFile[dimenCols['Height Column']],
        'Zone': "",
        'StorageType': "",
        'SubStorage': "",
        'Bin Type': "",
        'Num. Bin Required': 0,
        'Actual Bin Allocation': "",
        'Overflow Bins': "",
        'Overflow Comment': "",
        'Bin Location': ""
    })


    # # * Insert the Rows from other Files
    oh_dict = df_soldFile1.set_index(sold1Cols['Part# Column'])[sold1Cols['Sold Column']].to_dict()
    df_Main['Sold 1'] = df_Main['Part#'].map(oh_dict)

    oh_dict = df_soldFile2.set_index(sold2Cols['Part# Column'])[sold2Cols['Sold Column']].to_dict()
    df_Main['Sold 2'] = df_Main['Part#'].map(oh_dict)

    oh_dict = df_Inven.set_index(invenCols['Part# Column'])[invenCols['Inventory Column']].to_dict()
    df_Main['OH Inventory'] = df_Main['Part#'].map(oh_dict)
    oh_dict = df_Inven.set_index(invenCols['Part# Column'])[invenCols['Bin Column']].to_dict()
    df_Main['Bin Location'] = df_Main['Part#'].map(oh_dict)


    # Process and Clean
    # Drop rows with Sold and Inventory 'nan'
    df_Main = df_Main.dropna(subset=["Sold 1", "Sold 2", "OH Inventory"], how="all").reset_index(drop=True)
    # Set 0Dimensions
    df_Main.loc[(df_Main["Depth"] == 0) | (df_Main["Height"] == 0) | (df_Main["Width"] == 0), "0Dimensions"] = True
    # Drop 0Dimensions Rows if drop0Dims
    if drop0Dims: df_Main = df_Main[df_Main["0Dimensions"] == False]
    # Remove Alphanumeric Strings
    df_Main['OH Inventory'] = pd.to_numeric(df_Main['OH Inventory'], errors='coerce')
    df_Main['Sold 1'] = pd.to_numeric(df_Main['Sold 1'], errors='coerce')
    df_Main['Sold 2'] = pd.to_numeric(df_Main['Sold 2'], errors='coerce')
    # Fill 'nan' with 0 and convert to float
    df_Main['Sold 1'] = df_Main['Sold 1'].fillna(0).astype(float)
    df_Main['Sold 2'] = df_Main['Sold 2'].fillna(0).astype(float)
    df_Main['Total Sold'] = df_Main['Total Sold'].fillna(0).astype(float)
    df_Main['OH Inventory'] = df_Main['OH Inventory'].fillna(0).astype(float)
    # Set and Sort by Total_Sold
    df_Main["Total Sold"] = df_Main["Sold 1"].astype(float) + df_Main["Sold 2"].astype(float)
    df_Main = df_Main.sort_values('Total Sold', ascending=False)
    # ^ Add Random Values for SKU Count temporarily
    df_Main["SKU Count"] = np.random.choice(np.arange(20), size=len(df_Main), replace=True)
    return df_Main

def part_categorization(df_toBeCategorized, categoryColName):
    # TODO: Add more categories
    for i in range(df_toBeCategorized.shape[0]):
        desc = "-".join(df_toBeCategorized.loc[i, "Part Desc."].split("-")[1:])
        pnum = df_toBeCategorized.loc[i, "Part#"][1:].upper()
        category = ""
        if "battery" in desc.lower():
            if desc.strip().lower() == "battery":
                category = "Battery"
            else:
                category = "Battery Accessory"
        elif "tire" in desc.lower():
            if desc.strip().lower() == "tire":
                category = "Tire"
            else:
                category = "Tire Accessory"            
        elif "hood" in desc.lower():
            if (desc.strip().lower() == "hood asy") | (desc.strip().lower() == "hood  asy"):
                category = "Hood"
            else:
                category = "Hood Accessory"
                
        elif (desc.strip().lower() == "cover"):
            category = "Bumper Cover"
        elif ("17D957" in pnum) | ("17K835" in pnum):
            category = "Bumper Cover"
        elif desc.strip().lower() == "seal":
            category = "Seal"
        elif desc.strip().lower() == "name plate":
            category = "Name Plate"
        elif desc.strip().lower() == "v-belt":
            category = "V-Belt"
        elif desc.strip().lower() == "v-belt":
            category = "V-Belt"
       
        elif ("blade" in desc.lower()) & ("wiper" in desc.lower()):
            category = "Wiper Blade"        
        elif ("arm" in desc.lower()) & ("wiper" in desc.lower()):
            category = "Wiper Arm"
        elif ("belt" in desc.lower()) & ("retractor" not in desc.lower()) & ("hole" not in desc.lower()) & ("cover" not in desc.lower()):
            category = "Belt"
        # elif ("hose" in desc.lower()) & ("vent" not in desc.lower()) & ("connect" not in desc.lower() & ("radiator" not in desc.lower()& ("heater" not in desc.lower()):
        #     category = "Hose"

        df_toBeCategorized.loc[i, categoryColName] = category
        

def Apply_Zoning(df_toBeZoned, zones, soldColName='Total Sold', zoneColName='Zone'): 
    df_toBeZoned.loc[:, zoneColName] = df_toBeZoned[soldColName].apply(lambda x: next((zone for zone, ratio in zones.items() if x >= ratio), list(zones.keys())[-1]))
    df_toBeZoned.loc[df_toBeZoned[soldColName] < 0, zoneColName] = None

def getNumOfBin(depth, width, height, raw_bin_dim, ohInven, fillFactor):
    # * Raw Bin Dimensions has this format :-  Height_Depth_Width
    if (raw_bin_dim != "") and (ohInven > 0):
        bin_height = float(raw_bin_dim.split("_")[1])
        bin_depth = float(raw_bin_dim.split("_")[2])
        bin_width = float(raw_bin_dim.split("_")[3])

        if raw_bin_dim.split("_")[0] == "BR":   # * Battery Rack
            return round((ohInven * width) / bin_depth, 3)      
               
        volBin = fillFactor * bin_height * bin_depth * bin_width    # * Available Storage Space
        volPart = height * depth * width
        if (volBin == 0):
            return 0
        
        numOfBins = round((ohInven * volPart) / volBin, 3)      # * Returns Fraction. 
        return numOfBins
    else:
        return 0


# ### Main Function for Storage Assignment


def getStorage(zone, pcate, depth, width, height, ohInven, fillFactor):
    # Initialize the empty Variables
    storageType = ""
    subStorage = ""

    if zone == "":
        return storageType, subStorage, "", 0 # Return the Values 

    isSpec, storageType, subStorage, raw_bin_dim = utilsExe.getSpecialtyStorage(pcate, depth, width, height)

    if not isSpec: 
        if (zone == "Red Hot") | (zone == "Red"):
            storageType, subStorage, raw_bin_dim = utilsExe.getRedHotStorage(depth, width, height)
        elif (zone == "Orange") | (zone == "Yellow"):
            storageType, subStorage, raw_bin_dim = utilsExe.getOrangeYellowStorage(depth, width, height)
        elif (zone == "Green") | (zone == "Blue"):   
            storageType, subStorage, raw_bin_dim = utilsExe.getGreenBlueStorage(depth, width, height)
 
    numOfBins = getNumOfBin(depth, width, height, raw_bin_dim, ohInven, fillFactor)
    binDim = ""

    # * Build Bin Label with C (Clip), B (Bulk), D (Drawer), Battery Rack (BR), Tire Rack (TR) and Width-Depth-Height
    if raw_bin_dim.strip():   
        binDim =  raw_bin_dim.split('_')[0] + raw_bin_dim.split('_')[3] + raw_bin_dim.split('_')[2] + raw_bin_dim.split('_')[1]
    

    return storageType, subStorage, binDim, numOfBins # Return the Values


def applyStorage(df_Main):
    for i in tqdm(range(df_Main.shape[0]), desc="Completion"):
    #for i in range(df_Main.shape[0]):
        depth = df_Main.loc[i, "Depth"]
        height = df_Main.loc[i, "Height"]
        width = df_Main.loc[i, "Width"]

        zone = df_Main.loc[i, "Zone"]
        pcate = df_Main.loc[i, "Part Category"]
        ohInven = df_Main.loc[i, "OH Inventory"]

        # * If any dimension is zero, set empty Storage
        if df_Main.loc[i, "0Dimensions"] == True:
            df_Main.loc[i, "StorageType"] = ""
            df_Main.loc[i, "SubStorage"] = ""
            continue

        # Set Storage of the Parts
        df_Main.loc[i, "StorageType"], df_Main.loc[i, "SubStorage"], df_Main.loc[i, "Bin Type"], df_Main.loc[i, "Num. Bin Required"] = getStorage(zone, pcate, depth, width, height, ohInven, fillFactor)


    for hangingPN in tqdm(df_Main.loc[df_Main['StorageType'] == 'Hanging Specialty Storage', "Part#"], "Completion"): # Get Hanging Parts
        df_Main.loc[(df_Main['Part#'] == hangingPN), "SubStorage"], df_Main.loc[(df_Main['Part#'] == hangingPN), "Bin Type"], hookDiv = ("6-inch Hook", "HS06", 10) if df_Main.loc[(df_Main['Part#'] == hangingPN), "SKU Count"].values[0] <= 10 else ("12-inch Hook", "HS12", 20)
        df_Main.loc[(df_Main['Part#'] == hangingPN), "Num. Bin Required"] = int(df_Main.loc[(df_Main['Part#'] == hangingPN), "OH Inventory"].values[0])  # * Set No. of Hooks = Inventory Count
    df_Main.loc[df_Main['StorageType'] != 'Hanging Specialty Storage', "SKU Count"] = 0


    carousel_model = ''
    if df_Main[df_Main['StorageType'] == 'Tire Specialty Storage'].shape[0] > 0: 
        carousel_model = 'TR72' if df_Main[df_Main['StorageType'] == 'Tire Specialty Storage'][df_Main['SubStorage'] == '33-inches Dia'].shape[0] / df_Main[df_Main['StorageType'] == 'Tire Specialty Storage'].shape[0] >= tirePercent else 'TR48'
        carousel_width = 72 if df_Main[df_Main['StorageType'] == 'Tire Specialty Storage'][df_Main['SubStorage'] == '33-inches Dia'].shape[0] / df_Main[df_Main['StorageType'] == 'Tire Specialty Storage'].shape[0] >= tirePercent else 48
        for tirePN in df_Main.loc[df_Main['StorageType'] == 'Tire Specialty Storage', "Part#"]:
            df_Main.loc[(df_Main['Part#'] == tirePN), "Num. Bin Required"] = round(int(df_Main.loc[(df_Main['Part#'] == tirePN), "OH Inventory"].values[0]) / (carousel_width // int(df_Main.loc[(df_Main['Part#'] == tirePN), "Width"].values[0])), 3)
            df_Main.loc[(df_Main['Part#'] == tirePN), "Bin Type"] = carousel_model





def applyZoningStorageFunc(config):
    df_dimenFile, df_soldFile1, df_soldFile2, df_Inven = readFiles(config['Dimensions Config']['File Path'], config['Sold File 1 Config']['File Path'], config['Sold File 2 Config']['File Path'], config['Inventory Config']['File Path'], config['Dimensions Config']['Columns']['Vendor Column'], config['Sold File 1 Config']['Columns']['Vendor Column'], config['Sold File 2 Config']['Columns']['Vendor Column'], config['Inventory Config']['Columns']['Vendor Column'], vendor)
    df_Main = makeFinalData(df_dimenFile, df_soldFile1, df_soldFile2, df_Inven, config['Dimensions Config']['Columns'], config['Sold File 1 Config']['Columns'], config['Sold File 2 Config']['Columns'], config['Inventory Config']['Columns'], config['Drop 0 Dimensions'])
    #part_categorization(df_Main, 'Part Category')
    Apply_Zoning(df_Main, zones, 'Total Sold', 'Zone')
    applyStorage(df_Main)
    df_Main.to_excel('Final_Dataset.xlsx', index=False) 
    
    