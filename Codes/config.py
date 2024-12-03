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



## Variables NEW ZONING ALGO BAsed Sale Frequency, (NOT Sale Vol Percentage) Below are Sale per Day
TOTAL_DAYS = 300        ##  Total Days in Dataset
RED_HOT_SALE = 1        ## 1 Sell per 1 day
RED_SALE =  7           ## 1 sell per 7 days (1 week)   
ORANGE_SALE = 14        ## 1 sell per 14 days  (2 weeks) 
YELLOW_SALE = 21        ## 1 sell per 21 days  (3 weeks)
GREEN_SALE = 30         ## 1 sell per 30 days  (1 month)
BLUE_SALE = 60 


TIRE_PERCENT1 = 0.5
TIRE_PERCENT2 = 0.9
SKUcnt = 10
print_df_after_import = True
print_df_data_analyse = True

## Parameters
Zones=['Red Hot', 'Orange', 'Yellow', 'Green', 'Blue']
thresMultiplier=0.2