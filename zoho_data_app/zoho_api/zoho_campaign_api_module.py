import pandas as pd
import requests
import json
from pandas import json_normalize
from datetime import datetime

def get_campaign_token():

    url = 'https://accounts.zoho.com/oauth/v2/token?grant_type=refresh_token&refresh_token=1000.c7f853ebfd8beaf0e0833b019de25cf1.2feb766d6a43ad5b59c9850433687c6c&client_id=1000.8ZWIGIGFJGL2XE23M81L2FPLB7WQXC&client_secret=eb10f3fd944667ff8e4facb7b217f1531acd07b280'

    # post data menggunakan request
    response = requests.post(url)

    # konversi request.models.response to json
    json_data = json.loads(response.text)
    token = json_data['access_token']

    return token

def get_list_key():
    
    list_key_dict = {
         'Test' :'3zcd75f564cafbd4b5375ceb2783f45c26ed7d1a961ad057bc74f62c258ad0d97d',
         'Newsletter' :'3z117b3da1a6e11a3f64c81b21ca0031cb7487f2ce87540deba9887b92cb928901',
         'Karma Spa' :'3z41004d8703b56ddd271c2573d41242331444b8ba7769ceef4c9180ef12ac3cf5'
    }
    return list_key_dict

def get_data(token):
    # mencari tanggal hari ini
    today = '2022-11-21'

    limit = 1000
    index = str(0*limit)

    url_get_lead_contact = "https://campaigns.zoho.com/api/v1.1/getlistsubscribers?listkey=3zcd75f564cafbd4b5375ceb2783f45c26ed7d1a961ad057bc74f62c258ad0d97d&resfmt=JSON&sort=desc&fromindex="+index+"&range=1000"
    headers = {'Authorization': 'Zoho-oauthtoken '+token}

    content_res = requests.get(url_get_lead_contact, headers=headers).json()
    normalize = json_normalize(content_res['list_of_details'])
    df = pd.DataFrame(normalize)

    return df

def push_data(list_key, list_name, token, df):

    response_array = []
    pushcounter = 0 # menghitung jumlah data yang sudah dipush

    for index, row in df.iterrows():

        created_time = row['Created_Time']

        first_name = '"First Name" :'+'"'+row['First_Name']+'",'
        last_name = '"Last Name" :'+'"'+row['Last_Name']+'",'
        contact_email = '"Contact Email" :'+'"'+row['Email']+'",'
        phone = '"Phone" :'+'"'+row['Phone']+'",'
        mobile = '"Mobile" :'+'"'+row['Mobile']+'",'
        lead_locations = '"Lead Locations" :'+'"'+row['Lead_Locations']+'",'
        city = '"City" :'+'"'+row['City']+'",'
        nationality = '"Nationality" :'+'"'+row['Nationality']+'",'
        country = '"Country" :'+'"'+row['Country']+'",'
        booking_status = '"Booking Status" :'+'"'+row['Booking_Status']+'",'
        bookref = '"BookRef" :'+'"'+row['BookRef']+'"'

        contact_info = "contactinfo={"+first_name+last_name+contact_email+phone+mobile+lead_locations+city+nationality+country+booking_status+bookref+"}"

        url_get_lead_contact = "https://campaigns.zoho.com/api/v1.1/json/listsubscribe?resfmt=JSON&listkey="+list_key+"&"+contact_info

        # url_get_lead_contact = "https://campaigns.zoho.com/api/v1.1/json/listsubscribe?resfmt=JSON&listkey="+list_key+"&contactinfo={First Name:Fajar,Last Name:Fatoni,Contact Email:fajarfatonisocial@gmail.com, Lead Locations: Karma Bavaria}"
        
        # batas jumlah push untuk mentriger fungsi refresh token
        if (pushcounter == 100):
            token = get_campaign_token()
            pushcounter = 0 # reset jumlah data yang dipush ketika sudah mencapai batas yang ditentukan

        pushcounter += 1

        headers = {'Authorization': 'Zoho-oauthtoken '+token}
        content_res = requests.post(url_get_lead_contact, headers=headers).json()

        if 'User successfully subscribed' in content_res['message']:
            response_desc = 'New Contact Added'

        elif 'This email address already exists' in content_res['message']:
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
                    'Messages' : content_res['message'],
                    'Status' : content_res['status'],
                    'Response Description' : response_desc,
                    'Token Campaign API' : token
                })

    dict = json_normalize(response_array)
    response_df = pd.DataFrame(dict)
    
    return response_df
    # return url_get_lead_contact
