import pandas as pd
import re
import random
import time

def compile(spreadsheet, sheet_names_id, sheet_names, execeptional_list):

    count = 0
    frames = []

    while count < len(sheet_names):
        try:
            if sheet_names[count] not in execeptional_list:
                sheet = spreadsheet.worksheet(sheet_names[count])
                # print(f"Sheet {sheet_name} has {sheet.row_count} rows and {sheet.col_count} columns")

                globals()['worksheet%s' % count] = spreadsheet.worksheet(sheet_names[count])
                globals()['rows%s' % count] = globals()['worksheet%s' % count].get_all_records()

                globals()['df%s' % count] = pd.DataFrame(globals()['rows%s' % count])
                globals()['df%s' % count].columns = globals()['df%s' % count].columns.str.title() # change column into proper case
                
                globals()['df%s' % count]['Event Name'] = ''
                globals()['df%s' % count]['Event Name'] = sheet_names[count]

                globals()['df%s' % count]['Event Sheet Link'] = ''
                globals()['df%s' % count]['Event Sheet Link'] = f"https://docs.google.com/spreadsheets/d/{spreadsheet.id}/edit#gid={sheet_names_id[count]}"

                # get summary detail event sheets
                globals()['df%s' % count]['Event Link'] = ''
                globals()['event_link%s' % count] = globals()['df%s' % count]['Servicing Office'].loc[globals()['df%s' % count]['Servicing Office'].str.contains('http', na=False)].to_list()
                if  globals()['event_link%s' % count]: # if value exist on summary detail
                    globals()['df%s' % count]['Event Link'] = globals()['event_link%s' % count][0]
                    globals()['df%s' % count]['Event Link'] = globals()['df%s' % count]['Event Link'].str.replace('event info - ', '', regex=True, flags=re.I)    
                else:
                    globals()['df%s' % count]['Event Link'] = ''
                
                globals()['df%s' % count]['Available Spots'] = ''
                globals()['available_spots%s' % count] = globals()['df%s' % count]['Membership Type'].loc[globals()['df%s' % count]['Servicing Office'] == 'Available Spots'].to_list()
                if  globals()['available_spots%s' % count]: # if value exist on summary detail
                    globals()['df%s' % count]['Available Spots'] = globals()['available_spots%s' % count][0]
                else:
                    globals()['df%s' % count]['Available Spots'] = ''

                globals()['df%s' % count]['Quota Event'] = ''
                globals()['quota_event%s' % count] = globals()['df%s' % count]['Membership Type'].loc[globals()['df%s' % count]['Servicing Office'] == 'Quota Event'].to_list()
                if  globals()['quota_event%s' % count]:
                    globals()['df%s' % count]['Quota Event'] = globals()['quota_event%s' % count][0]
                else:
                    globals()['df%s' % count]['Quota Event'] = ''

                globals()['df%s' % count].fillna('', inplace=True)
                # memasukan semua file
                frames.append(globals()['df%s' % count])

                print(f"Sheet {sheet_names[count]} has {sheet.row_count} rows and {sheet.col_count} columns")
                # frames.extend([globals()['df%s' % count]])
            count += 1
        except Exception as e:
            print(f"Error: {e}")
            print(f"limit exceeded, delay for one minute:")
            time.sleep(65)
            count = count
            continue  # retry the API call
            # if e.code == 429:  # Quota exceeded error
            #     print(f"Quota exceeded! Retrying in {2**count} seconds...")
            #     time.sleep(2**count + random.uniform(0, 1))  # exponential backoff with jitter
            #     count += 1
            #     continue  # retry the API call
            # else:
            #     print(f"Error: {e}")
            #     # handle other API errors
    result = pd.concat(frames, ignore_index=True)

    return result
