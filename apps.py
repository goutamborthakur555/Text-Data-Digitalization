# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 22:56:22 2024

@author: Goutam
"""
############################################################
# =============================================================================
# Libraries required to install
# Importing Libraries
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import streamlit as st
import PyPDF2
from pdf2image import convert_from_path
import pytesseract
# import config
from PIL import Image
from io import StringIO

# Heading of the app
st.markdown("<h1 style='text-align: center; color: #51cc20;'>Trademark Digitalization</h1>",
            unsafe_allow_html=True)
# Small text below the app heading
st.write("""
------------------- AI Powered Legal Trademark Doc Digitalization & Management -------------------
""")

# Adding a banner image
image = Image.open('Trademark_Digitalization.jpg')
st.image(image,use_column_width=True)

st.header("This App will extract all the trademark registration & filing details")


# def file_selector():
try:
    st.sidebar.markdown(
        "<h4 style='text-align: left; color: #3363FF;'>Please upload the PDF(.pdf) file below for data extraction (Max upload size 200MB)!</h4>",
        unsafe_allow_html=True)

    pdf_path = st.sidebar.file_uploader("", type=('pdf'), key='pdf')
    if pdf_path is not None:

        bytes_data = pdf_path.getvalue()
        st.write(bytes_data)

        # To convert to a string based IO:
        stringio = StringIO(pdf_path.getvalue().decode("utf-8"))
        st.write(stringio)

        # To read file as string:
        string_data = stringio.read()
        st.write(string_data)



        # Function to extract text from PDF using PyPDF2 for text-based PDFs
        def extract_text_with_pypdf2(pdf_path):
            text = ""
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                num_pages = len(reader.pages)
                for page_num in range(num_pages):
                    page = reader.pages[page_num]
                    text += f"Page {page_num + 1}:\n"
                    text += page.extract_text() + "\n"
            return text

        # Function to extract text from scanned PDFs using OCR
        def extract_text_with_ocr(pdf_path):
            # Convert PDF pages to images
            pages = convert_from_path(pdf_path)

            # Extract text from each image
            extracted_text = ""
            for page_num, page in enumerate(pages):
                text = pytesseract.image_to_string(page)
                extracted_text += f"Page {page_num + 1}:\n"
                extracted_text += text + "\n"

            return extracted_text

        # # Path to the PDF file
        # pdf_path = config.input_file_loc + config.input_file_name

        # First, try to extract text using PyPDF2
        extracted_text = extract_text_with_pypdf2(pdf_path)

        # If the extracted text is empty, use OCR
        if not extracted_text.strip():
            extracted_text = extract_text_with_ocr(pdf_path)

        # Print the extracted text
        extracted_text = extracted_text.strip()
        # print(extracted_text)

        # # Filter text by Page No.
        import pandas as pd

        # Function to filter text by page number
        def filter_text_by_page(extracted_text, page_number):
            start_page = f"Page {page_number}:"
            end_page = f"Page {page_number + 1}:"

            start_index = extracted_text.find(start_page)
            end_index = extracted_text.find(end_page)

            if start_index == -1:
                return f"Page {page_number} not found."

            if end_index == -1:
                # If the end_page is not found, return text till the end of the document
                return extracted_text[start_index:].strip()

            return extracted_text[start_index:end_index].strip()

        # # Filter text by specific page number
        # page_number = 159
        # filtered_text = filter_text_by_page(extracted_text, page_number)
        # # print(filtered_text + "\n")
        #
        # # ### Remove last line/page no. from text
        # def remove_last_line(text):
        #     # Split the text into lines
        #     lines = text.split("\n")
        #     # Remove the last line
        #     lines = lines[:-1]
        #     # Join the lines back together
        #     result = "\n".join(lines)
        #     return result
        #
        # modified_text = remove_last_line(filtered_text)
        # # print(modified_text)

        # # Export text to text file
        export_text = extracted_text + "\n"

        def export_sentence_to_file(sentence, filename):
            # Open the file in write mode
            with open(filename, "w", encoding="utf-8") as file:
                # Write the sentence to the file
                file.write(sentence)


        # ## Text Cleaning
        sample_text = extracted_text

        # Splitting the text based on Page No. & creating a list
        def split_text_by_pages(text, max_chars=3000):
            import re

            # Regular expression to find page markers like "Page 1:", "Page 2:", etc.
            page_markers = list(re.finditer(r"(Page \d+:)", text))

            # List to hold the pages
            pages = []

            # Append the content between page markers
            for i in range(len(page_markers)):
                start = page_markers[i].start()
                if i < len(page_markers) - 1:
                    end = page_markers[i + 1].start()
                else:
                    end = len(text)

                page_content = text[start:end].strip()

                if page_content:
                    # Ensure the content does not exceed the max characters
                    pages.append(page_content[:max_chars])

            return pages

        # Calling the function to split text by pages
        pages_list = ""
        pages_list = split_text_by_pages(sample_text)
        # pages_list
        # len(pages_list)
        # pages_list[0]

        # # Main Loop
        df_rows = []
        n = 0  # Loop counter starting from 0
        cnt = 1  # Page number counter starting from 1

        df_final = pd.DataFrame(columns=['Page No',
                                         'Trade Marks Journal No',
                                         'Date',
                                         'Class',
                                         'Trademark Number',
                                         'Application Date',
                                         'Applicant',
                                         'Applicant Address',
                                         'Type',
                                         'Agent',
                                         'Agent Address',
                                         'Usage Start Date',
                                         'Jurisdiction',
                                         'Goods/Services',
                                         'Remarks',
                                         'Logo Name/Link'])

        for i in range(0, len(pages_list)):
            raw_text = ""
            raw_text = pages_list[i]

            n = n + 1
            pg_no = cnt
            print(pg_no)

            page = "Page " + str(cnt) + ":\n"
            cnt = cnt + 1

            cond_1 = ""
            cond_1 = sample_text.split(page)[1]

            # Logic 1:
            if (("Trade Marks Journal No" in cond_1) and ("Class" in cond_1) and
                    ("Address for service in India/Agents address:" in raw_text)):

                # Trade Marks Journal No
                try:
                    text1 = raw_text.split("Trade Marks Journal No:")[1].split(",")[0]
                    text1 = text1.strip()
                except:
                    text1 = ""

                # Date
                try:
                    text1a = raw_text.split("Class ")[0].strip().split(" ")[-1].strip()
                    text1a = text1a.strip()
                except:
                    text1a = ""

                # Class
                try:
                    text2 = raw_text.split("Class ")[1].split("\n")[0]
                    text2 = text2.strip()
                except:
                    text2 = ""

                # Trademark Number
                try:
                    text3 = int(raw_text.split("Class ")[1].split("\n")[1].split(" ")[0].strip())
                except:
                    try:
                        text3 = int(raw_text.split("Class ")[1].split("\n")[2].split(" ")[0].strip())
                    except:
                        try:
                            text3 = int(raw_text.split("Class ")[1].split("\n")[3].split(" ")[0].strip())
                        except:
                            text3 = ""

                # Application Date
                applicant_cnt = ""
                applicant_cnt = 1
                try:
                    extr_date = raw_text.split("Class ")[1].split("\n")[1]
                    extr_date = extr_date.strip()

                    if "/" in extr_date:
                        text4 = extr_date.split(" ")[-1].strip()
                        logo_name = ""

                    elif "/" in (
                    raw_text.split("Class ")[1].split("\n")[applicant_cnt + 1].strip().split(" ")[-1].strip()):
                        text4 = raw_text.split("Class ")[1].split("\n")[applicant_cnt + 1].strip().split(" ")[
                            -1].strip()
                        logo_name = extr_date

                    else:
                        text4 = raw_text.split("Class ")[1].split("\n")[applicant_cnt + 2].strip().split(" ")[
                            -1].strip()
                        logo_name = extr_date

                except:
                    try:
                        text4 = raw_text.split("Class ")[1].split("\n")[applicant_cnt + 2].strip().split(" ")[
                            -1].strip()
                        logo_name = ""
                    except:
                        text4 = ""
                        logo_name = ""

                applicant_cnt = applicant_cnt + 1

                # Applicant
                try:
                    extr_nam = raw_text.split(text4)[1].split("\n")[1]
                    extr_nam = extr_nam.strip()

                    if (("/" not in extr_nam) or ('m/' in extr_nam.lower()) or ('/o' in extr_nam.lower())):
                        text5 = extr_nam
                    else:
                        text5 = raw_text.split(text4)[1].split("\n")[2]

                except:
                    text5 = ""

                # Applicant Address
                try:
                    text6a = raw_text.split("Address for service in India")[0].split("\n")[:-2]
                    text6b = "\n".join(text6a)
                    text6c = text6b.split(text5)[-1].replace("\n", " ")

                    if text6c.startswith(","):
                        cleaned_text = text6c[1:]
                    else:
                        cleaned_text = text6c
                    text6 = cleaned_text.strip()

                except:
                    text6 = ""

                # Type
                try:
                    text7 = raw_text.split("Address for service in India")[0].strip()
                    text7 = text7.split("\n")[-1].strip()
                except:
                    text7 = ""

                # Agent
                try:
                    text8 = raw_text.split("Address for service in India/Agents address:")[1].split("\n")[1]
                    text8 = text8.strip()
                except:
                    text8 = ""

                # Agent Address, Usage Start Date, Jurisdiction, Goods/Services
                try:
                    # Agent Address
                    if "Proposed to be Used" in raw_text:
                        text9a = raw_text.split("Proposed to be Used")[0].split(text8)[1].replace("\n", " ")
                        text9 = text9a.strip()

                        # Usage Start Date
                        text10 = "Proposed to be Used"

                        # Jurisdiction
                        text11a = raw_text.split("Proposed to be Used")[1].strip().split("\n")[0]
                        if ":" in text11a:
                            text11 = raw_text.split("Proposed to be Used")[1].strip().split("\n")[2].strip()

                            # Remarks
                            text12a = text11a
                            text12b = raw_text.split("Proposed to be Used")[1].strip().split("\n")[1]
                            text12 = "\n".join([text12a, text12b])

                            address_cnt = ""
                            address_cnt = 2
                        else:
                            text11 = text11a

                            # Remarks:
                            text12 = ""

                            address_cnt = ""
                            address_cnt = 0

                        # Goods/Services:
                        try:
                            address_cnt = address_cnt + 1
                            text14 = raw_text.split("Proposed to be Used\n")[1].split("\n")[address_cnt]
                        except:
                            text14 = ""

                        try:
                            address_cnt = address_cnt + 1
                            text15 = raw_text.split("Proposed to be Used\n")[1].split("\n")[address_cnt]
                        except:
                            text15 = ""

                        try:
                            address_cnt = address_cnt + 1
                            text16 = raw_text.split("Proposed to be Used\n")[1].split("\n")[address_cnt]
                        except:
                            text16 = ""

                        try:
                            address_cnt = address_cnt + 1
                            text17 = raw_text.split("Proposed to be Used\n")[1].split("\n")[address_cnt]
                        except:
                            text17 = ""

                        try:
                            address_cnt = address_cnt + 1
                            text18 = raw_text.split("Proposed to be Used\n")[1].split("\n")[address_cnt]
                        except:
                            text18 = ""

                        try:
                            address_cnt = address_cnt + 1
                            text19 = raw_text.split("Proposed to be Used\n")[1].split("\n")[address_cnt]
                        except:
                            text19 = ""

                        try:
                            address_cnt = address_cnt + 1
                            text20 = raw_text.split("Proposed to be Used\n")[1].split("\n")[address_cnt]
                        except:
                            text20 = ""

                        try:
                            address_cnt = address_cnt + 1
                            text21 = raw_text.split("Proposed to be Used\n")[1].split("\n")[address_cnt]
                        except:
                            text21 = ""

                        try:
                            address_cnt = address_cnt + 1
                            text22 = raw_text.split("Proposed to be Used\n")[1].split("\n")[address_cnt]
                        except:
                            text22 = ""

                        try:
                            address_cnt = address_cnt + 1
                            text23 = raw_text.split("Proposed to be Used\n")[1].split("\n")[address_cnt]
                        except:
                            text23 = ""

                        try:
                            address_cnt = address_cnt + 1
                            text24 = raw_text.split("Proposed to be Used\n")[1].split("\n")[address_cnt]
                        except:
                            text24 = ""

                        try:
                            address_cnt = address_cnt + 1
                            text25 = raw_text.split("Proposed to be Used\n")[1].split("\n")[address_cnt]
                        except:
                            text25 = ""

                        try:
                            address_cnt = address_cnt + 1
                            text26 = raw_text.split("Proposed to be Used\n")[1].split("\n")[address_cnt]
                        except:
                            text26 = ""

                        try:
                            address_cnt = address_cnt + 1
                            text27 = raw_text.split("Proposed to be Used\n")[1].split("\n")[address_cnt]
                        except:
                            text27 = ""

                        try:
                            address_cnt = address_cnt + 1
                            text28 = raw_text.split("Proposed to be Used\n")[1].split("\n")[address_cnt]
                        except:
                            text28 = ""

                        try:
                            address_cnt = address_cnt + 1
                            text29 = raw_text.split("Proposed to be Used\n")[1].split("\n")[address_cnt]
                        except:
                            text29 = ""

                        try:
                            address_cnt = address_cnt + 1
                            text30 = raw_text.split("Proposed to be Used\n")[1].split("\n")[address_cnt]
                        except:
                            text30 = ""

                        try:
                            address_cnt = address_cnt + 1
                            text31 = raw_text.split("Proposed to be Used\n")[1].split("\n")[address_cnt]
                        except:
                            text31 = ""

                        try:
                            address_cnt = address_cnt + 1
                            text32 = raw_text.split("Proposed to be Used\n")[1].split("\n")[address_cnt]
                        except:
                            text32 = ""

                        try:
                            address_cnt = address_cnt + 1
                            text33 = raw_text.split("Proposed to be Used\n")[1].split("\n")[address_cnt]
                        except:
                            text33 = ""

                        try:
                            address_cnt = address_cnt + 1
                            text34 = raw_text.split("Proposed to be Used\n")[1].split("\n")[address_cnt]
                        except:
                            text34 = ""

                        try:
                            address_cnt = address_cnt + 1
                            text35 = raw_text.split("Proposed to be Used\n")[1].split("\n")[address_cnt]
                        except:
                            text35 = ""

                        try:
                            address_cnt = address_cnt + 1
                            text36 = raw_text.split("Proposed to be Used\n")[1].split("\n")[address_cnt]
                        except:
                            text36 = ""

                        desc = "\n".join(
                            [text14, text15, text16, text17, text18, text19, text20, text21, text22, text23,
                             text24, text25, text26, text27, text28, text29, text30, text31, text32, text33,
                             text34, text35, text36][:-1])
                        desc = desc.strip()
                        lines = desc.split('\n')
                        clean_desc = "\n".join(lines[:-1])


                    elif "Used Since" in raw_text:
                        text9a = raw_text.split("Used Since")[0].split(text8)[1].replace("\n", " ")
                        text9 = text9a.strip()

                        # Usage Start Date
                        text10a = raw_text.split("Used Since :")[1].split("\n")[0]
                        text10 = text10a.strip()

                        # Jurisdiction (Check this)
                        text11a = raw_text.split("Used Since :")[1].strip().split("\n")[1]
                        if ":" in text11a:
                            text11 = raw_text.split("Used Since :")[1].strip().split("\n")[3].strip()

                            # Remarks
                            text12a = text11a
                            text12b = raw_text.split("Used Since :")[1].strip().split("\n")[2]
                            text12 = "\n".join([text12a, text12b])

                            address_cnt = ""
                            address_cnt = 3
                        else:
                            text11 = text11a

                            # Remarks:
                            text12 = ""

                            address_cnt = ""
                            address_cnt = 1

                        # Goods/Services:
                        try:
                            address_cnt = address_cnt + 1
                            text14 = raw_text.split("Used Since :")[1].strip().split("\n")[address_cnt]
                        except:
                            text14 = ""

                        try:
                            address_cnt = address_cnt + 1
                            text15 = raw_text.split("Used Since :")[1].split("\n")[address_cnt]
                        except:
                            text15 = ""

                        try:
                            address_cnt = address_cnt + 1
                            text16 = raw_text.split("Used Since :")[1].split("\n")[address_cnt]
                        except:
                            text16 = ""

                        try:
                            address_cnt = address_cnt + 1
                            text17 = raw_text.split("Used Since :")[1].split("\n")[address_cnt]
                        except:
                            text17 = ""

                        try:
                            address_cnt = address_cnt + 1
                            text18 = raw_text.split("Used Since :")[1].split("\n")[address_cnt]
                        except:
                            text18 = ""

                        try:
                            address_cnt = address_cnt + 1
                            text19 = raw_text.split("Used Since :")[1].split("\n")[address_cnt]
                        except:
                            text19 = ""

                        try:
                            address_cnt = address_cnt + 1
                            text20 = raw_text.split("Used Since :")[1].split("\n")[address_cnt]
                        except:
                            text20 = ""

                        try:
                            address_cnt = address_cnt + 1
                            text21 = raw_text.split("Used Since :")[1].split("\n")[address_cnt]
                        except:
                            text21 = ""

                        try:
                            address_cnt = address_cnt + 1
                            text22 = raw_text.split("Used Since :")[1].split("\n")[address_cnt]
                        except:
                            text22 = ""

                        try:
                            address_cnt = address_cnt + 1
                            text23 = raw_text.split("Used Since :")[1].split("\n")[address_cnt]
                        except:
                            text23 = ""

                        try:
                            address_cnt = address_cnt + 1
                            text24 = raw_text.split("Used Since :")[1].split("\n")[address_cnt]
                        except:
                            text24 = ""

                        try:
                            address_cnt = address_cnt + 1
                            text25 = raw_text.split("Used Since :")[1].split("\n")[address_cnt]
                        except:
                            text25 = ""

                        try:
                            address_cnt = address_cnt + 1
                            text26 = raw_text.split("Used Since :")[1].split("\n")[address_cnt]
                        except:
                            text26 = ""

                        try:
                            address_cnt = address_cnt + 1
                            text27 = raw_text.split("Used Since :")[1].split("\n")[address_cnt]
                        except:
                            text27 = ""

                        try:
                            address_cnt = address_cnt + 1
                            text28 = raw_text.split("Used Since :")[1].split("\n")[address_cnt]
                        except:
                            text28 = ""

                        try:
                            address_cnt = address_cnt + 1
                            text29 = raw_text.split("Used Since :")[1].split("\n")[address_cnt]
                        except:
                            text29 = ""

                        try:
                            address_cnt = address_cnt + 1
                            text30 = raw_text.split("Used Since :")[1].split("\n")[address_cnt]
                        except:
                            text30 = ""

                        try:
                            address_cnt = address_cnt + 1
                            text31 = raw_text.split("Used Since :")[1].split("\n")[address_cnt]
                        except:
                            text31 = ""

                        try:
                            address_cnt = address_cnt + 1
                            text32 = raw_text.split("Used Since :")[1].split("\n")[address_cnt]
                        except:
                            text32 = ""

                        try:
                            address_cnt = address_cnt + 1
                            text33 = raw_text.split("Used Since :")[1].split("\n")[address_cnt]
                        except:
                            text33 = ""

                        try:
                            address_cnt = address_cnt + 1
                            text34 = raw_text.split("Used Since :")[1].split("\n")[address_cnt]
                        except:
                            text34 = ""

                        try:
                            address_cnt = address_cnt + 1
                            text35 = raw_text.split("Used Since :")[1].split("\n")[address_cnt]
                        except:
                            text35 = ""

                        try:
                            address_cnt = address_cnt + 1
                            text36 = raw_text.split("Used Since :")[1].split("\n")[address_cnt]
                        except:
                            text36 = ""

                        desc = "\n".join(
                            [text14, text15, text16, text17, text18, text19, text20, text21, text22, text23,
                             text24, text25, text26, text27, text28, text29, text30, text31, text32, text33,
                             text34, text35, text36][:-1])
                        desc = desc.strip()
                        lines = desc.split('\n')
                        clean_desc = "\n".join(lines[:-1])

                    else:
                        text9 = ""
                        text10 = ""
                        text11 = ""
                        clean_desc = ""
                        text12 = ""

                except:
                    text9 = ""
                    text10 = ""
                    text11 = ""
                    clean_desc = ""
                    text12 = ""


            # Logic 2:
            elif (("Trade Marks Journal No" in cond_1) and ("Class" in cond_1) and
                  ("Address for service in India/Attorney address:" in raw_text)):

                # Trade Marks Journal No
                try:
                    text1 = raw_text.split("Trade Marks Journal No:")[1].split(",")[0]
                    text1 = text1.strip()
                except:
                    text1 = ""

                # Date
                try:
                    text1a = raw_text.split("Class ")[0].strip().split(" ")[-1].strip()
                    text1a = text1a.strip()
                except:
                    text1a = ""

                # Class
                try:
                    text2 = raw_text.split("Class ")[1].split("\n")[0]
                    text2 = text2.strip()
                except:
                    text2 = ""

                # Trademark Number
                try:
                    text3 = int(raw_text.split("Class ")[1].split("\n")[1].split(" ")[0].strip())
                except:
                    try:
                        text3 = int(raw_text.split("Class ")[1].split("\n")[2].split(" ")[0].strip())
                    except:
                        try:
                            text3 = int(raw_text.split("Class ")[1].split("\n")[3].split(" ")[0].strip())
                        except:
                            text3 = ""

                # Application Date
                applicant_cnt = ""
                applicant_cnt = 1
                try:
                    extr_date = raw_text.split("Class ")[1].split("\n")[1]
                    extr_date = extr_date.strip()

                    if "/" in extr_date:
                        text4 = extr_date.split(" ")[-1].strip()
                        logo_name = ""

                    elif "/" in (
                    raw_text.split("Class ")[1].split("\n")[applicant_cnt + 1].strip().split(" ")[-1].strip()):
                        text4 = raw_text.split("Class ")[1].split("\n")[applicant_cnt + 1].strip().split(" ")[
                            -1].strip()
                        logo_name = extr_date

                    else:
                        text4 = raw_text.split("Class ")[1].split("\n")[applicant_cnt + 2].strip().split(" ")[
                            -1].strip()
                        logo_name = extr_date

                except:
                    try:
                        text4 = raw_text.split("Class ")[1].split("\n")[applicant_cnt + 2].strip().split(" ")[
                            -1].strip()
                        logo_name = ""
                    except:
                        text4 = ""
                        logo_name = ""

                applicant_cnt = applicant_cnt + 1

                # Applicant
                try:
                    extr_nam = raw_text.split(text4)[1].split("\n")[1]
                    extr_nam = extr_nam.strip()

                    if (("/" not in extr_nam) or ('m/' in extr_nam.lower()) or ('/o' in extr_nam.lower())):
                        text5 = extr_nam
                    else:
                        text5 = raw_text.split(text4)[1].split("\n")[2]

                except:
                    text5 = ""

                # Applicant Address
                try:
                    text6a = raw_text.split("Address for service in India")[0].split("\n")[:-2]
                    text6b = "\n".join(text6a)
                    text6c = text6b.split(text5)[-1].replace("\n", " ")

                    if text6c.startswith(","):
                        cleaned_text = text6c[1:]
                    else:
                        cleaned_text = text6c
                    text6 = cleaned_text.strip()

                except:
                    text6 = ""

                # Type
                try:
                    text7 = raw_text.split("Address for service in India")[0].strip()
                    text7 = text7.split("\n")[-1].strip()
                except:
                    text7 = ""

                # Agent
                try:
                    text8 = raw_text.split("Address for service in India/Attorney address:")[1].split("\n")[1]
                    text8 = text8.strip()
                except:
                    text8 = ""

                # Agent Address, Usage Start Date, Jurisdiction, Goods/Services
                try:
                    # Agent Address
                    if "Proposed to be Used" in raw_text:
                        text9a = raw_text.split("Proposed to be Used")[0].split(text8)[1].replace("\n", " ")
                        text9 = text9a.strip()

                        # Usage Start Date
                        text10 = "Proposed to be Used"

                        # Jurisdiction
                        text11a = raw_text.split("Proposed to be Used")[1].strip().split("\n")[0]
                        if ":" in text11a:
                            text11 = raw_text.split("Proposed to be Used")[1].strip().split("\n")[2].strip()

                            # Remarks
                            text12a = text11a
                            text12b = raw_text.split("Proposed to be Used")[1].strip().split("\n")[1]
                            text12 = "\n".join([text12a, text12b])

                            address_cnt = ""
                            address_cnt = 2
                        else:
                            text11 = text11a

                            # Remarks:
                            text12 = ""

                            address_cnt = ""
                            address_cnt = 0

                        # Goods/Services:
                        try:
                            address_cnt = address_cnt + 1
                            text14 = raw_text.split("Proposed to be Used\n")[1].split("\n")[address_cnt]
                        except:
                            text14 = ""

                        try:
                            address_cnt = address_cnt + 1
                            text15 = raw_text.split("Proposed to be Used\n")[1].split("\n")[address_cnt]
                        except:
                            text15 = ""

                        try:
                            address_cnt = address_cnt + 1
                            text16 = raw_text.split("Proposed to be Used\n")[1].split("\n")[address_cnt]
                        except:
                            text16 = ""

                        try:
                            address_cnt = address_cnt + 1
                            text17 = raw_text.split("Proposed to be Used\n")[1].split("\n")[address_cnt]
                        except:
                            text17 = ""

                        try:
                            address_cnt = address_cnt + 1
                            text18 = raw_text.split("Proposed to be Used\n")[1].split("\n")[address_cnt]
                        except:
                            text18 = ""

                        try:
                            address_cnt = address_cnt + 1
                            text19 = raw_text.split("Proposed to be Used\n")[1].split("\n")[address_cnt]
                        except:
                            text19 = ""

                        try:
                            address_cnt = address_cnt + 1
                            text20 = raw_text.split("Proposed to be Used\n")[1].split("\n")[address_cnt]
                        except:
                            text20 = ""

                        try:
                            address_cnt = address_cnt + 1
                            text21 = raw_text.split("Proposed to be Used\n")[1].split("\n")[address_cnt]
                        except:
                            text21 = ""

                        try:
                            address_cnt = address_cnt + 1
                            text22 = raw_text.split("Proposed to be Used\n")[1].split("\n")[address_cnt]
                        except:
                            text22 = ""

                        try:
                            address_cnt = address_cnt + 1
                            text23 = raw_text.split("Proposed to be Used\n")[1].split("\n")[address_cnt]
                        except:
                            text23 = ""

                        try:
                            address_cnt = address_cnt + 1
                            text24 = raw_text.split("Proposed to be Used\n")[1].split("\n")[address_cnt]
                        except:
                            text24 = ""

                        try:
                            address_cnt = address_cnt + 1
                            text25 = raw_text.split("Proposed to be Used\n")[1].split("\n")[address_cnt]
                        except:
                            text25 = ""

                        try:
                            address_cnt = address_cnt + 1
                            text26 = raw_text.split("Proposed to be Used\n")[1].split("\n")[address_cnt]
                        except:
                            text26 = ""

                        try:
                            address_cnt = address_cnt + 1
                            text27 = raw_text.split("Proposed to be Used\n")[1].split("\n")[address_cnt]
                        except:
                            text27 = ""

                        try:
                            address_cnt = address_cnt + 1
                            text28 = raw_text.split("Proposed to be Used\n")[1].split("\n")[address_cnt]
                        except:
                            text28 = ""

                        try:
                            address_cnt = address_cnt + 1
                            text29 = raw_text.split("Proposed to be Used\n")[1].split("\n")[address_cnt]
                        except:
                            text29 = ""

                        try:
                            address_cnt = address_cnt + 1
                            text30 = raw_text.split("Proposed to be Used\n")[1].split("\n")[address_cnt]
                        except:
                            text30 = ""

                        try:
                            address_cnt = address_cnt + 1
                            text31 = raw_text.split("Proposed to be Used\n")[1].split("\n")[address_cnt]
                        except:
                            text31 = ""

                        try:
                            address_cnt = address_cnt + 1
                            text32 = raw_text.split("Proposed to be Used\n")[1].split("\n")[address_cnt]
                        except:
                            text32 = ""

                        try:
                            address_cnt = address_cnt + 1
                            text33 = raw_text.split("Proposed to be Used\n")[1].split("\n")[address_cnt]
                        except:
                            text33 = ""

                        try:
                            address_cnt = address_cnt + 1
                            text34 = raw_text.split("Proposed to be Used\n")[1].split("\n")[address_cnt]
                        except:
                            text34 = ""

                        try:
                            address_cnt = address_cnt + 1
                            text35 = raw_text.split("Proposed to be Used\n")[1].split("\n")[address_cnt]
                        except:
                            text35 = ""

                        try:
                            address_cnt = address_cnt + 1
                            text36 = raw_text.split("Proposed to be Used\n")[1].split("\n")[address_cnt]
                        except:
                            text36 = ""

                        desc = "\n".join(
                            [text14, text15, text16, text17, text18, text19, text20, text21, text22, text23,
                             text24, text25, text26, text27, text28, text29, text30, text31, text32, text33,
                             text34, text35, text36][:-1])
                        desc = desc.strip()
                        lines = desc.split('\n')
                        clean_desc = "\n".join(lines[:-1])


                    elif "Used Since" in raw_text:
                        text9a = raw_text.split("Used Since")[0].split(text8)[1].replace("\n", " ")
                        text9 = text9a.strip()

                        # Usage Start Date
                        text10a = raw_text.split("Used Since :")[1].split("\n")[0]
                        text10 = text10a.strip()

                        # Jurisdiction (Check this)
                        text11a = raw_text.split("Used Since :")[1].strip().split("\n")[1]
                        if ":" in text11a:
                            text11 = raw_text.split("Used Since :")[1].strip().split("\n")[3].strip()

                            # Remarks
                            text12a = text11a
                            text12b = raw_text.split("Used Since :")[1].strip().split("\n")[2]
                            text12 = "\n".join([text12a, text12b])

                            address_cnt = ""
                            address_cnt = 3
                        else:
                            text11 = text11a

                            # Remarks:
                            text12 = ""

                            address_cnt = ""
                            address_cnt = 1

                        # Goods/Services:
                        try:
                            address_cnt = address_cnt + 1
                            text14 = raw_text.split("Used Since :")[1].split("\n")[address_cnt]
                        except:
                            text14 = ""

                        try:
                            address_cnt = address_cnt + 1
                            text15 = raw_text.split("Used Since :")[1].split("\n")[address_cnt]
                        except:
                            text15 = ""

                        try:
                            address_cnt = address_cnt + 1
                            text16 = raw_text.split("Used Since :")[1].split("\n")[address_cnt]
                        except:
                            text16 = ""

                        try:
                            address_cnt = address_cnt + 1
                            text17 = raw_text.split("Used Since :")[1].split("\n")[address_cnt]
                        except:
                            text17 = ""

                        try:
                            address_cnt = address_cnt + 1
                            text18 = raw_text.split("Used Since :")[1].split("\n")[address_cnt]
                        except:
                            text18 = ""

                        try:
                            address_cnt = address_cnt + 1
                            text19 = raw_text.split("Used Since :")[1].split("\n")[address_cnt]
                        except:
                            text19 = ""

                        try:
                            address_cnt = address_cnt + 1
                            text20 = raw_text.split("Used Since :")[1].split("\n")[address_cnt]
                        except:
                            text20 = ""

                        try:
                            address_cnt = address_cnt + 1
                            text21 = raw_text.split("Used Since :")[1].split("\n")[address_cnt]
                        except:
                            text21 = ""

                        try:
                            address_cnt = address_cnt + 1
                            text22 = raw_text.split("Used Since :")[1].split("\n")[address_cnt]
                        except:
                            text22 = ""

                        try:
                            address_cnt = address_cnt + 1
                            text23 = raw_text.split("Used Since :")[1].split("\n")[address_cnt]
                        except:
                            text23 = ""

                        try:
                            address_cnt = address_cnt + 1
                            text24 = raw_text.split("Used Since :")[1].split("\n")[address_cnt]
                        except:
                            text24 = ""

                        try:
                            address_cnt = address_cnt + 1
                            text25 = raw_text.split("Used Since :")[1].split("\n")[address_cnt]
                        except:
                            text25 = ""

                        try:
                            address_cnt = address_cnt + 1
                            text26 = raw_text.split("Used Since :")[1].split("\n")[address_cnt]
                        except:
                            text26 = ""

                        try:
                            address_cnt = address_cnt + 1
                            text27 = raw_text.split("Used Since :")[1].split("\n")[address_cnt]
                        except:
                            text27 = ""

                        try:
                            address_cnt = address_cnt + 1
                            text28 = raw_text.split("Used Since :")[1].split("\n")[address_cnt]
                        except:
                            text28 = ""

                        try:
                            address_cnt = address_cnt + 1
                            text29 = raw_text.split("Used Since :")[1].split("\n")[address_cnt]
                        except:
                            text29 = ""

                        try:
                            address_cnt = address_cnt + 1
                            text30 = raw_text.split("Used Since :")[1].split("\n")[address_cnt]
                        except:
                            text30 = ""

                        try:
                            address_cnt = address_cnt + 1
                            text31 = raw_text.split("Used Since :")[1].split("\n")[address_cnt]
                        except:
                            text31 = ""

                        try:
                            address_cnt = address_cnt + 1
                            text32 = raw_text.split("Used Since :")[1].split("\n")[address_cnt]
                        except:
                            text32 = ""

                        try:
                            address_cnt = address_cnt + 1
                            text33 = raw_text.split("Used Since :")[1].split("\n")[address_cnt]
                        except:
                            text33

                        try:
                            address_cnt = address_cnt + 1
                            text34 = raw_text.split("Used Since :")[1].split("\n")[address_cnt]
                        except:
                            text34 = ""

                        try:
                            address_cnt = address_cnt + 1
                            text35 = raw_text.split("Used Since :")[1].split("\n")[address_cnt]
                        except:
                            text35 = ""

                        try:
                            address_cnt = address_cnt + 1
                            text36 = raw_text.split("Used Since :")[1].split("\n")[address_cnt]
                        except:
                            text36 = ""

                        desc = "\n".join(
                            [text14, text15, text16, text17, text18, text19, text20, text21, text22, text23,
                             text24, text25, text26, text27, text28, text29, text30, text31, text32, text33,
                             text34, text35, text36][:-1])
                        desc = desc.strip()
                        lines = desc.split('\n')
                        clean_desc = "\n".join(lines[:-1])

                    else:
                        text9 = ""
                        text10 = ""
                        text11 = ""
                        clean_desc = ""
                        text12 = ""

                except:
                    text9 = ""
                    text10 = ""
                    text11 = ""
                    clean_desc = ""
                    text12 = ""


            # Logic 3:
            elif (("Trade Marks Journal No" in cond_1) and ("Class" in cond_1) and
                  (("Address for service in India/Agents address:" not in raw_text) or
                   ("Address for service in India/Attorney address:" not in raw_text))):

                # Trade Marks Journal No
                try:
                    text1 = raw_text.split("Trade Marks Journal No:")[1].split(",")[0]
                    text1 = text1.strip()
                except:
                    text1 = ""

                # Date
                try:
                    text1a = raw_text.split("Class ")[0].strip().split(" ")[-1].strip()
                    text1a = text1a.strip()
                except:
                    text1a = ""

                # Class
                try:
                    text2 = raw_text.split("Class ")[1].split("\n")[0]
                    text2 = text2.strip()
                except:
                    text2 = ""

                # Trademark Number
                try:
                    text3 = int(raw_text.split("Class ")[1].split("\n")[1].split(" ")[0].strip())
                except:
                    try:
                        text3 = int(raw_text.split("Class ")[1].split("\n")[2].split(" ")[0].strip())
                    except:
                        try:
                            text3 = int(raw_text.split("Class ")[1].split("\n")[3].split(" ")[0].strip())
                        except:
                            text3 = ""

                # Application Date
                applicant_cnt = ""
                applicant_cnt = 1
                try:
                    extr_date = raw_text.split("Class ")[1].split("\n")[1]
                    extr_date = extr_date.strip()

                    if "/" in extr_date:
                        text4 = extr_date.split(" ")[-1].strip()
                        logo_name = ""

                    elif "/" in (
                    raw_text.split("Class ")[1].split("\n")[applicant_cnt + 1].strip().split(" ")[-1].strip()):
                        text4 = raw_text.split("Class ")[1].split("\n")[applicant_cnt + 1].strip().split(" ")[
                            -1].strip()
                        logo_name = extr_date

                    else:
                        text4 = raw_text.split("Class ")[1].split("\n")[applicant_cnt + 2].strip().split(" ")[
                            -1].strip()
                        logo_name = extr_date

                except:
                    try:
                        text4 = raw_text.split("Class ")[1].split("\n")[applicant_cnt + 2].strip().split(" ")[
                            -1].strip()
                        logo_name = ""
                    except:
                        text4 = ""
                        logo_name = ""

                applicant_cnt = applicant_cnt + 1

                # Applicant
                try:
                    extr_nam = raw_text.split(text4)[1].split("\n")[1]
                    extr_nam = extr_nam.strip()

                    if (("/" not in extr_nam) or ('m/' in extr_nam.lower()) or ('/o' in extr_nam.lower())):
                        text5 = extr_nam
                    else:
                        text5 = raw_text.split(text4)[1].split("\n")[2]

                except:
                    text5 = ""

                # Applicant Address
                try:
                    text6a = raw_text.split("Proposed to be Used")[0].strip().split("\n")[-3].strip()
                    text6b = raw_text.split("Proposed to be Used")[0].strip().split("\n")[-2].strip()
                    text6 = "\n".join([text6a, text6b])

                except:
                    text6 = ""

                # Type
                try:
                    text7 = raw_text.split("Proposed to be Used")[0].strip().split("\n")[-1]
                    text7 = text7.strip()
                except:
                    text7 = ""

                # Agent
                try:
                    text8 = ""
                except:
                    text8 = ""

                # Agent Address, Usage Start Date, Jurisdiction, Goods/Services
                try:
                    # Agent Address
                    if "Proposed to be Used" in raw_text:
                        text9 = ""

                        # Usage Start Date
                        text10 = "Proposed to be Used"

                        # Jurisdiction
                        text11 = raw_text.split("Proposed to be Used")[1].strip().split("\n")[0].strip()

                        # Remarks
                        text12 = ""

                        # Goods/Services:
                        try:
                            text14 = raw_text.split("Proposed to be Used")[1].strip().split("\n")[1].strip()
                        except:
                            text14 = ""

                        try:
                            text15 = raw_text.split("Proposed to be Used")[1].strip().split("\n")[2].strip()
                        except:
                            text15 = ""

                        try:
                            text16 = raw_text.split("Proposed to be Used")[1].strip().split("\n")[3].strip()
                        except:
                            text16 = ""

                        try:
                            text17 = raw_text.split("Proposed to be Used")[1].strip().split("\n")[4].strip()
                        except:
                            text17 = ""

                        try:
                            text18 = raw_text.split("Proposed to be Used")[1].strip().split("\n")[5].strip()
                        except:
                            text18 = ""

                        try:
                            text19 = raw_text.split("Proposed to be Used")[1].strip().split("\n")[6].strip()
                        except:
                            text19 = ""

                        try:
                            text20 = raw_text.split("Proposed to be Used")[1].strip().split("\n")[7].strip()
                        except:
                            text20 = ""

                        try:
                            text21 = raw_text.split("Proposed to be Used")[1].strip().split("\n")[8].strip()
                        except:
                            text21 = ""

                        try:
                            text22 = raw_text.split("Proposed to be Used")[1].strip().split("\n")[9].strip()
                        except:
                            text22 = ""

                        try:
                            text23 = raw_text.split("Proposed to be Used")[1].strip().split("\n")[10].strip()
                        except:
                            text23 = ""

                        try:
                            text24 = raw_text.split("Proposed to be Used")[1].strip().split("\n")[11].strip()
                        except:
                            text24 = ""

                        try:
                            text25 = raw_text.split("Proposed to be Used")[1].strip().split("\n")[12].strip()
                        except:
                            text25 = ""

                        try:
                            text26 = raw_text.split("Proposed to be Used")[1].strip().split("\n")[13].strip()
                        except:
                            text26 = ""

                        try:
                            text27 = raw_text.split("Proposed to be Used")[1].strip().split("\n")[14].strip()
                        except:
                            text27 = ""

                        try:
                            text28 = raw_text.split("Proposed to be Used")[1].strip().split("\n")[15].strip()
                        except:
                            text28 = ""

                        try:
                            text29 = raw_text.split("Proposed to be Used")[1].strip().split("\n")[16].strip()
                        except:
                            text29 = ""

                        try:
                            text30 = raw_text.split("Proposed to be Used")[1].strip().split("\n")[17].strip()
                        except:
                            text30 = ""

                        try:
                            text31 = raw_text.split("Proposed to be Used")[1].strip().split("\n")[18].strip()
                        except:
                            text31 = ""

                        try:
                            text32 = raw_text.split("Proposed to be Used")[1].strip().split("\n")[19].strip()
                        except:
                            text32 = ""

                        try:
                            text33 = raw_text.split("Proposed to be Used")[1].strip().split("\n")[20].strip()
                        except:
                            text33 = ""

                        try:
                            text34 = raw_text.split("Proposed to be Used")[1].strip().split("\n")[21].strip()
                        except:
                            text34 = ""

                        try:
                            text35 = raw_text.split("Proposed to be Used")[1].strip().split("\n")[22].strip()
                        except:
                            text35 = ""

                        try:
                            text36 = raw_text.split("Proposed to be Used")[1].strip().split("\n")[23].strip()
                        except:
                            text36 = ""

                        desc = "\n".join(
                            [text14, text15, text16, text17, text18, text19, text20, text21, text22, text23,
                             text24, text25, text26, text27, text28, text29, text30, text31, text32, text33,
                             text34, text35, text36][:-1])
                        desc = desc.strip()
                        lines = desc.split('\n')
                        clean_desc = "\n".join(lines[:-1])


                    elif "Used Since" in raw_text:
                        text9a = raw_text.split("Used Since")[0].split(text8)[1].replace("\n", " ")
                        text9 = text9a.strip()

                        # Usage Start Date
                        text10a = raw_text.split("Used Since :")[1].split("\n")[0]
                        text10 = text10a.strip()

                        # Jurisdiction (Check this)
                        text11 = raw_text.split("Used Since :")[1].strip().split("\n")[1]

                        # Remakrs
                        text12 = ""

                        # Goods/Services:
                        try:
                            text14 = raw_text.split("Used Since :")[1].split("\n")[2]
                        except:
                            text14 = ""

                        try:
                            text15 = raw_text.split("Used Since :")[1].split("\n")[3]
                        except:
                            text15 = ""

                        try:
                            text16 = raw_text.split("Used Since :")[1].split("\n")[4]
                        except:
                            text16 = ""

                        try:
                            text17 = raw_text.split("Used Since :")[1].split("\n")[5]
                        except:
                            text17 = ""

                        try:
                            text18 = raw_text.split("Used Since :")[1].split("\n")[6]
                        except:
                            text18 = ""

                        try:
                            text19 = raw_text.split("Used Since :")[1].split("\n")[7]
                        except:
                            text19 = ""

                        try:
                            text20 = raw_text.split("Used Since :")[1].split("\n")[8]
                        except:
                            text20 = ""

                        try:
                            text21 = raw_text.split("Used Since :")[1].split("\n")[9]
                        except:
                            text21 = ""

                        try:
                            text22 = raw_text.split("Used Since :")[1].split("\n")[10]
                        except:
                            text22 = ""

                        try:
                            text23 = raw_text.split("Used Since :")[1].split("\n")[11]
                        except:
                            text23 = ""

                        try:
                            text24 = raw_text.split("Used Since :")[1].split("\n")[12]
                        except:
                            text24 = ""

                        try:
                            text25 = raw_text.split("Used Since :")[1].split("\n")[13]
                        except:
                            text25 = ""

                        try:
                            text26 = raw_text.split("Used Since :")[1].split("\n")[14]
                        except:
                            text26 = ""

                        try:
                            text27 = raw_text.split("Used Since :")[1].split("\n")[15]
                        except:
                            text27 = ""

                        try:
                            text28 = raw_text.split("Used Since :")[1].split("\n")[16]
                        except:
                            text28 = ""

                        try:
                            text29 = raw_text.split("Used Since :")[1].split("\n")[17]
                        except:
                            text29 = ""

                        try:
                            text30 = raw_text.split("Used Since :")[1].split("\n")[18]
                        except:
                            text30 = ""

                        try:
                            text31 = raw_text.split("Used Since :")[1].split("\n")[19]
                        except:
                            text31 = ""

                        try:
                            text32 = raw_text.split("Used Since :")[1].split("\n")[20]
                        except:
                            text32 = ""

                        try:
                            text33 = raw_text.split("Used Since :")[1].split("\n")[21]
                        except:
                            text33 = ""

                        try:
                            text34 = raw_text.split("Used Since :")[1].split("\n")[22]
                        except:
                            text34 = ""

                        try:
                            text35 = raw_text.split("Used Since :")[1].split("\n")[23]
                        except:
                            text35 = ""

                        try:
                            text36 = raw_text.split("Used Since :")[1].split("\n")[24]
                        except:
                            text36 = ""

                        desc = "\n".join(
                            [text14, text15, text16, text17, text18, text19, text20, text21, text22, text23,
                             text24, text25, text26, text27, text28, text29, text30, text31, text32, text33,
                             text34, text35, text36][:-1])
                        desc = desc.strip()
                        lines = desc.split('\n')
                        clean_desc = "\n".join(lines[:-1])

                    else:
                        text9 = ""
                        text10 = ""
                        text11 = ""
                        clean_desc = ""
                        text12 = ""

                except:
                    text9 = ""
                    text10 = ""
                    text11 = ""
                    clean_desc = ""
                    text12 = ""


            # Logic 4:
            else:
                text1 = ""
                text1a = ""
                text2 = ""
                text3 = ""
                text4 = ""
                text5 = ""
                text6 = ""
                text7 = ""
                text8 = ""
                text9 = ""
                text10 = ""
                text11 = ""
                clean_desc = ""
                text12 = ""
                logo_name = ""

            # For rows to be append
            df_rows.append([pg_no, text1, text1a, text2, text3, text4, text5, text6, text7, text8, text9,
                            text10, text11, clean_desc, text12, logo_name])
            # print(df_rows)

            # Appending 4 records at a time in the excel file
            if n % 20 == 0 or n == len(pages_list):
                df_final = df_final.append(pd.DataFrame(df_rows, columns=df_final.columns))
                df_rows = []

                # # Exporting the dataframe to excel file
                # df_final.to_excel(config.output_file_loc + "Output_File.xlsx", index=False)
                #
                # print("Exported to excel...")

            # Extracting data only for 5 records
            # if n==5:
            # break

        # # Removing the Junk Records
        # Define the condition for rows to be deleted
        df_final_fltrd = df_final['Date'].apply(lambda x: isinstance(x, str) and ('/' in x) and (len(x) >= 9))

        # Filter the DataFrame
        df_final_cleaned = df_final[df_final_fltrd]
        df_final_cleaned.shape

        # Reseting the index of the df_final_cleaned DataFrame
        df_final_cleaned.reset_index(drop=True, inplace=True)

        st.markdown("<h3 style='text-align: left; color: #33A1FF;'>Your's Extracted Data</h3>", unsafe_allow_html=True)
        st.write(df_final_cleaned)

        # Exporting the dataframe to excel file
        # df_final_cleaned.to_excel(config.output_file_loc + "Output_File_Cleaned.xlsx", index=False)

        import base64
        from io import BytesIO

        def to_excel(df_final_cleaned):
            output = BytesIO()
            writer = pd.ExcelWriter(output, engine='xlsxwriter')
            df_final_cleaned.to_excel(writer, columns=header, index=False, sheet_name='Sheet1')
            writer.save()
            processed_data = output.getvalue()
            return processed_data

        def get_table_download_link(df_final_cleaned):
            val = to_excel(df_final_cleaned)
            b64 = base64.b64encode(val)
            return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="Extracted Data File.xlsx">Download Extracted File</a>'

        st.markdown(get_table_download_link(df_final_cleaned), unsafe_allow_html=True)


    if st.button('About the App'):
        st.text("""
In today's fast-paced digital landscape, intellectual property (IP) assets such as trademarks are crucial identifiers of brand identity and for the legal services, digitalizing (keeping in online/cloud) all the trademark registration & filing details from a vast array of documents has become increasingly complex, time-consuming and challenging. To address this challenge, we propose the use of Deep Learning and Natural Language Processing (NLP) technologies to capture all the trademarks and related registration information from diverse array of documents. Brief process flow:
• Data Collection: Extracting the data from link provide by client using Web Scraping
• Pre-processing of unstructured input data (pdf files):
    o Converting pdf to image
    o Enhancing contrast, sharpness and resizing
    o Image Localization/Normalization
• Applying Tesseract OCR (Optical Character Reader)/ pytesseract library to extract text from the images.
• Training on the input data: However, if the accuracy is not good, we will go ahead with the custom training on the input images of different patterns.
• Testing/Validation of results: Validate the results on unseen images/pdf
• User Interface for Results: Post validation, we will publish the results in Google Drive/Sheet and in user interface which will be created using Streamlit framework.

This approach significantly improves accuracy and speed in processing large datasets, providing legal professionals with precise and reliable insights. The project aims to streamline the trademark management process, resulting in enhanced productivity, cost savings and scalability for legal consulting teams.

""")

        st.text('Thank you for visiting!')

# try:
#     data = file_selector()
except Exception as e:
    st.write("**Error:** Your uploaded file have some issue! Please recheck and upload the correct file!", e)

