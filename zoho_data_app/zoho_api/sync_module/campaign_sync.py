# %%
import pandas as pd
import numpy as np
from datetime import datetime
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
    'BookRef'
]

# %%
campaign_token = campaign.get_campaign_token()
crm_token = crm.get_crm_token()

# %%
df_dict = {
    'First_Name':['Fajar', 'Toni'], 
    'Last_Name':['Fatoni', 'Skyland'],
    'Email':['fajarfatonisocial@gmail.com', 'toniskyland21@gmail.com'],
    'Phone':['081237114798', '08132479914'],
    'Mobile':['081237114791', '08132479912'],
    'Lead_Locations':['Karma Bavaria', 'Karma Karnak'],
    'City':['Denpasar', 'Badung'],
    'Nationality':['Indonesia', 'Malaysia'],
    'Country':['Brazil', 'Argentina'],
    'Booking_Status':['Check-In', 'Check-Out'],
    'BookRef':['123456', '654321']
    }
new_df = pd.DataFrame.from_dict(df_dict)
new_df

# %%
new_df['First_Name'] = new_df['First_Name'].str.title()
new_df['Last_Name'] = new_df['Last_Name'].str.title()
new_df['Email'] = m.lowercase(new_df, 'Email')
m.clean_space(new_df, 'Email')

new_df

# %%
# new_df['Lead_Locations'] = new_df['Lead_Locations'].astype('string')
# new_df['Lead_Locations'].replace('\[|\]|\'','', regex=True, inplace=True)
# new_df

# new_df.replace('empty', '', inplace=True)

# test_df = new_df.loc[new_df['Email'] == 'guslin_love@yahoo.co.id'].copy()
# test_df['Lead_Locations'] = test_df['Lead_Locations'].astype('string')
# test_df['Lead_Locations'].replace('\[|\]|\'','', regex=True, inplace=True)
# test_df

# %%
# list key list test
list_key = campaign.get_list_key()
list_name = 'Test'

push_data = campaign.push_data(list_key['Test'], list_name, campaign_token, new_df)
push_data

# %%
today = datetime.today()

# dd/mm/YY
date = today.strftime("%d-%m-%Y")
print(date)

# %%
path = r'C:\Users\fajar\Documents\Python\Data\Zoho_Campaign\push data\api_log_history\test\test_'+str(date)+'.xlsx'
push_data.to_excel(path, sheet_name='Log History', index=False)

df_responses  = push_data.groupby(['Response Description'])['Email'].count().reset_index(name='Email Count').copy()

# jika ingin menambahkan sheets baru
with pd.ExcelWriter(path, mode="a", engine="openpyxl") as writer:
    df_responses.to_excel(writer, sheet_name="Summary Responses", index=False) 



