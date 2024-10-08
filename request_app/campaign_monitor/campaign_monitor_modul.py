import requests
from requests.auth import HTTPBasicAuth
import pandas as pd

# Replace with your actual API key and client ID
# api_key = 'W7KbXzk9fFsN+G3XrIemdIu156KSPq3Qh60OQFQw9oP0UPnDvfq8w2SH5plgeZnpzyA4Bc2QCKVpK9SB42n8ZO3Z4Cpefu2/HGULJneNoJZ2zza129wfcsOL35Fpoweq3ZcidTNu110I/HCNguRGUw=='
# client_id = '1545f43bbfe89f34ea7cf143c36c5e9f'

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

    result = df.loc[df['Name'].str.contains(search_value)].copy()
    return result

def get_openers_list(api_key, campaign_id, page=None):

    if page is not None:
        url = f'https://api.createsend.com/api/v3.2/campaigns/{campaign_id}/opens.json?page={page}'
    else:
        url = f'https://api.createsend.com/api/v3.2/campaigns/{campaign_id}/opens.json'
    
    # Make the GET request
    response = requests.get(url, auth=HTTPBasicAuth(api_key, ''))

    # Check for successful response
    if response.status_code == 200:
        opens_data = response.json()
        # Extract the 'Results' part of the JSON response
        openers_list = opens_data.get('Results', [])
        numbers_of_page = opens_data.get("NumberOfPages", [])
        # Create a DataFrame from the list of openers
        df = pd.DataFrame(openers_list)
        # print(f"Load data success")
        # if numbers_of_page > 1:
        #     print("Page lebih dari 1")
    else:
        print(f"Failed to retrieve openers. Status Code: {response.status_code}, Response: {response.text}")

    result = {'data': df, 'page_total':numbers_of_page}
    return result