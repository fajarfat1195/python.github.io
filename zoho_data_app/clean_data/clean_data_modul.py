import pandas as pd
import re
import numpy as np
from fractions import Fraction

def beambox(df):
    
    f_1 = (df['Lead Source Description'] == 'Beambox')
    # mengambil data yang email, phone dan mobilenya tidak kosong
    final_filter = (
        f_1 
        )

    return final_filter

def purple_wifi(df):
    
    f_1 = (df['Lead Source Description'] == 'Purple Wifi')
    # mengambil data yang email, phone dan mobilenya tidak kosong
    final_filter = (
        f_1 
        )

    return final_filter

def get_df_update(df, cc_before, country):

    new_df = df.loc[
    (df['Phone'].str.contains(cc_before, regex=True)) &
    (df['Country'].str.contains(country, regex=True, flags=re.I))
    ].copy()

    new_df.reset_index(drop=True, inplace=True)
    return new_df

def clean_spec_char_exc_plus(df):
    df['Phone'].replace(' ','', regex=True, inplace=True)
    df['Phone'].replace('\-','', regex=True, inplace=True)
    df['Mobile'].replace(' ','', regex=True, inplace=True)
    df['Mobile'].replace('\-','', regex=True, inplace=True)

def user_req_crm(df, country):
    
    f_1 = (df['Country'] == country)
    final_filter = (
        f_1
        )

    return final_filter

def get_country_update(df, country_before):

    new_df = df.loc[
    (df['Country'].str.contains(country_before, regex=True, flags=re.I))
    ].copy()

    new_df.reset_index(drop=True, inplace=True)
    return new_df

def get_loc(df):
    
    f_1 = (df['Lead Locations'].str.contains('songhai', regex=True, flags=re.I))
    # f_1 = (df['Lead Locations'].str.contains('Karma Sitabani, Corbett', regex=True))
    # mengambil data yang email, phone dan mobilenya tidak kosong
    c_1 = ~(df['Email'].isna() & df['Mobile'].isna() & df['Phone'].isna()) 
    final_filter = (

        f_1
        )

    return final_filter

def custom(df):
    
    f_1 = (df['Lead Sub-Brand'] == 'Other India DB')
    f_2 = (df['Lead Source'] == 'Club IN')
    # mengambil data yang email, phone dan mobilenya tidak kosong
    final_filter = (
        f_1 &
        f_2 
        )

    return final_filter
