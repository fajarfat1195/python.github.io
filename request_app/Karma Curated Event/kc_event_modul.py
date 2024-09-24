import pandas as pd
import re
import random
import time
import gspread
from gspread.exceptions import APIError, SpreadsheetNotFound, WorksheetNotFound

def compile(spreadsheet, sheet_names_id, sheet_names, execeptional_list):

    count = 0
    frames = []

    while count < len(sheet_names):
        try:
            if sheet_names[count] not in execeptional_list:
                if not pd.Series([sheet_names[count]]).str.contains('sheet', flags=re.I).any():
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

                    # get the non-empty values from the 'Event Date From' column
                    non_empty_date_from = globals()['df%s' % count]['Event Date From'][globals()['df%s' % count]['Event Date From'] != '']
                    non_empty_date_to = globals()['df%s' % count]['Event Date To'][globals()['df%s' % count]['Event Date To'] != '']
                    non_empty_event_status = globals()['df%s' % count]['Event Status'][globals()['df%s' % count]['Event Status'] != '']
                    non_empty_event_location = globals()['df%s' % count]['Event Location'][globals()['df%s' % count]['Event Location'] != '']
                    non_empty_event_region = globals()['df%s' % count]['Event Region'][globals()['df%s' % count]['Event Region'] != '']
                    non_empty_event_type = globals()['df%s' % count]['Event Type'][globals()['df%s' % count]['Event Type'] != '']

                    # fill empty values in 'Event Date From' with the first non-empty value
                    # if non_empty variable not N/A or data row column is not fully empty on sheets
                    if not non_empty_date_from.empty:
                        globals()['df%s' % count].loc[globals()['df%s' % count]['Event Date From'] == '', 'Event Date From'] = non_empty_date_from.iloc[0]
                    if not non_empty_date_to.empty:
                        globals()['df%s' % count].loc[globals()['df%s' % count]['Event Date To'] == '', 'Event Date To'] = non_empty_date_to.iloc[0]
                    if not non_empty_event_status.empty:
                        globals()['df%s' % count].loc[globals()['df%s' % count]['Event Status'] == '', 'Event Status'] = non_empty_event_status.iloc[0]
                    if not non_empty_event_location.empty:
                        globals()['df%s' % count].loc[globals()['df%s' % count]['Event Location'] == '', 'Event Location'] = non_empty_event_location.iloc[0]
                    if not non_empty_event_region.empty:
                        globals()['df%s' % count].loc[globals()['df%s' % count]['Event Region'] == '', 'Event Region'] = non_empty_event_region.iloc[0]
                    if not non_empty_event_type.empty:
                        globals()['df%s' % count].loc[globals()['df%s' % count]['Event Type'] == '', 'Event Type'] = non_empty_event_type.iloc[0]

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

                    # delete empty no row value (tidak ada )
                    globals()['df%s' % count].drop(globals()['df%s' % count].loc[globals()['df%s' % count]['No'] == ''].index, inplace=True)
                    globals()['df%s' % count].reset_index(drop=True, inplace=True)

                    # memasukan semua file
                    frames.append(globals()['df%s' % count])

                    print(f"Sheet {sheet_names[count]} has {sheet.row_count} rows and {sheet.col_count} columns")
                    # frames.extend([globals()['df%s' % count]])
            count += 1
        except Exception as e:
            print(f"Error: {e}")
            error_response = e.response.json()
            if error_response['error']['code'] == 429:
                print(f"limit exceeded, delay for one minute")
                time.sleep(65)
                count = count
                continue
            else:
                print(f"Error: {e}")
    result = pd.concat(frames, ignore_index=True)

    return result

def get_file_sheets(sheet_id, execeptional_list, gc):
    count = 0

    frames = []
    for i, value in sheet_id.items():
        count += 1
        print(f"compiling spreadsheets - {i}")
        spreadsheets = gc.open_by_key(value)
        sheet_names = [sheet.title for sheet in spreadsheets.worksheets()]
        sheet_names_id = [sheet.id for sheet in spreadsheets.worksheets()]

        globals()['df%s' % count] = compile(spreadsheets, sheet_names_id, sheet_names, execeptional_list)
        frames.append(globals()['df%s' % count])
        
    result = pd.concat(frames, ignore_index=True)

    return result