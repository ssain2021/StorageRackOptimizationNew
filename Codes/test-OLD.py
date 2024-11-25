import pandas as pd
from tabulate import tabulate
import numpy as np
import re

# Read (AKINS FoMoCo_Piece_Sales_112222_YTD.xlsx)
df = pd.read_excel(r"D:\Sukhendu\UPWORK-WORK\0_Dondray_Auto\Data&Files\AKINS FoMoCo_Piece_Sales_112222_YTD.xlsx", 0)
print(tabulate(df.head(3), headers = 'keys', tablefmt = 'simple'))
print(tabulate(df.head(3), headers = 'keys', tablefmt = 'github'))
print(tabulate(df.head(3), headers = 'keys', tablefmt = 'fancy_grid'))
print(tabulate(df.head(3), headers = 'keys', tablefmt = 'grid'))
print(tabulate(df.head(3), headers = 'keys', tablefmt = 'pipe'))
print(tabulate(df.head(3), headers = 'keys', tablefmt = 'orgtbl'))
print(tabulate(df.head(3), headers = 'keys', tablefmt = 'jira'))
print(tabulate(df.head(3), headers = 'keys', tablefmt = 'html'))
print(tabulate(df.head(3), headers = 'keys', tablefmt = 'latex'))
print(tabulate(df.head(3), headers = 'keys', tablefmt = 'psql'))



# Read (GPARTS Part Measures.xlsx)
# df = pd.read_excel(r"C:\Sukhendu\UPWORK-WORK\0_Dondray_Auto\GPARTS Part Measures.xlsx", 0)
# print(tabulate(df.head(300), headers = 'keys', tablefmt = 'psql'))

custom_headers = ['Mfg', 'Src', 'Cost', 'List', 'Bin', 'Part Number', 'Description', 'OH']

# Read (Counter_Pad_11142024.xlsx) 
#df = pd.read_excel(r"D:\Sukhendu\UPWORK-WORK\0_Dondray_Auto\Data&Files\Counter_Pad_11142024.xlsx", 0)
#df = pd.DataFrame(df.iloc[0, 0].split('\n'))
#print(tabulate(df.head(1), headers='keys', tablefmt='psql'))
#print(df.columns)
# df = pd.DataFrame(df.iloc[0, 0].split('\n'))

# data = []
# for i in range(df.shape[0]):
#     items = [item for item in df.iloc[i, 0].split('  ') if item.strip()]
#     if len(items) > 0:
#         data.append(items)
    
# # Define your desired headers
# custom_headers = ['Mfg', 'Src', 'Cost', 'List', 'Bin', 'Part Number', 'Description', 'OH']

# # Create the DataFrame with custom headers
# df_new = pd.DataFrame(data, columns=custom_headers)

# def handle_cost_comma(row):
#     cost_value = row['Cost']
#     if ' ' in cost_value:
#         cost_parts = cost_value.split()
#         if len(cost_parts) >= 2:
#             # Shift subsequent columns          
#             row['OH'] = row['Description']
#             row['Description'] = row['Part Number']
#             row['Part Number'] = row['Bin'] 
#             row['Bin'] = row['List']
#             # Split cost into two parts
#             row['Cost'] = cost_parts[0].strip()
#             row['List'] = cost_parts[1].strip() + ' '
    
#     return row

# print(tabulate(df_new.head(100), headers='keys', tablefmt='psql'))

# #  Handle Comma in Cost column. Split the Column and Shift next columns
# mask = df_new['Cost'].str.contains(' ')
# df_new.loc[mask, :] = df_new.loc[mask, :].apply(handle_cost_comma, axis=1)

# print(tabulate(df_new.head(100), headers='keys', tablefmt='psql'))
# print("\nNumber of rows affected:", mask.sum())

#Function to split a string into columns based on double spaces
# def split_string_into_columns(text):
#     return re.split(r'\s{2,}', text)

# # Apply the function to each cell in the DataFrame
# df_split = df.applymap(split_string_into_columns)

# # Function to handle lists in a cell
# def handle_lists(series):
#     # If all values are lists, explode them
#     if all(isinstance(x, list) for x in series):
#         return pd.Series([item for sublist in series for item in sublist])
#     # Otherwise, just return the original series
#     return series

# # Apply the function to each cell in the DataFrame
# df_split = df_split.apply(handle_lists)

# # Explode the resulting lists into separate rows
# df_exploded = df_split.explode(df_split.columns)

# # Reset the index to get a clean DataFrame
# df_counter_final = df_exploded.reset_index(drop=True)

# # Print the result
# print(tabulate(df_counter_final.head(20), headers='keys', tablefmt='psql'))

# Read (Wholesale JAN_Oct_Parts_Ranking_Counter_Invoices_All_Brands.xlsx) 
# df_wholesale = pd.read_excel(r"C:\Sukhendu\UPWORK-WORK\0_Dondray_Auto\Wholesale JAN_Oct_Parts_Ranking_Counter_Invoices_All_Brands.xlsx", 0)

# df_wholesale1 = df_wholesale[['Vendor', 'Source', 'Part Number', 'Description','Avg. Cost', 'Price', 'Sold', 'Sold.1', 'Gross Profit']]
# df_wholesale_Ford = df_wholesale1[df_wholesale1['Vendor'] == 'FOR']

# print(tabulate(df_wholesale_Ford.head(250), headers = 'keys', tablefmt = 'psql'))


#['Vendor', 'Source', 'Part Number', 'Description', 'Unnamed: 4', 'Unnamed: 5', 'Unnamed: 6', 'Unnamed: 7', 'Unnamed: 8', 'Avg. Cost', 'Price', 'Sold', 'Unnamed: 12', 'Sold.1', 'Unnamed: 14', 'Gross Profit']





