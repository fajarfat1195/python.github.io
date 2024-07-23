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
    list['Tiket Konser'] = 'nv298m58xx08b'

    return list

def load_subs(list_id):
    response = endpoint.get_subscribers(list_uid=list_id, page=1, per_page=10)
    dict = json.loads(response.content)
    df = json_normalize(dict['data']['records']) 
    return df

def reindex_cols(df, cols):
    df = df.reindex(columns=cols)

    return df

def insert_data_subs(list_id): # single row subs

    response = endpoint.create(list_uid=list_id, data=[
            {
            'EMAIL': 'john.doe1@example.com',  # the confirmation email will be sent!!! Use valid email address
            'FNAME': 'John1',
            'LNAME': 'Doe1',
            'ALAMAT': 'Sydnei',
            'STATUS': 'Single'
            },
        ])
    
    return response

def convert_array_to_json(df):

    np_array = df.to_numpy() # convert dataframe to array json
    json_array = []
    for x in np_array:
        json_array.append({'EMAIL': x[0], 'FNAME': x[1], 'LNAME': x[2], 'ALAMAT': x[3], 'STATUS': x[4]})
    return json_array

def bulk_insert_data_subs(list_id, insert_data_json): # multiple row subs
    response = endpoint.create_bulk(list_uid=list_id, data=insert_data_json)
    return 'success insert'
    #return response.content

def update_data_subs(list_id, df):

    np_array = df.to_numpy() # convert dataframe to array json
    for x in np_array:

        subs_id = x[0]
        email = x[1]
        first_name = x[2]
        last_name = x[3]
        alamat = x[4]
        status = x[5]

        response = endpoint.update(list_uid=list_id, subscriber_uid=subs_id, data={
        'EMAIL':email,
        'FNAME':first_name,	
        'LNAME':last_name,	
        'ALAMAT':alamat,	
        'STATUS':status
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

def delete_maillwizz_not_exist_zoho(df_maillwizz, col_maillwizz, df_zoho, col_zoho):
    
    # email mailwizz yang tidak ada di zoho akan di take out (karena ada kemungkinan sudah menjadi member, atau tidak masuk ke dalam kriteria filtrasi - take out subs)
    result_df = df_maillwizz.loc[~df_maillwizz[col_maillwizz].isin(df_zoho[col_zoho])].copy()

    list = load_lists_id()
    delete_data_subs_id(list['Tiket Konser'], result_df)

    return result_df

def input_new_subs_from_zoho(df_zoho, col_zoho, df_maillwizz, col_mailwizz):

    # email zoho yang tidak ada di maillwizz akan dimasukan sebagai subs baru (new subs)
    result_df = df_zoho.loc[~df_zoho[col_zoho].isin(df_maillwizz[col_mailwizz])].copy()

    list = load_lists_id()

    # convert to json
    new_df_json = convert_array_to_json(result_df)

    bulk_insert_data_subs(list['Tiket Konser'], new_df_json)

    return result_df

def sync_maillwizz_zoho_field(df_zoho, col_zoho, df_maillwizz, col_mailwizz):

    sync_maillwizz_field = pd.merge(df_maillwizz,
                        df_zoho,
                        left_on = col_mailwizz,
                        right_on = col_zoho,
                        how ='left')

    return sync_maillwizz_field
