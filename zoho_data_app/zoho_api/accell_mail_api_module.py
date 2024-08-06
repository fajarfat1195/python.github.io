import pandas as pd
import requests
import json
from pandas import json_normalize
from datetime import datetime


def get_list_key():
    
    list_key_dict = {
         'Test' :'66b09736acc16',
         'Newsletter' :'66b07f7a36d87'
    }
    return list_key_dict


def get_campaign_token():

    url = 'https://accounts.zoho.com/oauth/v2/token?grant_type=refresh_token&refresh_token=1000.c7f853ebfd8beaf0e0833b019de25cf1.2feb766d6a43ad5b59c9850433687c6c&client_id=1000.8ZWIGIGFJGL2XE23M81L2FPLB7WQXC&client_secret=eb10f3fd944667ff8e4facb7b217f1531acd07b280'

    # post data menggunakan request
    response = requests.post(url)

    # konversi request.models.response to json
    json_data = json.loads(response.text)
    token = json_data['access_token']

    return token

def push_data(list_key, list_name, df):

    token = '3HgP0r8Q9N5g27bvhSa70nP0xkGSirTno9tnerl1CukoNgoPubzB0RXfe3pC'
    response_array = []
    pushcounter = 0 # menghitung jumlah data yang sudah dipush

    for index, row in df.iterrows():

        created_time = row['Created_Time']

        contact_email = 'EMAIL='+row['Email']+'&'
        first_name = 'FIRST_NAME='+row['First_Name']+'&'
        last_name = 'LAST_NAME='+row['Last_Name']+'&'
        status = 'status=subscribed'

        contact_info = contact_email+first_name+last_name+status

        url_push_lead_contact = "https://acelle.experiencekarmaclub.com/api/v1/subscribers?api_token="+token+"&list_uid="+list_key+"&"+contact_info

        # url_get_lead_contact = "https://campaigns.zoho.com/api/v1.1/json/listsubscribe?resfmt=JSON&listkey="+list_key+"&contactinfo={First Name:Fajar,Last Name:Fatoni,Contact Email:fajarfatonisocial@gmail.com, Lead Locations: Karma Bavaria}"
        

        content_res = requests.post(url_push_lead_contact).json()

        message = content_res.get('message')
        email = content_res.get('EMAIL')

        # jika json responses memiliki field 'message'
        if message:
            if 'Subscriber was successfully created' in message:
                response_desc = 'New Contact Added'
            else:
                response_desc = 'Ignored Index/Contact'
        else:
            # jika json responses memiliki field 'email'
            if email:
                response_desc = 'Contact Already Exists'
            else:
                response_desc = 'Ignored Index/Contact'

        now = datetime.now()
        datetime_push = now.strftime("%d-%m-%Y %H:%M:%S")

        response_array.append({
                    'Push Datetime' : datetime_push,
                    'List Name': list_name,
                    'Email Created Time': created_time,
                    'Email' : row['Email'],
                    'Response Description' : response_desc,
                    'Token Campaign API' : token
                })

    dict = json_normalize(response_array)
    response_df = pd.DataFrame(dict)
    
    return response_df
    # return url_get_lead_contact
