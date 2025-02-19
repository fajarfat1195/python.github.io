import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError
import pandas as pd
import time
import ast
import requests

# Replace with your actual API key
# api_key = 'b055f3c445761f9b379cb7c932ceaec3-us17'
# server = 'us17'

# Function to check for value in column
def search_value_list_dic(column, key, value):
    if isinstance(column, list):
        # print(f"list value")
        return any(value in act.get(key, value) for act in column if isinstance(act, dict))
    elif isinstance(column, dict):
        # print(f"dict value")
        return value in column.get(key, value)
    return False  # Return False for unsupported types (e.g., None)

# get data campaign list
def get_campaign_list(api_key, server, search_value):


    try:
        client = MailchimpMarketing.Client()
        client.set_config({
            "api_key": api_key,
            "server": server
        })

        # Initialize variables for pagination
        all_campaigns = []
        count = 10  # Number of campaigns to fetch per request
        offset = 0  # Starting point for pagination

        while True:
            # Fetch campaigns with pagination parameters
            response = client.campaigns.list(count=count, offset=offset)

            # Check if there are campaigns returned
            if not response['campaigns']:
                break  # Exit loop if no more campaigns are returned

            # Append the campaigns to the list
            all_campaigns.extend(response['campaigns'])

            # Update the offset for the next request
            offset += count

        # Convert the list of campaigns to a DataFrame
        df_campaigns = pd.DataFrame(all_campaigns)

        # Display the DataFrame
        print(df_campaigns)

    except ApiClientError as error:
        print("Error: {}".format(error.text))

    # result = df_campaigns[df_campaigns.apply(lambda x: search_value_list_dic(x['settings'], 'title', search_value),
    #     axis=1)]
    
    return df_campaigns

# retrieve data endpoint from campaign
def get_data_list(api_key, server, campaign_id):

    retry_error_keywords = [
        "Read timed out",
        "ConnectionError",
        "Connection aborted."
    ]

    # Initialize the Mailchimp client
    client = MailchimpMarketing.Client()
    client.set_config({
        "api_key": api_key,
        "server": server
    })
    # Initialize variables for pagination
    all_emails = []
    count = 10  # Number of campaigns to fetch per request
    offset = 0  # Starting point for pagination
    max_retries = 5  # Maximum number of retries

    for attempt in range(max_retries):
        try:
            while True:
                # Fetch email activity for the specified campaign ID
                response = client.reports.get_email_activity_for_campaign(campaign_id, count=count, offset=offset)

                # Check if there are emails returned
                if not response['emails']:
                    break  # Exit loop if no more emails are returned

                # Append the emails to the list
                all_emails.extend(response['emails'])

                # Update the offset for the next request
                offset += count

            # Convert the list of emails to a DataFrame
            if all_emails:  # Check if all_emails is not empty
                globals()['df_emails_%s' % campaign_id] = pd.DataFrame(all_emails)
            else:
                globals()['df_emails_%s' % campaign_id] = pd.DataFrame()  # Initialize as empty DataFrame if no emails were found

            # # Print the DataFrame
            # print(globals()['df_emails_%s' % campaign_id])

            break  # Exit the retry loop if successful

        except ApiClientError as error:
            print("Error: {}".format(error.text))
            # Check if any of the keywords are in the error text
            if any(keyword in str(error.text) for keyword in retry_error_keywords):
                print("A retryable error occurred. Retrying in 1 minute...")
                print("Error condition 1")
                time.sleep(60)  # Pause for one minute before retrying
                continue
            else:
                print("Error condition 2")
                break  # Exit if it's a different error

        # except requests.exceptions.ReadTimeout as e:
        #     print("Read timeout occurred: {}".format(e))
        #     print("Retrying in 1 minute...")
        #     time.sleep(60)  # Pause for one minute before retrying
        #     continue  # Retry the operation

        # except requests.exceptions.ConnectionError as e:
        #     print("Connection error occurred: {}".format(e))
        #     print("Retrying in 1 minute...")
        #     time.sleep(60)  # Pause for one minute before retrying
        #     continue  # Retry the operation

        # except requests.exceptions.RemoteDisconnected as e:
        #     print("Remote disconnected error occurred: {}".format(e))
        #     print("Retrying in 1 minute...")
        #     time.sleep(60)  # Pause for one minute before retrying
        #     continue  # Retry the operation

        # except Exception as e:
        #     print("An unexpected error occurred: {}".format(e))
        #     break  # Exit on unexpected errors

    return globals()['df_emails_%s' % campaign_id]