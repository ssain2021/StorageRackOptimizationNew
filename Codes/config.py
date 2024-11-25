################################  config.py  ####################################
# Author: Sukhendu Sain
# Description: Config file of codebase. Houses different parameters and variables
# Data: 23-Nov-2024
#################################################################################
import os

## Files Path ##
ROOT_FILE_PATH = '\\'.join(os.getcwd().split('\\')[:-1])

AKINS_FOMO_FILE_PATH = os.path.join(ROOT_FILE_PATH, r"Data&Files\AKINS FoMoCo_Piece_Sales_112222_YTD.xlsx")
GPARTS_FILE_PATH = os.path.join(ROOT_FILE_PATH, r"Data&Files\GPARTS Part Measures.xlsx")
WHOLESALE_FILE_PATH = os.path.join(ROOT_FILE_PATH, r"Data&Files\Wholesale JAN_Oct_Parts_Ranking_Counter_Invoices_All_Brands.xlsx")
SERVICE_FILE_PATH = os.path.join(ROOT_FILE_PATH, r"Data&Files\Service JAN_Oct_Parts_Ranking_ROs_All_Brands.xlsx")
COUNTERPAD_FILE_PATH = os.path.join(ROOT_FILE_PATH, r"Data&Files\Counter_Pad_11142024.xlsx")
