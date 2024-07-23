# %%
import pandas as pd
import numpy as np
from datetime import date
from datetime import datetime
from datetime import datetime, timedelta
from pandas import json_normalize

import re

import sys
sys.path.append('../')

import zoho_crm_api_module as crm
import zoho_campaign_api_module as campaign
import requests

import sys
sys.path.append('../../../zoho_data_app/')

# importing
import main_module as m
import zoho_filter_module as fil

# %%
cols = [
    'Created_Time', 
    'id', 
    'First_Name', 
    'Last_Name', 
    'Email', 
    'Phone', 
    'Mobile', 
    'Brand', 
    'Lead_Sub_Brand', 
    'Lead_Source', 
    'Lead_Regions',
    'Lead_Locations', 
    'City', 
    'Nationality', 
    'Country', 
    'Booking_Status', 
    'Guest_Type', 
    'Email_Opt_In',
    'Email_Opt_Out', 
    'BookRef',
    'Email_status', 
    'Odyssey_Members', 
    'Do_Not_Mail', 
    'Do_Not_Contact'
]

# %%
campaign_token = campaign.get_campaign_token()
crm_token = crm.get_crm_token()

# %%
df = crm.get_newsletter_data(crm_token, cols)
df.fillna('empty', inplace=True)
new_df = crm.get_newsletter_data_filter(df)
new_df.sort_values('Created_Time', ascending=True, inplace=True)
new_df.reset_index(drop=True, inplace=True)
count_data_awal = new_df.shape[0]

# %%
new_df['First_Name'] = new_df['First_Name'].str.title()
new_df['Last_Name'] = new_df['Last_Name'].str.title()
new_df['Email'] = m.lowercase(new_df, 'Email')
m.clean_space(new_df, 'Email')

new_df
# new_df.to_excel(r"C:\Users\fajar\Documents\Python\Data\newsletter_zoho.xlsx", index=False)

# %%
# # mencari tanggal 8 hari kebelekang
# calculate_date = datetime.now() - timedelta(days=8)
# new_cal_date = str(calculate_date.strftime("%Y-%m-%d")).split(' ')
# first_date = new_cal_date[0]

# # mencari tanggal hari ini
# today = datetime.now() 
# second_date = today.strftime("%Y-%m-%d")

# print(first_date)
# print(second_date)

# %%
# new_df['Lead_Locations']

# %%
new_df.replace('empty', '', inplace=True)
new_df

# %%
# new_df = new_df.loc[new_df['Email'] == 'ferry.yudhitama+112312test@karmagroup.com'].copy()
# new_df.reset_index(drop=True, inplace=True)

# new_df = new_df.iloc[0:1].copy()
# new_df.reset_index(drop=True, inplace=True)

# new_df

# %%
# cek push newsletter data
# new_df.to_excel(r"C:\Users\fajar\Documents\Python\Data\push_newsletter.xlsx", index=False)

# %%
# Cek leads test
test_leads = new_df.loc[
    
        new_df['Email'].str.contains('^test@', flags=re.I, regex=True) |
        new_df['Email'].str.contains('\+test', flags=re.I, regex=True) |
    
        new_df['First_Name'].str.contains('^test$', flags=re.I, regex=True) |
        new_df['Last_Name'].str.contains('^test$', flags=re.I, regex=True) |

        new_df['First_Name'].str.contains('test 1', flags=re.I, regex=True) |
        new_df['Last_Name'].str.contains('test 2', flags=re.I, regex=True) |
        new_df['First_Name'].str.contains('test1', flags=re.I, regex=True) |
        new_df['Last_Name'].str.contains('test2', flags=re.I, regex=True) |

        new_df['First_Name'].str.contains(' test ', flags=re.I, regex=True) | 
        new_df['Last_Name'].str.contains(' test ', flags=re.I, regex=True) | 
        new_df['Last_Name'].str.contains(' test$', flags=re.I, regex=True)
    ]

count_leads_test = test_leads.shape[0]

# test_leads.to_excel(r'C:\Users\fajar\Documents\Python\Data\test_leads_2.xlsx', index=False)
test_leads

# %%
new_df.drop(test_leads.index, inplace=True)
new_df.reset_index(drop=True, inplace=True)

count_after_dedup_test = new_df.shape[0]
count_after_dedup_test

# %%
count_final_data = new_df.shape[0]

# %%
# Define a dictionary containing ICC rankings
summary = {'Summary Description': ['Data Awal', 'Data Test', 'After Wash Test', '', 'Data Akhir'],
			'Count': [count_data_awal, count_leads_test, count_after_dedup_test,'', count_final_data]}

# Convert the dictionary into DataFrame
df_summary = pd.DataFrame(summary)
df_summary

# %%
row_data = new_df.shape[0]

if row_data > 0 :
    print('push data')
else :
    print('data empty')


# %%
# merubah listkey di area ini

# list key list test
list_key = campaign.get_list_key()
list_name = 'Newsletter'

# push data ke list zoho campaign
push_data = campaign.push_data(list_key[list_name], list_name, campaign_token, new_df)
push_data

# %%
today = datetime.now() 
date = today.strftime("%d-%m-%Y")

path = r'C:\Users\fajar\Documents\Python\Data\Zoho_Campaign\push data\api_log_history\newsletter\newsletter_log_history_'+str(date)+'.xlsx'

push_data.to_excel(path, sheet_name='Log History', index=False)
df_responses  = push_data.groupby(['Response Description'])['Email'].count().reset_index(name='Email Count').copy()

# %%
# jika ingin menambahkan sheets baru
with pd.ExcelWriter(path, mode="a", engine="openpyxl") as writer:
    df_summary.to_excel(writer, sheet_name="Summary Leads", index=False)
    df_responses.to_excel(writer, sheet_name="Summary Responses", index=False) 


