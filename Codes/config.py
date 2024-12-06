################################  config.py  ####################################
# Author: Sukhendu Sain
# Description: Config file of codebase. Houses different parameters and variables
# Data: 23-Nov-2024
#################################################################################
import os


## Files Path ##
ROOT_FILE_PATH = '\\'.join(os.getcwd().split('\\')[:-1])

#AKINS_FOMO_FILE_PATH = os.path.join(ROOT_FILE_PATH, r"Data&Files\AKINS FoMoCo_Piece_Sales_112222_YTD.xlsx")
GPARTS_FILE_PATH = os.path.join(ROOT_FILE_PATH, r"Data&Files\GPARTS Part Measures.xlsx")
WHOLESALE_FILE_PATH = os.path.join(ROOT_FILE_PATH, r"Data&Files\Wholesale JAN_Oct_Parts_Ranking_Counter_Invoices_All_Brands.xlsx")
SERVICE_FILE_PATH = os.path.join(ROOT_FILE_PATH, r"Data&Files\Service JAN_Oct_Parts_Ranking_ROs_All_Brands.xlsx")
COUNTERPAD_FILE_PATH = os.path.join(ROOT_FILE_PATH, r"Data&Files\Counter_Pad_11142024.xlsx")




## Variables 

print_df_after_import = False
print_df_data_analyse = True

drop0Dims = False

TIRE_PERCENT1 = 0.5
TIRE_PERCENT2 = 0.9






## Parameters

# Zoning Parameters
Zones=['Red Hot', 'Orange', 'Yellow', 'Green', 'Blue']
thresMultiplier=0.2

totalDaysOfData = 300    # Total Days in Dataset
redHot1SaleTP = 1        # 1 Sell per 1 day
red1SaleTP =  7          # 1 sell per 7 days (1 week)   
orange1SaleTP = 14       # 1 sell per 14 days  (2 weeks) 
yellow1SaleTP = 21       # 1 sell per 21 days  (3 weeks)
green1SaleTP = 30        # 1 sell per 30 days  (1 month)
blue1SaleTP = 10000000     # 1 sell per 10000000 Days (~Rest of Data)

zones = {
    'Red Hot': totalDaysOfData/redHot1SaleTP,
    'Red': totalDaysOfData/red1SaleTP,
    'Orange': totalDaysOfData/orange1SaleTP,
    'Yellow': totalDaysOfData/yellow1SaleTP,
    'Green': totalDaysOfData/green1SaleTP,
    'Blue': totalDaysOfData/blue1SaleTP
}
