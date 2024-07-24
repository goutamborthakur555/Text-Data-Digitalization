# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 22:56:22 2024

@author: Goutam
"""
############################################################
# =============================================================================
# Libraries required to install
import os
import pandas as pd
import numpy as np
import fitz  # PyMuPDF
from PIL import Image
import pytesseract
from PIL import Image
import io

# Configure the input file path/location & file name:
input_file_loc = "../Input Dataset/DataSource1_NewFormat/JournalNo_PublicationDate/2152_15042024/"
input_file_name = "CLASS 1 - 4.pdf"

# Configure the output file path/location:
output_file_loc = "../Output/"

# Path to the ChromeDriver
chrome_driver_path = "../Util/"

# Configure the pdf download file path/location
pdf_download_dir = "../Input Dataset/Downloaded_PDF/"

# Configure the files path/location to be consolidate
logo_log_dir = "../Output/Logos_log.xlsx"
output_cleaned_dir = "../Output/Output_File_Cleaned.xlsx"


# # Testing:
# input_file_name = "ABC.xlsx"
# test_input_path = pd.read_excel(input_file_loc + "ABC.xlsx")
# print(test_input_path.shape)


