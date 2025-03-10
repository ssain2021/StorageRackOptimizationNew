################################  config.py  ####################################
# Author: Sukhendu Sain
# Description: Config file of codebase. Houses different parameters and variables
# Data: 23-Nov-2024
#################################################################################
import os

## @ Files Path ##
ROOT_FILE_PATH = '\\'.join(os.getcwd().split('\\')[:-1])

GPARTS_FILE_PATH = os.path.join(ROOT_FILE_PATH, r"Data&Files\GPARTS Part Measures.xlsx")
WHOLESALE_FILE_PATH = os.path.join(ROOT_FILE_PATH, r"Data&Files\Wholesale JAN_Oct_Parts_Ranking_Counter_Invoices_All_Brands.xlsx")
SERVICE_FILE_PATH = os.path.join(ROOT_FILE_PATH, r"Data&Files\Service JAN_Oct_Parts_Ranking_ROs_All_Brands.xlsx")
COUNTERPAD_FILE_PATH = os.path.join(ROOT_FILE_PATH, r"Data&Files\Counter_Pad_011425.xlsx")




## @ Variables ##

print_df_after_import = False
print_df_data_analyse = True

drop0Dims = False




## @ Parameters ##

## * Zoning Parameters
# TODO: Clarify for other Zones
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


## * Storage Parameters
tirePercent = 0.5      ##  50% of tires are 33 inches, or more
fillFactor = 0.7       #  70% Filling, 30% Open Space for DRAWER / RACK / SHELVE




