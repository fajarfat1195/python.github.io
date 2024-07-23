import pandas as pd
import numpy as np
import json
from pandas import json_normalize
from setup_api import setup
from mailwizz.endpoint.list_subscribers import ListSubscribers

"""
SETUP THE API
"""
setup()

endpoint = ListSubscribers()

def load_lists_id():
    list = {}

    # daftar list beserta list_id
    list['Test'] = 'af276ooltdfc8'

    return list

def load_subs(list_id):

    array_df = []

    for x in range(80000):
        i = x+1
        response = endpoint.get_subscribers(list_uid=list_id, page=i, per_page=100)
        dict = json.loads(response.content)
        df = json_normalize(dict['data']['records']) 
        new_df = pd.DataFrame(df)
        count_data_subs = new_df.shape[0]

        # jika jumlah data yang diloop masih ada atau lebih dari 0
        # memasukan df kedalam array_df
        if (count_data_subs > 0):
            array_df.append(new_df)

        # jika jumlah data sudah habis atau 0 maka akan menghentikan loop
        else:
            break
        
    concat_df = pd.concat(array_df, ignore_index=True)
    return concat_df
    
def reindex_cols(df, cols):
    df = df.reindex(columns=cols)

    return df

def insert_data_subs(list_id, df): # single row subs
    np_array = df.to_numpy() # convert dataframe to array json
    response_array = []
    for x in np_array:
        response = endpoint.create(list_uid=list_id, data=
            {
            'CREATEDTIME' : x[1], 
            'CREATEDDATE': x[2], 
            'FNAME': x[3], 
            'LNAME': x[4],
            'EMAIL': x[5], 
            'PHONE': x[6], 
            'MOBILE': x[7], 
            'BIRTHDATE': x[8], 
            'BIRTHYEAR': x[9], 
            'STREET': x[10],
            'STREET2': x[11], 
            'CITY': x[12], 
            'STATE': x[13], 
            'COUNTRY': x[14], 
            'DEPDATE': x[15], 
            'ARRDATE': x[16], 
            'CARDTYPE': x[17],
            'MARSTATUS': x[18], 
            'LABELBRAND': x[19], 
            'LEADSUBBRAND': x[20], 
            'LEADSOURCE': x[21],
            'LEADLOCATIONS': x[22], 
            'LEADSOURCEDESC': x[23], 
            'LEADREGIONS': x[24], 
            'LEADSTATUS': x[25],
            'EMAILOPTOUT': x[26], 
            'OPTIN': x[27]
            },
        )

        
        # aktifkan code ini jika ingin mengetahui errornya kenapa
        data  = json.loads(response.content)
        if (data['status'] == 'error'):
            response_array.append({
                'Email' : x[5],
                'Status' : 'Error',
                'Messages' : data['error'],
                'Subs ID' : ''
            }
            )
        else:
            response_array.append({
                'Email' : x[5],
                'Status' : 'Success',
                'Messages' : 'Input email success',
                'Subs ID' : data['data']['record']['subscriber_uid']
            }
            )

        # print(response.content)
        
    dict = json_normalize(response_array)
    response_df = pd.DataFrame(dict)
    
    return response_df
       

def convert_array_to_json(df):

    np_array = df.to_numpy() # convert dataframe to array json
    json_array = []
    for x in np_array:
        json_array.append({
            'CREATEDTIME' : x[1], 
            'CREATEDDATE': x[2], 
            'FNAME': x[3], 
            'LNAME': x[4],
            'EMAIL': x[5], 
            'PHONE': x[6], 
            'MOBILE': x[7], 
            'BIRTHDATE': x[8], 
            'BIRTHYEAR': x[9], 
            'STREET': x[10],
            'STREET2': x[11], 
            'CITY': x[12], 
            'STATE': x[13], 
            'COUNTRY': x[14], 
            'DEPDATE': x[15], 
            'ARRDATE': x[16], 
            'CARDTYPE': x[17],
            'MARSTATUS': x[18], 
            'LABELBRAND': x[19], 
            'LEADSUBBRAND': x[20], 
            'LEADSOURCE': x[21],
            'LEADLOCATIONS': x[22], 
            'LEADSOURCEDESC': x[23], 
            'LEADREGIONS': x[24], 
            'LEADSTATUS': x[25],
            'EMAILOPTOUT': x[26], 
            'OPTIN': x[27]
            })
    return json_array

def check_email_exist(list_id, df):
    np_array = df.to_numpy() # convert dataframe to array json
    for x in np_array:
        response = endpoint.email_search(list_uid=list_id, email_address=x[5])
        json_response = json.loads(response.content)
        
        if (json_response['status'] == 'success'):
            print(x[5]+' '+'exist'+' '+json_response['data']['subscriber_uid'])
        

def bulk_insert_data_subs(list_id, insert_data_json): # multiple row subs
    response = endpoint.create_bulk(list_uid=list_id, data=insert_data_json)
    #return 'success insert'
    return response.content

def update_data_subs(list_id, df):

    np_array = df.to_numpy() # convert dataframe to array json
    for x in np_array:

        subs_id = x[0]
        response = endpoint.update(list_uid=list_id, subscriber_uid=subs_id, data={
            'CREATEDTIME' : x[1], 
            'CREATEDDATE': x[2], 
            'FNAME': x[3], 
            'LNAME': x[4],
            'EMAIL': x[5], 
            'PHONE': x[6], 
            'MOBILE': x[7], 
            'BIRTHDATE': x[8], 
            'BIRTHYEAR': x[9], 
            'STREET': x[10],
            'STREET2': x[11], 
            'CITY': x[12], 
            'STATE': x[13], 
            'COUNTRY': x[14], 
            'DEPDATE': x[15], 
            'ARRDATE': x[16], 
            'CARDTYPE': x[17],
            'MARSTATUS': x[18], 
            'LABELBRAND': x[19], 
            'LEADSUBBRAND': x[20], 
            'LEADSOURCE': x[21],
            'LEADLOCATIONS': x[22], 
            'LEADSOURCEDESC': x[23], 
            'LEADREGIONS': x[24], 
            'LEADSTATUS': x[25],
            'EMAILOPTOUT': x[26], 
            'OPTIN': x[27]
        })
    
    return 'success update'
    #return response.content

def delete_data_subs_id(list_id, df):
    np_array = df.to_numpy() # convert dataframe to array json
    for x in np_array:

        subs_id = x[0]

        response = endpoint.delete(list_uid=list_id, subscriber_uid=subs_id)
        
    return 'success delete'
    #return response.content

def delete_data_subs_email(list_id, df):
    np_array = df.to_numpy() # convert dataframe to array json
    for x in np_array:

        email = x[1]

        response = endpoint.delete_by_email(list_uid=list_id, email_address=email)
    
    return 'success delete'
    #return response.content

def delete_maillwizz_not_exist_zoho(list, df_maillwizz, col_maillwizz, df_zoho, col_zoho):
    
    # email mailwizz yang tidak ada di zoho akan di take out (karena ada kemungkinan sudah menjadi member, atau tidak masuk ke dalam kriteria filtrasi - take out subs)
    result_df = df_maillwizz.loc[~df_maillwizz[col_maillwizz].isin(df_zoho[col_zoho])].copy()
    delete_data_subs_id(list, result_df)

    return result_df

def input_new_subs_from_zoho(list, df_zoho, col_zoho, df_maillwizz, col_mailwizz):

    # check email zoho yang tidak ada di maillwizz akan dimasukan sebagai subs baru (new subs)
    result_df = df_zoho.loc[~df_zoho[col_zoho].isin(df_maillwizz[col_mailwizz])].copy()

    result = insert_data_subs(list, result_df)

    return result

def sync_maillwizz_zoho_field(df_maillwizz, col_mailwizz, df_zoho, col_zoho):

    sync_maillwizz_field = pd.merge(df_maillwizz,
                        df_zoho,
                        left_on = col_mailwizz,
                        right_on = col_zoho,
                        how ='inner')

    return sync_maillwizz_field
