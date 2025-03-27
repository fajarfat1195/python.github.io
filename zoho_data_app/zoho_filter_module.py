import pandas as pd
import numpy as np
from datetime import datetime

import re

def user_req(df):
    

    f_1 = (df['Lead Sub-Brand'].str.contains('Karma Experience', regex=True, flags=re.I))
    f_2 = ~(df['Email'].str.contains('karmagroup.com'))
    c_1 = ~(df['Email'].isna() & df['Mobile'].isna() & df['Phone'].isna()) 
    final_filter = (
        f_1 &
        f_2 &
        c_1
    )

    return final_filter


def pg_sg(df):
    
    f_1 = (df['Lead Source'] == 'Past Guests')
    f_2 = (df['Country'].str.contains('singapore', regex=True, flags=re.I))
    # mengambil data yang email, phone dan mobilenya tidak kosong
    c_1 = ~(df['Email'].isna() & df['Mobile'].isna() & df['Phone'].isna()) 
    final_filter = (

        (f_1) &
        (f_2) &
        c_1
        )

    return final_filter

def user_req_wifi_karma_beach(df):
    
    f_1 = (df['Lead Source'].str.contains('wifi', regex=True, flags=re.I))
    f_2 = (df['Lead Locations'].str.contains('karma beach', regex=True, flags=re.I))
    # mengambil data yang email, phone dan mobilenya tidak kosong
    c_1 = ~(df['Email'].isna() & df['Mobile'].isna() & df['Phone'].isna()) 
    final_filter = (

        (f_1) &
        (f_2) &
        c_1
        )

    return final_filter

def user_req_on_island(df):
    
    f_1 = (df['Lead Source Description'].str.contains('guest survey', regex=True, flags=re.I))
    f_2 = (df['Country'].str.contains('indonesia', regex=True, flags=re.I))
    # mengambil data yang email, phone dan mobilenya tidak kosong
    c_1 = ~(df['Email'].isna() & df['Mobile'].isna() & df['Phone'].isna()) 
    final_filter = (

        (f_1) &
        (f_2) &
        c_1
        )

    return final_filter

def user_req_bali_hospitality(df):
    
    f_1 = (df['Lead Source'].str.contains('bali hospitality|hospitality industry', regex=True, flags=re.I))
    # mengambil data yang email, phone dan mobilenya tidak kosong
    c_1 = ~(df['Email'].isna() & df['Mobile'].isna() & df['Phone'].isna()) 
    final_filter = (

        (f_1) &
        c_1
        )

    return final_filter


def user_req_bali_expat(df):
    
    f_1 = (df['Lead Source Description'].str.contains('bali expat', regex=True, flags=re.I))
    f_2 = (df['Lead Locations'].str.contains('bali expat', regex=True, flags=re.I))
    # mengambil data yang email, phone dan mobilenya tidak kosong
    c_1 = ~(df['Email'].isna() & df['Mobile'].isna() & df['Phone'].isna()) 
    final_filter = (

        (f_1) |
        (f_2) &
        c_1
        )

    return final_filter

def user_req_bali_karma_beach_vip(df):
    
    f_1 = (df['Lead Source']=='Karma Beach VIP')
    # mengambil data yang email, phone dan mobilenya tidak kosong
    c_1 = ~(df['Email'].isna() & df['Mobile'].isna() & df['Phone'].isna()) 
    final_filter = (

        (f_1) &
        c_1
        )

    return final_filter

def user_req_bali_karma_beach(df):
    
    f_1 = (df['Lead Sub-Brand'].str.contains('karma beach', regex=True, flags=re.I))
    f_2 = (df['Lead Source']!='Karma Beach VIP')
    # mengambil data yang email, phone dan mobilenya tidak kosong
    c_1 = ~(df['Email'].isna() & df['Mobile'].isna() & df['Phone'].isna()) 
    final_filter = (

        (f_1) &
        (f_2) &
        c_1
        )

    return final_filter


def user_req_bali(df):
    
    f_1 = (df['City'].str.contains('^bali$|ubud|gianyar|denpasar|badung|canggu', regex=True, flags=re.I))
    f_2 = (df['State'].str.contains('^bali$|ubud|gianyar|denpasar|badung|canggu', regex=True, flags=re.I))
    # mengambil data yang email, phone dan mobilenya tidak kosong
    c_1 = ~(df['Email'].isna() & df['Mobile'].isna() & df['Phone'].isna()) 
    final_filter = (

        (f_1) |
        (f_2) &
        c_1
        )

    return final_filter

def user_req_phone_indo(df):
    
    f_1 = (df['Phone'].str.contains('^\+62361|^\+62|^62361|^62', regex=True, flags=re.I))
    # mengambil data yang email, phone dan mobilenya tidak kosong
    c_1 = ~(df['Email'].isna() & df['Mobile'].isna() & df['Phone'].isna()) 
    final_filter = (

        (f_1) &
        c_1
        )

    return final_filter

def user_req_crm(df, country):
    
    f_1 = (df['Country'].str.contains(country, regex=True, flags=re.I))
    final_filter = (
        f_1 
        )

    return final_filter


def user_req_ge(df):
    f_1 = (df['Lead Source'].str.contains('guest exit', regex=True, flags=re.I))
    f_2 = (df['Country'].str.contains('united kingdom|wales|england|scotland|northern ireland', regex=True, flags=re.I))
    f_3 = (df['Phone'].str.contains('^44|^\+44'))
    final_filter = (
        f_1 &
        f_2 &
        # f_3
        (f_2 | f_3)
        )

    return final_filter

def user_req_tm(df):
    f_1 = (df['Lead Brand'].str.contains('Timeshare Marketing', regex=True, flags=re.I))
    f_2 = (~df['Lead Source'].str.contains('guest exit', regex=True, flags=re.I))
    f_3 = (df['Country'].str.contains('united kingdom|wales|england|scotland|northern ireland', regex=True, flags=re.I))
    f_4 = (df['Phone'].str.contains('^44|^\+44'))
    final_filter = (
        f_1 &
        f_2 & 
        # f_3
        (f_3 | f_4)
        )

    return final_filter

def user_req_tm_au(df):
    f_1 = (df['Lead Brand'].str.contains('Timeshare Marketing', regex=True, flags=re.I))
    f_2 = (~df['Lead Source'].str.contains('guest exit', regex=True, flags=re.I))
    f_3 = (df['Country'].str.contains('australia', regex=True, flags=re.I))
    # f_4 = (df['Phone'].str.contains('^44|^\+44'))
    final_filter = (
        f_1 &
        f_2 & 
        f_3
        # (f_3 | f_4)
        )

    return final_filter

def user_req_tm_id(df):
    f_1 = (df['Lead Brand'].str.contains('Timeshare Marketing', regex=True, flags=re.I))
    f_2 = (~df['Lead Source'].str.contains('guest exit', regex=True, flags=re.I))
    f_3 = (df['Country'].str.contains('indonesia', regex=True, flags=re.I))
    # f_4 = (df['Phone'].str.contains('^44|^\+44'))
    final_filter = (
        f_1 &
        f_2 & 
        f_3
        # (f_3 | f_4)
        )

    return final_filter

def user_req_wifi(df):
    
    f_1 = (df['Lead Source'] == 'Wifi')
    f_2 = ((df['Country'].str.contains('australia|united kingdom|indonesia', regex=True, flags=re.I))| df['Phone'].str.contains('^61|^\+61|^44|^\+44|^08|^62|^\+62', regex=True))
    f_3 = ((df['Birthdate'].notna()) | (df['Year of Birth'].notna()))
    f_4 = (df['Email'].notna())
    f_5 = (df['Lead Locations'].str.contains('beach', regex=True, flags=re.I))
    c_1 = ~(df['Email'].isna() & df['Mobile'].isna() & df['Phone'].isna()) 
    final_filter = (
        f_1 &
        f_2 &
        f_3 &
        f_4 &
        f_5 &
        c_1
        )

    return final_filter



def user_req_guest_exit(df):
    
    f_1 = (df['Lead Source'] == 'Guest Exit')|(df['Lead Source'] == 'KE2 (Guest Exit)')
    f_2 = (df['Created Time'].dt.strftime('%Y') == '2023')
    # mengambil data yang email, phone dan mobilenya tidak kosong
    c_1 = ~(df['Email'].isna() & df['Mobile'].isna() & df['Phone'].isna()) 
    final_filter = (

        f_1 &
        f_2 &
        c_1
        )

    return final_filter

def user_req_yuk_tamasya(df):
    
    f_1 = (df['Lead Sub-Brand'] == 'Yuk Tamasya')
    f_2 = (df['Created Time'].dt.strftime('%Y') == '2023')
    # mengambil data yang email, phone dan mobilenya tidak kosong
    c_1 = ~(df['Email'].isna() & df['Mobile'].isna() & df['Phone'].isna()) 
    final_filter = (

        f_1 &
        f_2 &
        c_1
        )

    return final_filter

def user_req_keau(df):
    
    f_1 = (df['Lead Sub-Brand'] == 'Karma Experience AU')
    # f_2 = (df['Created Time'].dt.strftime('%Y') == '2023')
    # mengambil data yang email, phone dan mobilenya tidak kosong
    c_1 = ~(df['Email'].isna() & df['Mobile'].isna() & df['Phone'].isna()) 
    final_filter = (

        f_1 &
        # f_2 &
        c_1
        )

    return final_filter



def gdpr_checked(df):
    f_1 = (df['GDPR Compliant']=='true')

    # mengambil data yang email, phone dan mobilenya tidak kosong
    c_1 = ~(df['Email'].isna() & df['Mobile'].isna() & df['Phone'].isna()) 
    final_filter = (
        f_1 &
        c_1
        )

    return final_filter

def gdpr_checked_opt_in_unchecked(df):
    f_1 = (df['GDPR Compliant']=='true')
    f_2 = (df['Opt In']=='false')

    # mengambil data yang email, phone dan mobilenya tidak kosong
    c_1 = ~(df['Email'].isna() & df['Mobile'].isna() & df['Phone'].isna()) 
    final_filter = (
        f_1 &
        f_2 &
        c_1
        )

    return final_filter

def opt_in_checked(df):
    f_1 = (df['Opt In']=='true')

    # mengambil data yang email, phone dan mobilenya tidak kosong
    c_1 = ~(df['Email'].isna() & df['Mobile'].isna() & df['Phone'].isna()) 
    final_filter = (
        f_1 &
        c_1
        )

    return final_filter

def newsletter(df):
    f_1 = (df['Lead Source Description'].str.contains('newsletter', regex=True, flags=re.I)) | (df['Lead Source'] == 'Newsletter')

    # mengambil data yang email, phone dan mobilenya tidak kosong
    c_1 = ~(df['Email'].isna() & df['Mobile'].isna() & df['Phone'].isna()) 
    final_filter = (f_1 & c_1)

    return final_filter
    
def drop_newsletter(df):
    f_exc_1 = ((df['Lead Brand'] == 'Timeshare Marketing') | (df['Lead Brand'] == 'Other'))
    f_exc_2 = (df['Lead Sub-Brand'] == 'Karma Sanctum')
    f_exc_3 = ((df['Lead Source'] == 'Bamboo') | (df['Lead Source'] == 'Chairman database'))
    final_filter = (f_exc_1 | f_exc_2 | f_exc_3)

    return final_filter

def only_source_past_guests(df):

    # convert data kolom menjadi format tanggal menggunakan pandas
    # supaya bisa menggunakan filter tanggal
    df['Created Time'] = pd.to_datetime(df['Created Time'], errors='coerce')

    f_1 = (df['Lead Brand'] == 'Karma Resorts')
    f_2 = (df['Lead Sub-Brand'] == 'Other')
    f_3 = (df['Lead Source'] == 'Past Guests')
    f_4 = ~(df['Email'].str.contains('karmagroup.com'))
    c_1 = ~(df['Email'].isna() & df['Mobile'].isna() & df['Phone'].isna()) 

    # mengambil data yang email, phone dan mobilenya tidak kosong
    
    final_filter = (
        f_1 & 
        f_2 & 
        f_3 & 
        f_4 & 
        c_1 
    )

    return final_filter


def past_guest_by_cc_country(df):
    
    f_1 = (df['Lead Source'] == 'Past Guests')
    f_2a = (df['Country'].str.contains('indonesia', regex=True, flags=re.I))
    f_2b = (df['Phone'].str.contains('^62|^\+62', regex=True))
    c_1 = ~(df['Email'].isna() & df['Mobile'].isna() & df['Phone'].isna()) 
    final_filter = (
        f_1 &
        (f_2a | f_2b) &
        c_1
        )

    return final_filter

def past_guest(df):
    
    f_1 = (df['Lead Source'] == 'Past Guests')
    c_1 = ~(df['Email'].isna() & df['Mobile'].isna() & df['Phone'].isna()) 
    final_filter = (
        f_1 &
        c_1
        )

    return final_filter


def user_backup_crm(df):
    
    f_1 = (df['Lead Brand'].str.contains('karma resorts|karma group', regex=True, flags=re.I))
    f_2 = (df['Lead Sub-Brand'].str.contains('house of karma', regex=True, flags=re.I))
    f_3 = (df['Lead Source'].str.contains('guest exit|chairman database|bamboo', regex=True, flags=re.I))
    f_4 = (df['Lead Source Description'].str.contains('di Mare', regex=True, flags=re.I))
    final_filter = (
        (f_1) |
        (f_2) |
        (f_3) |
        (f_4)
        )

    return final_filter

def get_eu():
    eu = ['Russia', 'Germany', 'France', 'Italy', 'Spain','Ukraine','Poland','Romania','Netherlands','Belgium','Czechia','Greece','Portugal','Sweden','Hungary',
        'Belarus','Austria','Serbia','Switzerland','Bulgaria','Denmark','Finland','Slovakia','Norway','Ireland','Croatia','Moldova','Bosnia','Herzegovina','Albania','Lithuania',
        'North Macedonia','Slovenia','Latvia','Kosovo','Estonia','Montenegro','Luxembourg','Malta','Iceland','Andorra','Monaco','Liechtenstein','San Marino','Holy See',
        'Czech Republic','Israel','New Caledonia','Republic of Cyprus']
    return eu

def get_uk():
    uk = ['England', 'United Kingdom', 'Wales', 'Scotland', 'Northern ireland']
    return uk

def get_eu_uk():
    eu_uk =  ['Russia', 'Germany', 'France', 'Italy', 'Spain','Ukraine','Poland','Romania','Netherlands','Belgium','Czechia','Greece','Portugal','Sweden','Hungary',
        'Belarus','Austria','Serbia','Switzerland','Bulgaria','Denmark','Finland','Slovakia','Norway','Ireland','Croatia','Moldova','Bosnia','Herzegovina','Albania','Lithuania',
        'North Macedonia','Slovenia','Latvia','Kosovo','Estonia','Montenegro','Luxembourg','Malta','Iceland','Andorra','Monaco','Liechtenstein','San Marino','Holy See',
        'Czech Republic','Israel','New Caledonia','Republic of Cyprus', 'England', 'United Kingdom', 'Wales', 'Scotland', 'Northern ireland']
    
    return eu_uk

def pg_eu_uk(df):
    f_1 = (df['Lead Source'] == 'Past Guests')
    f_2 = (df['Country'].str.contains('|'.join(get_eu_uk()), regex=True, flags=re.I))
    c_1 = ~(df['Email'].isna() & df['Mobile'].isna() & df['Phone'].isna()) 
    final_filter = (
        f_1 &
        f_2 &
        c_1 
    )

    return final_filter