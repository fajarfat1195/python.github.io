import requests
from requests.auth import HTTPBasicAuth
import pandas as pd

# Replace with your actual API key and client ID
# api_key = 'W7KbXzk9fFsN+G3XrIemdIu156KSPq3Qh60OQFQw9oP0UPnDvfq8w2SH5plgeZnpzyA4Bc2QCKVpK9SB42n8ZO3Z4Cpefu2/HGULJneNoJZ2zza129wfcsOL35Fpoweq3ZcidTNu110I/HCNguRGUw=='
# client_id = '1545f43bbfe89f34ea7cf143c36c5e9f'

# get data campaign list
def get_campaign_list(api_key, client_id, search_value):

    # API endpoint
    url = f'https://api.createsend.com/api/v3.2/clients/{client_id}/campaigns.json'

    # Make the GET request
    response = requests.get(url, auth=HTTPBasicAuth(api_key, ''))

    # Check for successful response
    if response.status_code == 200:
        campaigns = response.json()
        print("Campaigns List:")
        # Create a DataFrame from the campaigns data
        df = pd.DataFrame(campaigns, columns=['Name','SentDate','TotalRecipients','CampaignID','Subject'])
        # Display the DataFrame
    else:
        print(f"Failed to retrieve campaigns. Status Code: {response.status_code}, Response: {response.text}")

    result = df.loc[df['Name'].str.contains(search_value, regex=True)].copy()
    result.reset_index(drop=True, inplace=True)
    return result

# retrieve data endpoint from campaign
def get_data_list(api_key, campaign_id, endpoint, page=None):

    if page is not None:
        url = f'https://api.createsend.com/api/v3.2/campaigns/{campaign_id}/{endpoint}.json?page={page}'
    else:
        url = f'https://api.createsend.com/api/v3.2/campaigns/{campaign_id}/{endpoint}.json'
    
    # Make the GET request
    response = requests.get(url, auth=HTTPBasicAuth(api_key, ''))

    # Check for successful response
    if response.status_code == 200:
        response_data = response.json()
        # Extract the 'Results' part of the JSON response
        data_list = response_data.get('Results', [])
        numbers_of_page = response_data.get("NumberOfPages", [])
        # Create a DataFrame from the list of data
        df = pd.DataFrame(data_list)
        # print(f"Load data success")
        # if numbers_of_page > 1:
        #     print("Page lebih dari 1")
    else:
        print(f"Failed to retrieve data. Status Code: {response.status_code}, Response: {response.text}")

    result = {'data': df, 'page_total':numbers_of_page}
    return result

# retrieve data per campaign list using loop and get the data based on endpoint
def loop_data_list_page(api_key, campaign_id, endpoint, page_total):
    count = 1
    frames = []

    while count <= page_total: #tidak menggunakan len karena page total berupa
        globals()['get_data_list%s' % count] = get_data_list(api_key, campaign_id, endpoint, count)
        globals()['df%s' % count] = pd.DataFrame(globals()['get_data_list%s' % count]['data'])
        
        # memasukan semua file
        frames.append(globals()['df%s' % count])
        count += 1

    df_data = pd.concat(frames, ignore_index=True)
    if 'Date' in df_data.columns:
        df_data.sort_values(['EmailAddress','Date'], ascending=[True, False], inplace=True)
    else:
        df_data.sort_values(['EmailAddress'], ascending=[True], inplace=True)
    df_data.drop_duplicates(subset=['EmailAddress'], inplace=True)

    return df_data
