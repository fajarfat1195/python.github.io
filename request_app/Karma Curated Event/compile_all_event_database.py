# %%
import pandas as pd
import gspread
import kc_event_modul as kc
from fractions import Fraction
import re
import numpy as np

import main_module as m

# Pastikan permision access di menu "Share" di rubah ke anyone with the link terlebih dahulu, agar bisa mengunakan cara OAuth
# Jika Ingin lebih dibatasi menggunakan cara google service account lebih disarankan

gc = gspread.oauth(
    credentials_filename= r'C:\Users\fajar\Documents\Python\Data\Google Credentials\karma-oauth.json'
)

# sheet_id = {
#     "2024": '1k-70BJNRm01RE2S7gBXuOfqxofk1gYz4g6lPbLUCklw',
#     "2025": '1AfxaROCWtYuCWPo31LYonED-qQ1y196lytIh2IAydxQ'
# }

sheet_id = {
    "2023": '15bYOR2R6r20lvVUyVoVbYRdUr_8aiE02Ege-QT3cCi0',
    "2024": '1k-70BJNRm01RE2S7gBXuOfqxofk1gYz4g6lPbLUCklw',
    "2025": '1AfxaROCWtYuCWPo31LYonED-qQ1y196lytIh2IAydxQ'
}

# SHEET_ID_DATABASE = '1AfxaROCWtYuCWPo31LYonED-qQ1y196lytIh2IAydxQ'
SHEET_ID_DATABASE = '1k-70BJNRm01RE2S7gBXuOfqxofk1gYz4g6lPbLUCklw'
SHEET_DATABASE = 'DB'

execeptional_list = [
    'DB', 
    'DV', 
    'List Events Transition',
    'Summary Report',
    'PAST EVENTS - Summary Report',
    'Past Attedants',
    'Template'
    ]


# %%
# # Open the spreadsheet
# spreadsheet_source = gc.open_by_key(SHEET_ID_SOURCE)

# # Get all sheet names
# sheet_names = [sheet.title for sheet in spreadsheet_source.worksheets()]
# sheet_names_id = [sheet.id for sheet in spreadsheet_source.worksheets()]
# print(sheet_names_id)

# %%
spreadsheet_db = gc.open_by_key(SHEET_ID_DATABASE)
worksheet_db = spreadsheet_db.worksheet(SHEET_DATABASE)
rows_db = worksheet_db.get_all_records()
# rows_db = worksheet_db.get_all_records()

# %%
df = kc.get_file_sheets(sheet_id, execeptional_list, gc)
df

# %%
m.clean_number(df, 'Tel/Phone')
m.clean_number(df, 'Member No')

df['Status'] = df['Status'].str.title()
df['Event Status'] = df['Event Status'].str.title()
df['Membership Type'] = df['Membership Type'].str.title()
df['Servicing Office'] = df['Servicing Office'].str.upper()

# %%
df.columns

# %%
# df.to_csv(r'C:\Users\fajar\Documents\Python\Data\test.csv', index=False)

# %%
# df.drop(df.loc[df['No'] == ''].index, inplace=True)
# df.reset_index(drop=True, inplace=True)

df['Event Date From'] = pd.to_datetime(df['Event Date From'], format='mixed')
df['Event Date From'] = df['Event Date From'].dt.strftime('%d %b %Y')
df['Event Date To'] = pd.to_datetime(df['Event Date To'], format='mixed')
df['Event Date To'] = df['Event Date To'].dt.strftime('%d %b %Y')
df['Dob'] = pd.to_datetime(df['Dob'], format='mixed')
df['Dob'] = df['Dob'].dt.strftime('%d %b %Y')
df['Event Name'] = df['Event Name'].str.upper()

df.loc[~df['Email'].str.contains('@'), 'Email'] = ''

# %%
df.fillna('', inplace=True)
# df.to_csv(r'C:\Users\fajar\Documents\Python\Data\test.csv', index=False)

# %%
df.values.tolist()

# %%
df.columns

# %%
worksheet_db.clear()
worksheet_db.update([df.columns.values.tolist()] + df.values.tolist())


