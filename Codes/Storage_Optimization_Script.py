# %%
################################  Storage_Optimization.ipynb  ####################################
# Author: Sukhendu Sain
# Description: Main file of codebase. Houses main code
# Data: 22-Nov-2024
#################################################################################

# %%
# Import Necessary Libraries, Utils, and Config Files
import utils
from config import *
import pandas as pd
# import importlib
# importlib.reload(utils)

# %% [markdown]
# # Data Import and Clean

# %%
#### Read FILE:: (AKINS FoMoCo_Piece_Sales_112222_YTD.xlsx) into Dataframe
df_Akins = utils.read_excel(AKINS_FOMO_FILE_PATH)
df_Akins
#utils.print_df(df_Wholesale_Ford) # Print the Dataframe
# 

# %%
#### Read FILE:: (GPARTS Part Measures.xlsx) into Dataframe
df_Gparts = utils.read_excel(GPARTS_FILE_PATH)
utils.print_df(df_Gparts) # Print the Dataframe

print(df_Gparts[df_Gparts["Prod Att - Length"] == 0].shape[0]) # Print the Rows with 0 Dimensions

# %%
#### Read FILE:: (Wholesale JAN_Oct_Parts_Ranking_Counter_Invoices_All_Brands.xlsx) into Dataframe
df_Wholesale = utils.read_excel(WHOLESALE_FILE_PATH)

# Clean the Wholesale Dataframe
df_Wholesale = df_Wholesale.drop(columns=[col for col in df_Wholesale.columns if 'Unnamed' in col], inplace=False)
df_Wholesale_Ford = df_Wholesale[df_Wholesale['Vendor'] == 'FOR'] # Put only 'Ford' Brand Data into another DF

utils.print_df(df_Wholesale_Ford) # Print the Dataframe

# %%
#### Read FILE:: (Service JAN_Oct_Parts_Ranking_ROs_All_Brands.xlsx) into Dataframe
df_Service = utils.read_excel(SERVICE_FILE_PATH)

# Clean the Service Dataframe
df_Service = df_Service.drop(columns=[col for col in df_Service.columns if 'Unnamed' in col], inplace=False)
df_Service_Ford = df_Service[df_Service['Vendor'] == 'FOR'] # Put only 'Ford' Brand Data into another DF

utils.print_df(df_Service_Ford, 100) # Print the Dataframe

# %%
# df_CounterPad = utils.read_excel(COUNTERPAD_FILE_PATH)
# data = df_CounterPad.iloc[0,0]

# # Split the data into lines
# lines = data.strip().split('\n')

# # Create a list to store the parsed data
# parsed_data = []

# # Parse each line
# for line in lines:
#     # Split the line into columns
#     columns = line.split()
    
#     # Extract the data
#     mfg = columns[0]
#     src = columns[1]
#     cost = float(columns[2].replace(',', ''))
#     list_price = float(columns[3].replace(',', ''))
#     bin = columns[4]
#     part_number = columns[5]
#     oh = float(columns[-1])
    
#     # Extract the description (all columns between part_number and OH)
#     description = ' '.join(columns[6:-1])
    
#     # Add the parsed data to the list
#     parsed_data.append({
#         'Mfg': mfg,
#         'Src': src,
#         'Cost': cost,
#         'List': list_price,
#         'Bin': bin,
#         'Part Number': part_number,
#         'Description': description,
#         'OH': oh
#     })

# # Convert the list of dictionaries to a pandas DataFrame
# df = pd.DataFrame(parsed_data)

# # Print the DataFrame
# utils.print_df(df, 100)

# %%


# %% [markdown]
# # Data Analysis
# 

# %%
## Find Number of Matching Part Numbers in each of the Dataframe

# The Dataframes to match
all_dfs = [df_Wholesale_Ford, df_Gparts]

# Part# Column Name of each DF
part_number_columns = ['Part Number', 'Svc Part Number']

# Find common part numbers
common_part_numbers = set(all_dfs[0][part_number_columns[0]])
for i in range(1, len(all_dfs)):
    common_part_numbers &= set(all_dfs[i][part_number_columns[i]])

print(f"Part numbers common to all DataFrames: {len(common_part_numbers)}")
utils.print_df(df_Wholesale_Ford[df_Wholesale_Ford["Part Number"].isin(common_part_numbers)], 100)

# %%
## Find Rows with 0 in either Dimensions

# Print the Rows with 0 Dimensions
print(f"Numer of Rows with 0 Dimensions: {df_Gparts[df_Gparts["Prod Att - Length"] == 0].shape[0]}, {(df_Gparts[df_Gparts["Prod Att - Length"] == 0].shape[0]/df_Gparts.shape[0])*100}%") 
utils.print_df(df_Gparts[df_Gparts["Prod Att - Length"] == 0], 10) # Print top 10 Rows with 0 Dimensions

# %%


# %% [markdown]
# # Data Processing & Calculation

# %%
## Sort the 'Wholesale..' DF by 'Sort Pcs' Columns in Descending order
# Sold Pcs/Sold = Sales Frequency

df_Wholesale_Ford["Total Sold"] = df_Wholesale_Ford["Sold"] +  df_Wholesale_Ford["Sold.1"]
df_Wholesale_Ford.sort_values(['Total Sold'], ascending=False, inplace=True)

# %%
df_Wholesale_Ford

# %%
data = []
sum = 0
totalSoldPCs = int(df_Wholesale_Ford["Total Sold"].sum())
print(sum, totalSoldPCs)
for i in range(df_Wholesale_Ford.shape[0]):
    zone = ""
    if sum/totalSoldPCs <= 0.2:
        zone = "Red_Hot_Zone"
    if sum/totalSoldPCs > 0.2 and sum/totalSoldPCs <= 0.4:
        zone = "Orange_Zone"
    if sum/totalSoldPCs > 0.4 and sum/totalSoldPCs <= 0.6:
        zone = "Yellow_Zone"
    if sum/totalSoldPCs > 0.6 and sum/totalSoldPCs <= 0.8:
        zone = "Green_Zone"
    if sum/totalSoldPCs > 0.8:
        zone = "Blue_Zone"
    data.append([df_Wholesale_Ford["Part Number"].iloc[i], zone, sum])
    sum = sum + df_Wholesale_Ford["Total Sold"].iloc[i]
df_zones = pd.DataFrame(data)
utils.print_df(df_zones,None)

with open("htt.txt", "w") as f:
    f.write(df_zones.to_string())

# %%



