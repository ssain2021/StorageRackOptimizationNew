from config import *
from tqdm import tqdm
import pandas as pd
import numpy as np
import math
import openpyxl
import utils


def readFiles(dimenFile, soldFile1, soldFile2, invenFile, dimenCols, sold1Cols, sold2Cols, invenCols, filterVendor):
    df_dimenFile = utils.read_excel(dimenFile)      
    if filterVendor: df_dimenFile = df_dimenFile[(df_dimenFile[dimenCols['Vendor']] == filterVendor)].reset_index()
    df_soldFile1 = utils.read_excel(soldFile1)
    if filterVendor: df_soldFile1 = df_soldFile1[(df_soldFile1[sold1Cols['Vendor']] == filterVendor)].reset_index()
    df_soldFile2 = utils.read_excel(soldFile2)
    if filterVendor: df_soldFile2 = df_soldFile2[(df_soldFile2[sold2Cols['Vendor']] == filterVendor)].reset_index()
    df_Inven = utils.read_excel(invenFile)
    if filterVendor: df_Inven = df_Inven[(df_Inven[invenCols['Vendor']] == filterVendor)].reset_index()
    return df_dimenFile, df_soldFile1, df_soldFile2, df_Inven


def zoningStorageFunc(filterVendor, dimenFile, depthCol, widthCol, heightCol, soldFile1, soldFile2, soldCol1, soldCol2, invenFile, invenCol):

