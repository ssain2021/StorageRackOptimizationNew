from tqdm import tqdm
from pandas import to_numeric, DataFrame, concat
from numpy import random
from math import floor
#import openpyxl
import utilsExe
from io import StringIO

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
    yield "Read Files Completion:     0%|    | 0/4"
    yield f"- Reading File: {dimenFile.split("/")[-1]} ... "
    df_dimenFile = utilsExe.read_excel(dimenFile)      
    if filterVendor: df_dimenFile = df_dimenFile[(df_dimenFile[dimenVendorCol] == filterVendor)].reset_index()
    yield f"- Reading File: {soldFile1.split("/")[-1]} ... "
    yield "Read Files Completion:     25%|#   | 1/4"
    df_soldFile1 = utilsExe.read_excel(soldFile1)
    if filterVendor: df_soldFile1 = df_soldFile1[(df_soldFile1[sold1VendorCol] == filterVendor)].reset_index()
    yield f"- Reading File: {soldFile2.split("/")[-1]} ... "
    yield "Read Files Completion:     50%|##  | 2/4"
    df_soldFile2 = utilsExe.read_excel(soldFile2)
    if filterVendor: df_soldFile2 = df_soldFile2[(df_soldFile2[sold2VendorCol] == filterVendor)].reset_index()
    yield f"- Reading File: {invenFile.split("/")[-1]} ... "
    yield "Read Files Completion:     75%|### | 3/4"
    df_Inven = utilsExe.read_excel(invenFile)
    if filterVendor: df_Inven = df_Inven[(df_Inven[invenVendorCol] == filterVendor)].reset_index()
    yield "- Reading all Files Done"
    yield "Read Files Completion:     100%|#####| 4/4"
    yield df_dimenFile, df_soldFile1, df_soldFile2, df_Inven

def makeFinalData(df_dimenFile, df_soldFile1, df_soldFile2, df_Inven, dimenCols, sold1Cols, sold2Cols, invenCols, drop0Dims):
    yield "Merged Dataset Creation Completion:     0%|          | 0/10"
    df_Main = DataFrame({
        'Part#': df_dimenFile[dimenCols['Part# Column']],
        'Part Desc.': df_dimenFile[dimenCols['Desc. Column']],
        'Part Category': "",
        'Wholesale Sold': 0,
        'Service Sold': 0,
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

    yield "Merged Dataset Creation Completion:     10%|#         | 2/20"

    # # * Insert the Rows from other Files
    oh_dict = df_soldFile1.set_index(sold1Cols['Part# Column'])[sold1Cols['Sold Column']].to_dict()
    df_Main['Sold 1'] = df_Main['Part#'].map(oh_dict)
    yield "Merged Dataset Creation Completion:     15%|#1        | 3/20"
    oh_dict = df_soldFile2.set_index(sold2Cols['Part# Column'])[sold2Cols['Sold Column']].to_dict()
    df_Main['Sold 2'] = df_Main['Part#'].map(oh_dict)
    yield "Merged Dataset Creation Completion:     20%|##        | 4/20"
    oh_dict = df_Inven.set_index(invenCols['Part# Column'])[invenCols['Inventory Column']].to_dict()
    df_Main['OH Inventory'] = df_Main['Part#'].map(oh_dict)
    yield "Merged Dataset Creation Completion:     25%|##1       | 5/20"
    oh_dict = df_Inven.set_index(invenCols['Part# Column'])[invenCols['Bin Column']].to_dict()
    df_Main['Bin Location'] = df_Main['Part#'].map(oh_dict)
    yield "Merged Dataset Creation Completion:     30%|###       | 6/20"


    # Process and Clean
    # Drop rows with Sold and Inventory 'nan'
    df_Main = df_Main.dropna(subset=["Sold 1", "Sold 2", "OH Inventory"], how="all").reset_index(drop=True)
    yield "- Dataset Created.. Processing/Cleaning the Data"
    yield "Merged Dataset Creation Completion:     40%|####      | 8/20"
    # Set 0Dimensions
    df_Main.loc[(df_Main["Depth"] == 0) | (df_Main["Height"] == 0) | (df_Main["Width"] == 0), "0Dimensions"] = True
    yield "Merged Dataset Creation Completion:     45%|####1     | 9/20"
    # Drop 0Dimensions Rows if drop0Dims
    if drop0Dims == "true": df_Main = df_Main[df_Main["0Dimensions"] == False]; yield "- Rows with 0 Dimensions dropped"
    # Remove Alphanumeric Strings
    df_Main['OH Inventory'] = to_numeric(df_Main['OH Inventory'], errors='coerce')
    yield "Merged Dataset Creation Completion:     50%|#####     | 10/20"
    df_Main['Sold 1'] = to_numeric(df_Main['Sold 1'], errors='coerce')
    yield "Merged Dataset Creation Completion:     55%|#####1    | 11/20"
    df_Main['Sold 2'] = to_numeric(df_Main['Sold 2'], errors='coerce')
    yield "Merged Dataset Creation Completion:     60%|######    | 12/20"
    # Fill 'nan' with 0 and convert to float
    df_Main['Sold 1'] = df_Main['Sold 1'].fillna(0).astype(float)
    yield "Merged Dataset Creation Completion:     65%|######1   | 13/20"
    df_Main['Sold 2'] = df_Main['Sold 2'].fillna(0).astype(float)
    yield "Merged Dataset Creation Completion:     70%|#######   | 14/20"
    df_Main['Total Sold'] = df_Main['Total Sold'].fillna(0).astype(float)
    yield "Merged Dataset Creation Completion:     75%|#######1  | 15/20"
    df_Main['OH Inventory'] = df_Main['OH Inventory'].fillna(0).astype(float)
    yield "Merged Dataset Creation Completion:     80%|########  | 16/20"
    # Set and Sort by Total_Sold
    df_Main["Total Sold"] = df_Main["Sold 1"] + df_Main["Sold 2"]
    df_Main = df_Main.sort_values('Total Sold', ascending=False).reset_index(drop=True)
    yield "Merged Dataset Creation Completion:     90%|######### | 18/20"
    # ^ Add Random Values for SKU Count temporarily
    df_Main["SKU Count"] = random.choice(range(20), size=len(df_Main), replace=True)
    yield "Merged Dataset Creation Completion:     100%|##########| 20/20"
    yield df_Main

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
        
        df_toBeCategorized.loc[i, categoryColName] = category
        

def Apply_Zoning(df_toBeZoned, zones, soldColName='Total Sold', zoneColName='Zone'): 
    df_toBeZoned.loc[:, zoneColName] = df_toBeZoned[soldColName].apply(lambda x: next((zone for zone, ratio in zones.items() if x >= ratio), list(zones.keys())[-1]))
    df_toBeZoned.loc[df_toBeZoned[soldColName] < 0, zoneColName] = None
    return df_toBeZoned['Zone'].value_counts()

def getNumOfBin(depth, width, height, raw_bin_dim, ohInven, fillFactor):
    if (raw_bin_dim != "") and (ohInven > 0):
        bin_height = float(raw_bin_dim.split("_")[1])
        bin_depth = float(raw_bin_dim.split("_")[2])
        bin_width = float(raw_bin_dim.split("_")[3])

        if raw_bin_dim.split("_")[0] == "BR":   # * Battery Rack
            return round((ohInven * width) / bin_depth, 3)      
               
        volBin = fillFactor * bin_height * bin_depth * bin_width
        volPart = height * depth * width
        if (volBin == 0):
            return 0
        
        numOfBins = round((ohInven * volPart) / volBin, 3)
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
    output = StringIO()
    for i in tqdm(range(df_Main.shape[0]), desc="Storage Apply Completion", file=output):
        yield output.getvalue().split('\r')[-1]
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
    yield "- Storage Allocated to Non-Specialty Parts... Starting Hanging Storage"

    for hangingPN in tqdm(df_Main.loc[df_Main['StorageType'] == 'Hanging Specialty Storage', "Part#"], desc="Hanging Storage Completion", file=output): # Get Hanging Parts
        yield output.getvalue().split('\r')[-1]
        df_Main.loc[(df_Main['Part#'] == hangingPN), "SubStorage"], df_Main.loc[(df_Main['Part#'] == hangingPN), "Bin Type"], hookDiv = ("6-inch Hook", "HS06", 10) if df_Main.loc[(df_Main['Part#'] == hangingPN), "SKU Count"].values[0] <= 10 else ("12-inch Hook", "HS12", 20)
        df_Main.loc[(df_Main['Part#'] == hangingPN), "Num. Bin Required"] = int(df_Main.loc[(df_Main['Part#'] == hangingPN), "OH Inventory"].values[0])  # * Set No. of Hooks = Inventory Count
    df_Main.loc[df_Main['StorageType'] != 'Hanging Specialty Storage', "SKU Count"] = 0
    yield "- Storage Allocated to Hanging Parts... Starting Tire Storage"

    carousel_model = ''
    if df_Main[df_Main['StorageType'] == 'Tire Specialty Storage'].shape[0] > 0: 
        carousel_model = 'TR72' if df_Main[df_Main['StorageType'] == 'Tire Specialty Storage'][df_Main['SubStorage'] == '33-inches Dia'].shape[0] / df_Main[df_Main['StorageType'] == 'Tire Specialty Storage'].shape[0] >= tirePercent else 'TR48'
        carousel_width = 72 if df_Main[df_Main['StorageType'] == 'Tire Specialty Storage'][df_Main['SubStorage'] == '33-inches Dia'].shape[0] / df_Main[df_Main['StorageType'] == 'Tire Specialty Storage'].shape[0] >= tirePercent else 48
        for tirePN in tqdm(df_Main.loc[df_Main['StorageType'] == 'Tire Specialty Storage', "Part#"], desc="Hanging Storage Completion", file=output):
            yield output.getvalue().split('\r')[-1]
            df_Main.loc[(df_Main['Part#'] == tirePN), "Num. Bin Required"] = round(int(df_Main.loc[(df_Main['Part#'] == tirePN), "OH Inventory"].values[0]) / (carousel_width // int(df_Main.loc[(df_Main['Part#'] == tirePN), "Width"].values[0])), 3)
            df_Main.loc[(df_Main['Part#'] == tirePN), "Bin Type"] = carousel_model





def applyZoningStorageFunc(config):
    df_dimenFile = df_soldFile1 = df_soldFile2 = df_Inven = None
    generator = readFiles(config['Dimensions Config']['File Path'], config['Sold File 1 Config']['File Path'], config['Sold File 2 Config']['File Path'], config['Inventory Config']['File Path'], config['Dimensions Config']['Columns']['Vendor Column'], config['Sold File 1 Config']['Columns']['Vendor Column'], config['Sold File 2 Config']['Columns']['Vendor Column'], config['Inventory Config']['Columns']['Vendor Column'], vendor)
    while True:
        try:
            message = next(generator)
            if type(message) == str:
                yield(message)
            else:
                df_dimenFile, df_soldFile1, df_soldFile2, df_Inven = message
        except StopIteration:
            break
    yield "Creating Merged Dataset.... ⚙️"
    #df_Main = None
    generator = makeFinalData(df_dimenFile, df_soldFile1, df_soldFile2, df_Inven, config['Dimensions Config']['Columns'], config['Sold File 1 Config']['Columns'], config['Sold File 2 Config']['Columns'], config['Inventory Config']['Columns'], config['Drop 0 Dimensions'])
    while True:
        try:
            message = next(generator)
            if type(message) == str:
                yield(message)
            else:
                df_Main = message
        except StopIteration:
            break
    yield f"- Final Dataset Rows Count: {df_Main.shape[0]} 📅"
    yield "Main Merged Dataset Created.... Starting Parts Categorization.... "
    part_categorization(df_Main, 'Part Category')
    yield "Parts Categorization Done... Starting Zoning of all Parts... 🟥🟧🟨🟩🟦"
    vCounts = Apply_Zoning(df_Main, zones, 'Total Sold', 'Zone')
    yield "- Zone Counts: " + str(vCounts)
    yield "Apply Zoning Done.... Starting Part Storage Allocation... "
    generator = applyStorage(df_Main)
    while True:
        try:
            message = next(generator)
            yield(message)
        except StopIteration:
            break
    yield "Part Storage Allocation Completed...."
    yield "Main Logic Completed - Final Dataset converting to Excel"
    df_Main.to_excel('Final_Dataset.xlsx', index=False) 
    yield "Process Completed - Final Dataset converted to Excel ✅"
    yield "Return", df_Main
    

def Bin_Data():
    df_binData = DataFrame(columns=['Bin Label', 'Bin Category', 'Total Bins', 'Filled Amount', 'Bin Order', 'Bin Location', 'Availiability Flag'])

    # * High-Density Drawers (2)
    binData = [ 
        {'Bin Label': 'D362406', 'Bin Category': 'Drawer', 'Total Bins': 5, 'Filled Amount': 0, 'Bin Order': 1, 'Bin Location': 'None', 'Availiability Flag': 'Yes'},
        {'Bin Label': 'D482406', 'Bin Category': 'Drawer', 'Total Bins': 4, 'Filled Amount': 0, 'Bin Order': 2, 'Bin Location': 'None', 'Availiability Flag': 'Yes'}
    ]
    # * Clip-Shelving (6)
    binData.extend([
        {'Bin Label': 'C361215', 'Bin Category': 'Clip', 'Total Bins': 4, 'Filled Amount': 0, 'Bin Order': 3, 'Bin Location': 'None', 'Availiability Flag': 'Yes'},
        {'Bin Label': 'C361815', 'Bin Category': 'Clip', 'Total Bins': 6, 'Filled Amount': 0, 'Bin Order': 4, 'Bin Location': 'None', 'Availiability Flag': 'Yes'},
        {'Bin Label': 'C362415', 'Bin Category': 'Clip', 'Total Bins': 8, 'Filled Amount': 0.0, 'Bin Order': 5, 'Bin Location': 'None', 'Availiability Flag': 'Yes'},    
        {'Bin Label': 'C481215', 'Bin Category': 'Clip', 'Total Bins': 3, 'Filled Amount': 0.0, 'Bin Order': 6, 'Bin Location': 'None', 'Availiability Flag': 'Yes'},  
        {'Bin Label': 'C481815', 'Bin Category': 'Clip', 'Total Bins': 5, 'Filled Amount': 0.0, 'Bin Order': 7, 'Bin Location': 'None', 'Availiability Flag': 'Yes'},   
        {'Bin Label': 'C482415', 'Bin Category': 'Clip', 'Total Bins': 7, 'Filled Amount': 0.0, 'Bin Order': 8, 'Bin Location': 'None', 'Availiability Flag': 'Yes'}
    ])

    # * Bulk-Storage (18)
    binData.extend([
    {'Bin Label': 'B482448', 'Bin Category': 'Bulk', 'Total Bins': 4, 'Filled Amount': 0.0, 'Bin Order': 9, 'Bin Location': 'None', 'Availiability Flag': 'Yes'},
    {'Bin Label': 'B483648', 'Bin Category': 'Bulk', 'Total Bins': 5, 'Filled Amount': 0.0, 'Bin Order': 10, 'Bin Location': 'None', 'Availiability Flag': 'Yes'},
    {'Bin Label': 'B484248', 'Bin Category': 'Bulk', 'Total Bins': 6, 'Filled Amount': 0.0, 'Bin Order': 11, 'Bin Location': 'None', 'Availiability Flag': 'Yes'},
    {'Bin Label': 'B484848', 'Bin Category': 'Bulk', 'Total Bins': 4, 'Filled Amount': 0.0, 'Bin Order': 12, 'Bin Location': 'None', 'Availiability Flag': 'Yes'},
    {'Bin Label': 'B487248', 'Bin Category': 'Bulk', 'Total Bins': 3, 'Filled Amount': 0.0, 'Bin Order': 13, 'Bin Location': 'None', 'Availiability Flag': 'Yes'},
    {'Bin Label': 'B489648', 'Bin Category': 'Bulk', 'Total Bins': 4, 'Filled Amount': 0.0, 'Bin Order': 14, 'Bin Location': 'None', 'Availiability Flag': 'Yes'},
    {'Bin Label': 'B722448', 'Bin Category': 'Bulk', 'Total Bins': 4, 'Filled Amount': 0.0, 'Bin Order': 15, 'Bin Location': 'None', 'Availiability Flag': 'Yes'},
    {'Bin Label': 'B723648', 'Bin Category': 'Bulk', 'Total Bins': 3, 'Filled Amount': 0.0, 'Bin Order': 16, 'Bin Location': 'None', 'Availiability Flag': 'Yes'},
    {'Bin Label': 'B724248', 'Bin Category': 'Bulk', 'Total Bins': 4, 'Filled Amount': 0.0, 'Bin Order': 17, 'Bin Location': 'None', 'Availiability Flag': 'Yes'},
    {'Bin Label': 'B724848', 'Bin Category': 'Bulk', 'Total Bins': 6, 'Filled Amount': 0.0, 'Bin Order': 18, 'Bin Location': 'None', 'Availiability Flag': 'Yes'},
    {'Bin Label': 'B727248', 'Bin Category': 'Bulk', 'Total Bins': 4, 'Filled Amount': 0.0, 'Bin Order': 19, 'Bin Location': 'None', 'Availiability Flag': 'Yes'},
    {'Bin Label': 'B729648', 'Bin Category': 'Bulk', 'Total Bins': 5, 'Filled Amount': 0.0, 'Bin Order': 20, 'Bin Location': 'None', 'Availiability Flag': 'Yes'},
    {'Bin Label': 'B962448', 'Bin Category': 'Bulk', 'Total Bins': 4, 'Filled Amount': 0.0, 'Bin Order': 21, 'Bin Location': 'None', 'Availiability Flag': 'Yes'},
    {'Bin Label': 'B963648', 'Bin Category': 'Bulk', 'Total Bins': 5, 'Filled Amount': 0.0, 'Bin Order': 22, 'Bin Location': 'None', 'Availiability Flag': 'Yes'},
    {'Bin Label': 'B964248', 'Bin Category': 'Bulk', 'Total Bins': 7, 'Filled Amount': 0.0, 'Bin Order': 23, 'Bin Location': 'None', 'Availiability Flag': 'Yes'},
    {'Bin Label': 'B964848', 'Bin Category': 'Bulk', 'Total Bins': 4, 'Filled Amount': 0.0, 'Bin Order': 24, 'Bin Location': 'None', 'Availiability Flag': 'Yes'},
    {'Bin Label': 'B967248', 'Bin Category': 'Bulk', 'Total Bins': 6, 'Filled Amount': 0.0, 'Bin Order': 25, 'Bin Location': 'None', 'Availiability Flag': 'Yes'},
    {'Bin Label': 'B969648', 'Bin Category': 'Bulk', 'Total Bins': 4, 'Filled Amount': 0.0, 'Bin Order': 26, 'Bin Location': 'None', 'Availiability Flag': 'Yes'}
    ])

    # * Specialty (7) TR
    binData.extend([
        {'Bin Label': 'BR484816', 'Bin Category': 'Battery', 'Total Bins': 14, 'Filled Amount': 0, 'Bin Order': 0, 'Bin Location': 'None', 'Availiability Flag': 'Yes'},
        {'Bin Label': 'TR48', 'Bin Category': 'Tire', 'Total Bins': 6, 'Filled Amount': 0, 'Bin Order': 0, 'Bin Location': 'None', 'Availiability Flag': 'Yes'},
        {'Bin Label': "TR72", 'Bin Category': 'Tire', 'Total Bins': 6, 'Filled Amount': 0, 'Bin Order': 0, 'Bin Location': 'None', 'Availiability Flag': 'Yes'},
        {'Bin Label': 'BC967248', 'Bin Category': 'Bumper Cover', 'Total Bins': 3, 'Filled Amount': 0.0, 'Bin Order': 0, 'Bin Location': 'None', 'Availiability Flag': 'Yes'},  
        {'Bin Label': 'BH967280', 'Bin Category': 'Hood', 'Total Bins': 5, 'Filled Amount': 0.0, 'Bin Order': 0, 'Bin Location': 'None', 'Availiability Flag': 'Yes'},   
        {'Bin Label': 'HS06', 'Bin Category': 'Hanging', 'Total Bins': 5, 'Filled Amount': 0.0, 'Bin Order': 0, 'Bin Location': 'None', 'Availiability Flag': 'Yes'},   
        {'Bin Label': 'HS12', 'Bin Category': 'Hanging', 'Total Bins': 7, 'Filled Amount': 0.0, 'Bin Order': 0, 'Bin Location': 'None', 'Availiability Flag': 'Yes'}
    ])

    # Append the Data to the DF
    df_binData = concat([df_binData, DataFrame(binData)], ignore_index=True)
    df_binData['Total Bins'] = random.choice(range(40, 400), df_binData.shape[0])
    return df_binData


def RedZoneAllocation(df_Main, df_binData):
    output = StringIO()
    for pn in tqdm(df_Main.loc[(df_Main['Zone'] == 'Red Hot') | (df_Main['Zone'] == 'Red') | (df_Main['Zone'] == 'Orange') | (df_Main['Zone'] == 'Yellow'), 'Part#'], "Red Family Zones Non-Specialty Actual Bin Allocation Completion", file=output):
        yield output.getvalue().split('\r')[-1]
        # Get & Set Variables
        actualBin =  ""
        overflowBin = ""
        overflowComment = ""

        partData = df_Main[df_Main['Part#'] == pn]
        partHeight = partData['Height'].values[0]
        partWidth = partData['Width'].values[0]
        partDepth = partData['Depth'].values[0]
        partVolume = partHeight * partWidth * partDepth 
        binType = partData['Bin Type'].values[0]
        storageType = partData['StorageType'].values[0]
        partOHInven = partData['OH Inventory'].values[0]


        # ~ Base Continue Case - If no Storage Assignment, no Inventory Parts or is Specialty Part
        if (binType == "") or ("Specialty Storage" in storageType) or (partOHInven <= 0):     
            continue

        binData = df_binData.loc[df_binData['Bin Label'] == binType]
        totalBinOfType = binData['Total Bins'].values[0]
        filledAmtOfBin = binData['Filled Amount'].values[0]
        binOrder = binData['Bin Order'].values[0]
        flagAvail = binData['Availiability Flag'].values[0]

        # Calculate Variables
        binVolume = fillFactor * (float(binType[1:3]) * float(binType[3:5]) * float(binType[5:7]))
        remainingBinVolume = float(totalBinOfType - filledAmtOfBin) * binVolume  # Check for Remaining Vol in Bin 
        partsAllocated = min(floor(remainingBinVolume / partVolume), partOHInven)

        if partsAllocated > 0:   # * If Actual Bin is Availiable
            # Calculate Variables
            totalPartVolume = partOHInven * partVolume
            actualBinRequired = round((partsAllocated * partVolume) / binVolume, 3)
            numBins = round(totalPartVolume / binVolume, 3)

            # Set Values
            df_binData.loc[df_binData['Bin Label'] == binType, 'Filled Amount'] += actualBinRequired
            actualBin = f"{binType} ({actualBinRequired}, {partsAllocated})"

            if filledAmtOfBin + actualBinRequired >= (totalBinOfType - 0.01): # If Bin is FULL, Reset Flag
                df_binData.loc[df_binData['Bin Label'] == binType, 'Availiability Flag'] = 'No'

            if (filledAmtOfBin + numBins) > (totalBinOfType- 0.01):   # * If Overflow (Actual Bin can't fit all Parts) (Only 1)
                overflowParts = partOHInven - partsAllocated
                
                # Find next availiable BIN to  handle overflow parts
                binFound = False
                for binType1 in df_binData.loc[(df_binData['Bin Order'] > binOrder), 'Bin Label']:
                    # Calculate Variables
                    binData = df_binData[df_binData['Bin Label'] == binType1]
                    totalBinOfType = binData['Total Bins'].values[0]
                    filledAmtOfBin = binData['Filled Amount'].values[0]
                    binVolume = fillFactor * (float(binType1[1:3]) * float(binType1[3:5]) * float(binType1[5:7]))
                    remainingBinVolume = float(totalBinOfType - filledAmtOfBin) * binVolume  # Check for Remaining Vol in Bin 
                    partsAllocated = min(floor(remainingBinVolume / partVolume), partOHInven)

                    if partsAllocated > 0:   # If Actual Bin is Availiable
                        binFound = True
                        break
                    #  OLD Code
                    # if (df_binData[df_binData['Bin Label'] == binType1]['Availiability Flag'].values[0] == 'Yes'):
                    #     binData = df_binData[df_binData['Bin Label'] == binType1]
                    #     fillAmt = df_binData[df_binData['Bin Label'] == binType1]['Filled Amount'].values[0] 
                    #     totalBin = df_binData[df_binData['Bin Label'] == binType1]['Total Bins'].values[0] 
                    #     if (fillAmt < (totalBin - 0.01)):
                    #         break

                if not (binFound):
                    df_Main.loc[df_Main['Part#'] == pn, 'Overflow Bins'] = f"Part1- No More Available/Fitting Bins"
                    df_Main.loc[df_Main['Part#'] == pn, 'Overflow Comment'] = f"{overflowParts} Parts Left; No Bins availiable to fit"
                    continue

                # Get & Calculate Variables
                binType = binData['Bin Label'].values[0]
                totalBinOfType = binData['Total Bins'].values[0]
                filledAmtOfBin = binData['Filled Amount'].values[0]
                
                binVolume = fillFactor * (float(binType[1:3]) * float(binType[3:5]) * float(binType[5:7]))
                remainingBinVolume = float(totalBinOfType - filledAmtOfBin) * binVolume  # Check for Remaining Vol in Bin 
                partsAllocated = min(floor(remainingBinVolume / partVolume), overflowParts)
                actualBinRequired = round((partsAllocated * partVolume) / binVolume, 3)

                # Add  FilledAmount for OverFlow Bin  
                df_binData.loc[df_binData['Bin Label'] == binType, 'Filled Amount'] += actualBinRequired
                overflowBin = f"{binType} ({actualBinRequired}, {partsAllocated})"
            
                # If more overflow
                leftParts = overflowParts - partsAllocated
                if leftParts > 0:
                    binsNeeded = round(leftParts * partVolume / binVolume, 3)
                    overflowComment = f"Second Overflow: {leftParts} Parts Left; {binsNeeded} quantity of {binType} Bin Needed;"
                
                if filledAmtOfBin + actualBinRequired >= (totalBinOfType - 0.01): 
                    df_binData.loc[df_binData['Bin Label'] == binType, 'Availiability Flag'] = 'No'

        else:    # * If Actual Bin is not avaialble
            binFound = False
            for binType1 in df_binData.loc[(df_binData['Bin Order'] > binOrder), 'Bin Label']:
                # Calculate Variables
                binData = df_binData[df_binData['Bin Label'] == binType1]
                totalBinOfType = binData['Total Bins'].values[0]
                filledAmtOfBin = binData['Filled Amount'].values[0]
                binVolume = fillFactor * (float(binType1[1:3]) * float(binType1[3:5]) * float(binType1[5:7]))
                remainingBinVolume = float(totalBinOfType - filledAmtOfBin) * binVolume  # Check for Remaining Vol in Bin 
                partsAllocated = min(floor(remainingBinVolume / partVolume), partOHInven)

                if partsAllocated > 0:
                    binFound = True
                    break
                #  OLD Code
                # if (df_binData[df_binData['Bin Label'] == binType1]['Availiability Flag'].values[0] == 'Yes'):
                #     binData = df_binData[df_binData['Bin Label'] == binType1]
                #     fillAmt = df_binData[df_binData['Bin Label'] == binType1]['Filled Amount'].values[0] 
                #     totalBin = df_binData[df_binData['Bin Label'] == binType1]['Total Bins'].values[0] 
                #     if (fillAmt < (totalBin - 0.01)):
                #         break

            if not (binFound):
                df_Main.loc[df_Main['Part#'] == pn, 'Actual Bin Allocation'] = "Part2- No More Available/Fitting Bins"
                df_Main.loc[df_Main['Part#'] == pn, 'Overflow Bins'] = "Part2- No More Available/Fitting Bins"
                df_Main.loc[df_Main['Part#'] == pn, 'Overflow Comment'] = f"{partOHInven} Parts Left; No Bins availiable to fit"
                continue

            binType = binData['Bin Label'].values[0]
            totalBinOfType = binData['Total Bins'].values[0]
            filledAmtOfBin = binData['Filled Amount'].values[0]
            binOrder = binData['Bin Order'].values[0]
            binVolume = fillFactor * (float(binType[1:3]) * float(binType[3:5]) * float(binType[5:7]))
            remainingBinVolume = float(totalBinOfType - filledAmtOfBin) * binVolume   ## Check for Remaining Vol in Bin 
            partVolume = partHeight * partWidth * partDepth 
            totalPartVolume = partOHInven * partVolume
            numBins = round(totalPartVolume / binVolume, 3)         ### Number of Bins Required to fill Inventry Parts
            partsAllocated = min(floor(remainingBinVolume / partVolume), partOHInven)
            actualBinRequired = round((partsAllocated * partVolume) / binVolume, 3)
            
            df_binData.loc[df_binData['Bin Label'] == binType, 'Filled Amount'] += actualBinRequired
            actualBin = f"{binType} ({actualBinRequired}, {partsAllocated})"

            if filledAmtOfBin + actualBinRequired >= (totalBinOfType - 0.01): 
                df_binData.loc[df_binData['Bin Label'] == binType, 'Availiability Flag'] = 'No'

            if filledAmtOfBin + numBins > totalBinOfType:   # * If Overflow (Actual Bin can't fit all Parts) (Only 1)
                overflowParts = partOHInven - partsAllocated
                for binType1 in df_binData.loc[(df_binData['Bin Order'] > binOrder), 'Bin Label']:
                    # Calculate Variables
                    binData = df_binData[df_binData['Bin Label'] == binType1]
                    totalBinOfType = binData['Total Bins'].values[0]
                    filledAmtOfBin = binData['Filled Amount'].values[0]
                    binVolume = fillFactor * (float(binType1[1:3]) * float(binType1[3:5]) * float(binType1[5:7]))
                    remainingBinVolume = float(totalBinOfType - filledAmtOfBin) * binVolume  # Check for Remaining Vol in Bin 
                    partsAllocated = min(floor(remainingBinVolume / partVolume), partOHInven)

                    if partsAllocated > 0:
                        binFound = True
                        break
                    #  OLD Code
                    # if (df_binData[df_binData['Bin Label'] == binType1]['Availiability Flag'].values[0] == 'Yes'):
                    #     binData = df_binData[df_binData['Bin Label'] == binType1]
                    #     fillAmt = df_binData[df_binData['Bin Label'] == binType1]['Filled Amount'].values[0] 
                    #     totalBin = df_binData[df_binData['Bin Label'] == binType1]['Total Bins'].values[0] 
                    #     if (fillAmt < (totalBin - 0.01)):
                    #         break

                if not (binFound):
                    df_Main.loc[df_Main['Part#'] == pn, 'Overflow Bins'] = f"Part3- No More Available/Fitting Bins"
                    df_Main.loc[df_Main['Part#'] == pn, 'Overflow Comment'] = f"{overflowParts} Parts Left; No Bins availiable to fit"
                    continue

                binType = binData['Bin Label'].values[0]
                binVolume = fillFactor * (float(binType[1:3]) * float(binType[3:5]) * float(binType[5:7]))
                totalBinOfType = binData['Total Bins'].values[0]
                filledAmtOfBin = binData['Filled Amount'].values[0]
                remainingBinVolume = float(totalBinOfType - filledAmtOfBin) * binVolume  # Check for Remaining Vol in Bin 
                partsAllocated = min(floor(remainingBinVolume / partVolume), overflowParts)
                actualBinRequired = round((partsAllocated * partVolume) / binVolume, 3)
                
                df_binData.loc[df_binData['Bin Label'] == binType, 'Filled Amount'] += actualBinRequired
                overflowBin = f"{binType} ({actualBinRequired}, {partsAllocated})"
            
                leftParts = overflowParts - partsAllocated
                if leftParts > 0:
                    binsNeeded = round(leftParts * partVolume / binVolume, 2)
                    overflowComment = f"Second Overflow: {leftParts} Parts Left; {binsNeeded} quantity of {binType} Bin Needed;"

                if filledAmtOfBin + actualBinRequired >= (totalBinOfType - 0.01): 
                    df_binData.loc[df_binData['Bin Label'] == binType, 'Availiability Flag'] = 'No'

        df_Main.loc[df_Main['Part#'] == pn, 'Actual Bin Allocation'] = actualBin
        df_Main.loc[df_Main['Part#'] == pn, 'Overflow Bins'] = overflowBin
        df_Main.loc[df_Main['Part#'] == pn, 'Overflow Comment'] = overflowComment

        yield "Return", df_Main

    # ~1 min 15 secs


def GreenBlueAllocation(df_Main, df_binData):
    output = StringIO()
    for pn in tqdm(df_Main.loc[(df_Main['Zone'] == 'Green') | (df_Main['Zone'] == 'Blue'), 'Part#'], "Green&Blue Non-Specialty Actual Bin Allocation Completion", file=output):
        yield output.getvalue().split('\r')[-1]
        # Get Variable
        actualBin =  ""
        overflowBin = ""
        overflowComment = ""

        partData = df_Main[df_Main['Part#'] == pn]
        partHeight = partData['Height'].values[0]
        partWidth = partData['Width'].values[0]
        partDepth = partData['Depth'].values[0]
        partVolume = partHeight * partWidth * partDepth 
        binType = partData['Bin Type'].values[0]
        storageType = partData['StorageType'].values[0]
        partOHInven = partData['OH Inventory'].values[0]

        ## * If Inventry Qty is zero, Go to Next Part -- Handle Specialty Storage separately 
        if (binType == "") or ("Specialty Storage" in storageType) or (partOHInven <= 0):     
            continue

        binData = df_binData.loc[df_binData['Bin Label'] == binType]
        totalBinOfType = binData['Total Bins'].values[0]
        filledAmtOfBin = binData['Filled Amount'].values[0]
        binOrder = binData['Bin Order'].values[0]
    
        # Calculate Variables
        binVolume = fillFactor * (float(binType[1:3]) * float(binType[3:5]) * float(binType[5:7]))
        remainingBinVolume = float(totalBinOfType - filledAmtOfBin) * binVolume  # Check for Remaining Vol in Bin 
        partsAllocated = min(floor(remainingBinVolume / partVolume), partOHInven)

        if partsAllocated > 0: # & (binData['Availiability Flag'].values[0] == "Yes"):    # If Actual Bin is Availiable
            binVolume = fillFactor * (float(binType[1:3]) * float(binType[3:5]) * float(binType[5:7]))
            remainingBinVolume = float(totalBinOfType - filledAmtOfBin) * binVolume  # Check for Remaining Vol in Bin      
            totalPartVolume = partOHInven * partVolume
            numBins = round(totalPartVolume / binVolume, 3)
            partsAllocated = min(floor(remainingBinVolume / partVolume), partOHInven)
            binRequired = round((partsAllocated * partVolume) / binVolume, 3)    

            df_binData.loc[df_binData['Bin Label'] == binType, 'Filled Amount'] += binRequired
            actualBin = f"{binType} ({binRequired}, {partsAllocated})"

            if filledAmtOfBin + ((partsAllocated * partVolume) / binVolume) >= (totalBinOfType - 0.01):    ### @ ACtual BIN
                df_binData.loc[df_binData['Bin Label'] == binType, 'Availiability Flag'] = 'No'

            ###  Handle OVERFLOW  condition (Only 1 Overflow) 
            if filledAmtOfBin + numBins > totalBinOfType:
                
                overflowParts = partOHInven - partsAllocated
                for binType1 in df_binData.loc[(df_binData['Bin Order'] > binOrder), 'Bin Label']:
                    # Calculate Variables
                    binData = df_binData[df_binData['Bin Label'] == binType1]
                    totalBinOfType = binData['Total Bins'].values[0]
                    filledAmtOfBin = binData['Filled Amount'].values[0]
                    binVolume = fillFactor * (float(binType1[1:3]) * float(binType1[3:5]) * float(binType1[5:7]))
                    remainingBinVolume = float(totalBinOfType - filledAmtOfBin) * binVolume  # Check for Remaining Vol in Bin 
                    partsAllocated = min(floor(remainingBinVolume / partVolume), partOHInven)

                    if partsAllocated > 0:   # @ If Actual Bin is Availiable
                        binFound = True
                        break
                    #  OLD Code
                    # if (df_binData[df_binData['Bin Label'] == binType1]['Availiability Flag'].values[0] == 'Yes'):
                    #     binData = df_binData[df_binData['Bin Label'] == binType1]
                    #     fillAmt = df_binData[df_binData['Bin Label'] == binType1]['Filled Amount'].values[0] 
                    #     totalBin = df_binData[df_binData['Bin Label'] == binType1]['Total Bins'].values[0] 
                    #     if (fillAmt < (totalBin - 0.01)):
                    #         break

                if not (binFound):
                    df_Main.loc[df_Main['Part#'] == pn, 'Overflow Bins'] = f"Part1-No More Available/Fitting Bins"
                    df_Main.loc[df_Main['Part#'] == pn, 'Overflow Comment'] = f"{overflowParts} Parts Left; No Bins availiable to fit"
                    continue

                binType = binData['Bin Label'].values[0]
                binVolume = fillFactor * (float(binType[1:3]) * float(binType[3:5]) * float(binType[5:7]))
                totalBinOfType = binData['Total Bins'].values[0]
                filledAmtOfBin = binData['Filled Amount'].values[0]
                remainingBinVolume = float(totalBinOfType - filledAmtOfBin) * binVolume  # Check for Remaining Vol in Bin 
                partsAllocated = min(floor(remainingBinVolume / partVolume), overflowParts)
                binRequired = round((partsAllocated * partVolume) / binVolume, 3)  

                overflowBin = f"{binType} ({binRequired}, {partsAllocated})"
            
                leftParts = overflowParts - partsAllocated
                if leftParts > 0:
                    binsNeeded = round(leftParts * partVolume / binVolume, 3)
                    overflowComment = f"Second Overflow: {leftParts} Parts Left; {binsNeeded} quantity of {binType} Bin Needed;"
                
                if (filledAmtOfBin + binRequired) >= (totalBinOfType - 0.01): 
                    df_binData.loc[df_binData['Bin Label'] == binType, 'Availiability Flag'] = 'No'

        else:    ## ^  If  suggested Bin Is NOT Avaialble.  Pick Next Available Bin and Process
            for binType1 in df_binData.loc[(df_binData['Bin Order'] > binOrder), 'Bin Label']:
                # Calculate Variables
                binData = df_binData[df_binData['Bin Label'] == binType1]
                totalBinOfType = binData['Total Bins'].values[0]
                filledAmtOfBin = binData['Filled Amount'].values[0]
                binVolume = fillFactor * (float(binType1[1:3]) * float(binType1[3:5]) * float(binType1[5:7]))
                remainingBinVolume = float(totalBinOfType - filledAmtOfBin) * binVolume  # Check for Remaining Vol in Bin 
                partsAllocated = min(floor(remainingBinVolume / partVolume), partOHInven)

                if partsAllocated > 0:   # @ If Actual Bin is Availiable
                    binFound = True
                    break
                #  OLD Code
                # if (df_binData[df_binData['Bin Label'] == binType1]['Availiability Flag'].values[0] == 'Yes'):
                #     binData = df_binData[df_binData['Bin Label'] == binType1]
                #     fillAmt = df_binData[df_binData['Bin Label'] == binType1]['Filled Amount'].values[0] 
                #     totalBin = df_binData[df_binData['Bin Label'] == binType1]['Total Bins'].values[0] 
                #     if (fillAmt < (totalBin - 0.01)):
                #         break

            if not (binFound):            
                df_Main.loc[df_Main['Part#'] == pn, 'Actual Bin Allocation'] = "Part2-No More Available/Fitting Bins"
                df_Main.loc[df_Main['Part#'] == pn, 'Overflow Bins'] = "Part2-No More Available/Fitting Bins"
                df_Main.loc[df_Main['Part#'] == pn, 'Overflow Comment'] = f"{partOHInven} Parts Left; No Bins availiable to fit"
                continue

            binType = binData['Bin Label'].values[0]
            totalBinOfType = binData['Total Bins'].values[0]
            filledAmtOfBin = binData['Filled Amount'].values[0]
            binOrder = binData['Bin Order'].values[0]
            binVolume = fillFactor * (float(binType[1:3]) * float(binType[3:5]) * float(binType[5:7]))
            remainingBinVolume = float(totalBinOfType - filledAmtOfBin) * binVolume   ## Check for Remaining Vol in Bin 
            partVolume = partHeight * partWidth * partDepth 
            totalPartVolume = partOHInven * partVolume
            numBins = round(totalPartVolume / binVolume, 3)         ### Number of Bins Required to fill Inventry Parts
            partsAllocated = min(floor(remainingBinVolume / partVolume), partOHInven)
            binRequired = round((partsAllocated * partVolume) / binVolume, 3)  
            
            df_binData.loc[df_binData['Bin Label'] == binType, 'Filled Amount'] += binRequired
            actualBin = f"{binType} ({binRequired}, {partsAllocated})"

            if (filledAmtOfBin + binRequired) >= (totalBinOfType - 0.01):
                df_binData.loc[df_binData['Bin Label'] == binType, 'Availiability Flag'] = 'No'

            ###  Handle OVERFLOW  condition (Only 1 Overflow) 
            if filledAmtOfBin + numBins > totalBinOfType:
                overflowParts = partOHInven - partsAllocated
                for binType1 in df_binData.loc[(df_binData['Bin Order'] > binOrder), 'Bin Label']:
                    # Calculate Variables
                    binData = df_binData[df_binData['Bin Label'] == binType1]
                    totalBinOfType = binData['Total Bins'].values[0]
                    filledAmtOfBin = binData['Filled Amount'].values[0]
                    binVolume = fillFactor * (float(binType1[1:3]) * float(binType1[3:5]) * float(binType1[5:7]))
                    remainingBinVolume = float(totalBinOfType - filledAmtOfBin) * binVolume  # Check for Remaining Vol in Bin 
                    partsAllocated = min(floor(remainingBinVolume / partVolume), partOHInven)

                    if partsAllocated > 0:   # @ If Actual Bin is Availiable
                        binFound = True
                        break
                    #  OLD Code
                    # if (df_binData[df_binData['Bin Label'] == binType1]['Availiability Flag'].values[0] == 'Yes'):
                    #     binData = df_binData[df_binData['Bin Label'] == binType1]
                    #     fillAmt = df_binData[df_binData['Bin Label'] == binType1]['Filled Amount'].values[0] 
                    #     totalBin = df_binData[df_binData['Bin Label'] == binType1]['Total Bins'].values[0] 
                    #     if (fillAmt < (totalBin - 0.01)):
                    #         break

                if not (binFound):
                    df_Main.loc[df_Main['Part#'] == pn, 'Overflow Bins'] = f"Part3-No More Available/Fitting Bins"
                    df_Main.loc[df_Main['Part#'] == pn, 'Overflow Comment'] = f"{overflowParts} Parts Left; No Bins availiable to fit"
                    continue

                binType = binData['Bin Label'].values[0]
                binVolume = fillFactor * (float(binType[1:3]) * float(binType[3:5]) * float(binType[5:7]))
                totalBinOfType = binData['Total Bins'].values[0]
                filledAmtOfBin = binData['Filled Amount'].values[0]
                remainingBinVolume = float(totalBinOfType - filledAmtOfBin) * binVolume  # Check for Remaining Vol in Bin 
                partsAllocated = min(floor(remainingBinVolume / partVolume), overflowParts)
                binRequired = round((partsAllocated * partVolume) / binVolume, 3) 

                ## @ ADD Below Filled Amount for Overflow bins
                df_binData.loc[df_binData['Bin Label'] == binType, 'Filled Amount'] += binRequired
                overflowBin = f"{binType} ({binRequired}, {partsAllocated})"
            
                leftParts = overflowParts - partsAllocated
                if leftParts > 0:
                    binsNeeded = round(leftParts * partVolume / binVolume, 3)
                    overflowComment = f"Second Overflow: {leftParts} Parts Left; {binsNeeded} quantity of {binType} Bin Needed;"

                if (filledAmtOfBin + binRequired) >= (totalBinOfType - 0.01):
                    df_binData.loc[df_binData['Bin Label'] == binType, 'Availiability Flag'] = 'No'

        df_Main.loc[df_Main['Part#'] == pn, 'Actual Bin Allocation'] = actualBin
        df_Main.loc[df_Main['Part#'] == pn, 'Overflow Bins'] = overflowBin
        df_Main.loc[df_Main['Part#'] == pn, 'Overflow Comment'] = overflowComment

        yield "Return", df_Main
    # ~16 mins 12 secs


def SpecialtyAllocation(df_Main, df_binData):
    output = StringIO()
    for pn in tqdm(df_Main['Part#'], desc="All Zones Specialty Actual Bin Allocation Completion", file=output):
        yield output.getvalue().split('\r')[-1]
        # Get & Set Variables
        actualBin =  ""
        overflowBin = ""
        overflowComment = ""

        partData = df_Main[df_Main['Part#'] == pn]
        partHeight = partData['Height'].values[0]
        partWidth = partData['Width'].values[0]
        partDepth = partData['Depth'].values[0]
        binType = partData['Bin Type'].values[0]
        partOHInven = partData['OH Inventory'].values[0]
        partSKUCount = partData['SKU Count'].values[0]

        # ~ Base Continue Case - If no Storage Assignment, no Inventory Parts or is not Specialty Part
        if (binType == "") or (partOHInven <= 0):     
            continue
        if (all([binLabelTypes not in binType.lower() for binLabelTypes in ['br', 'tr', 'hs', 'bc', 'bh']])):     
            continue

        binData = df_binData.loc[df_binData['Bin Label'] == binType]
        totalBinOfType = binData['Total Bins'].values[0]
        filledAmtOfBin = binData['Filled Amount'].values[0]

        ## * Calculation for Battery
        if "br" in binType.lower():
            remainingBinWidth = (totalBinOfType - filledAmtOfBin) * float(binType[4:6])
            partsAllocated = min(floor(remainingBinWidth / partWidth), partOHInven)
            binsRequired = round((partsAllocated * partWidth) / float(binType[4:6]), 4)
            partsLeft = partOHInven - partsAllocated
            overflowBinsNeeded = partsLeft / float(binType[2:4])
        ## * Calculation for Tire
        if "tr" in binType.lower():
            remainingBinWidth = (totalBinOfType - filledAmtOfBin) * float(binType[2:4])
            partsAllocated = min(floor(remainingBinWidth / partWidth), partOHInven)
            binsRequired = round((partsAllocated * partWidth) / float(binType[2:4]), 4)
            partsLeft = partOHInven - partsAllocated
            overflowBinsNeeded = round(partsLeft / float(binType[2:4]), 3)
        ## * Calculation for Hanging Storage
        if "hs" in binType.lower():
            partsAllocated = min(floor(totalBinOfType - filledAmtOfBin), partOHInven)
            binsRequired = round(partsAllocated, 4)
            partsLeft = partOHInven - partsAllocated
            overflowBinsNeeded = partsLeft
        ## * Calculation for Bumper Cover & Hoods
        if ("bc" in binType.lower()) | ("bh" in binType.lower()):
            partVolume = partHeight * partWidth * partDepth 
            binVol = fillFactor * (float(binType[2:4]) * float(binType[4:6]) * float(binType[6:8]))
            partsAllocated = min(floor(((totalBinOfType - filledAmtOfBin) * binVol) / partVolume), partOHInven)
            binsRequired = round((partsAllocated * partVolume) / binVol, 4)
            partsLeft = partOHInven - partsAllocated
            overflowBinsNeeded = round((partsLeft * partVolume) / binVol, 3)

        ## * Main Data Update
        if filledAmtOfBin + binsRequired >= (totalBinOfType - 0.01): # Update Availiability Flag, if full
            df_binData.loc[df_binData['Bin Label'] == binType, 'Availiability Flag'] = 'No'

        if partsAllocated > 0: # If any parts allocated
            df_binData.loc[df_binData['Bin Label'] == binType, 'Filled Amount'] += binsRequired
            actualBin = f"{binType} ({binsRequired}, {partsAllocated})"
        else:
            actualBin = "SP- No More Available/Fitting Bins" # If no parts can be allocated

        if partsLeft > 0: # If Overflow
            overflowBin = "SP- No More Available/Fitting Bins"
            overflowComment = f"{partOHInven - partsAllocated} Parts Left; {overflowBinsNeeded} quantity of {binType} Bin Needed;"

        df_Main.loc[df_Main['Part#'] == pn, 'Actual Bin Allocation'] = actualBin
        df_Main.loc[df_Main['Part#'] == pn, 'Overflow Bins'] = overflowBin
        df_Main.loc[df_Main['Part#'] == pn, 'Overflow Comment'] = overflowComment
            
        yield "Return", df_Main
    # ~ 11 mins 28 sec



def actualBinAllocation(df_Main):
    df_binData = Bin_Data()
    yield "Bins Data Read... Starting Actual Bin Allocation for Non-Specialty Parts of Red Family Zones... 🟥🟧🟨"
    generator = RedZoneAllocation(df_Main, df_binData)
    while True:
        try:
            message = next(generator)
            if message[0] == "Return":
                df_Main = message[1]
            else:
                yield(message)
        except StopIteration:
            break
    #yield f"RED Zone Test Message: {df_Main.shape[0]}"
    yield "Done Actual Bin Allocation for Red Family Zones... Starting for Non-Specialty Parts of Green & Blue Zones... 🟩🟦"
    generator = GreenBlueAllocation(df_Main, df_binData)
    while True:
        try:
            message = next(generator)
            if message[0] == "Return":
                df_Main = message[1]
            else:
                yield(message)
        except StopIteration:
            break
    yield "Done Actual Bin Allocation for Green & Blue Zones... Starting for All Zone Specialty Parts... 🟥🟧🟨🟩🟦⭐"    
    generator = SpecialtyAllocation(df_Main, df_binData)
    while True:
        try:
            message = next(generator)
            if message[0] == "Return":
                df_Main = message[1]
            else:
                yield(message)
        except StopIteration:
            break
    yield "Done Actual Bin Allocation for Green & Blue Zones..."    
    yield "Main Logic Completed - Final Dataset converting to Excel"
    df_Main.to_excel('Final_Dataset.xlsx', index=False) 
    yield "Process Completed - Final Dataset converted to Excel ✅"
    yield "Return", df_Main
