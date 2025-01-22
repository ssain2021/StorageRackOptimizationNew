def zoningStorageFunc(dimenFile, depthCol, widthCol, heightCol, soldFiles, invenFile, invenCol):
    df_dimenFile = utils.read_excel(dimenFile)


    for soldFile, soldCol in soldFiles:
        
    df_Wholesale = utils.read_excel(WHOLESALE_FILE_PATH)

    # Clean the Wholesale Dataframe
    df_Wholesale['Description'] = df_Wholesale['Description'].astype(str)
    df_Wholesale = df_Wholesale.drop(columns=[col for col in df_Wholesale.columns if 'Unnamed' in col], inplace=False)
    df_Wholesale = df_Wholesale[(df_Wholesale['Vendor'] == 'FOR')].reset_index()
    df_Wholesale.loc[df_Wholesale['Description'].apply(lambda x: len(x.split("      ")) > 1), 'Avg. Cost'] = df_Wholesale['Description'].apply(lambda x: [i for i in x.strip().split("      ")][-1])
    df_Wholesale.loc[df_Wholesale['Description'].apply(lambda x: len(x.split("      ")) > 1), 'Description'] = df_Wholesale['Description'].apply(lambda x: "     ".join([i for i in x.strip().split("      ")][:-1]))

    if print_df_after_import: utils.print_df(df_Wholesale) # Print the Dataframe
    # ~7 secs



    ## @ Read FILE:: (Service JAN_Oct_Parts_Ranking_ROs_All_Brands.xlsx) into Dataframe
    df_Service = utils.read_excel(SERVICE_FILE_PATH)

    # Clean the Service Dataframe
    df_Service['Description'] = df_Service['Description'].astype(str)
    df_Service = df_Service.drop(columns=[col for col in df_Service.columns if 'Unnamed' in col], inplace=False)
    df_Service = df_Service[(df_Service['Vendor'] == 'FOR')].reset_index()
    df_Service.loc[df_Service['Description'].apply(lambda x: len(x.split("      ")) > 1), 'Avg. Cost'] = df_Service['Description'].apply(lambda x: [i for i in x.strip().split("      ")][-1])
    df_Service.loc[df_Service['Description'].apply(lambda x: len(x.split("      ")) > 1), 'Description'] = df_Service['Description'].apply(lambda x: "     ".join([i for i in x.strip().split("      ")][:-1]))
    df_Service.loc[df_Service['Qty Sold'].apply(lambda x: len(str(x).split("      ")) > 1), 'Dollars Sold'] = df_Service['Qty Sold'].apply(lambda x: [i for i in str(x).strip().split("      ")][-1])
    df_Service.loc[df_Service['Qty Sold'].apply(lambda x: len(str(x).split("      ")) > 1), 'Qty Sold'] = df_Service['Qty Sold'].apply(lambda x: "     ".join([i for i in str(x).strip().split("      ")][:-1]))

    if print_df_after_import: utils.print_df(df_Service, 100) # Print the Dataframe


    df_CounterPad1 = utils.read_excel(COUNTERPAD_FILE_PATH, 0, None)
    df_CounterPad2 = utils.read_excel(COUNTERPAD_FILE_PATH, 1, None)

    df_CounterPad = pd.concat([df_CounterPad1, df_CounterPad2])

    df_CounterPad.columns = df_CounterPad.iloc[1, :]
    df_CounterPad = df_CounterPad.rename(columns={'Part #': 'Part#'}) # Rename the 'Part #' column to 'Part#'
    df_CounterPad = df_CounterPad[(df_CounterPad['Vendor'] == 'FOR')].reset_index()
