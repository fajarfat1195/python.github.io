import pandas as pd
import re

def compile(spreadsheet, sheet_names, execeptional_list):

    count = 0
    frames = []

    for sheet_name in sheet_names:
        if sheet_name not in execeptional_list:
            sheet = spreadsheet.worksheet(sheet_name)

            count += 1
            # print(f"Sheet {sheet_name} has {sheet.row_count} rows and {sheet.col_count} columns")

            globals()['worksheet%s' % count] = spreadsheet.worksheet(sheet_name)
            globals()['rows%s' % count] = globals()['worksheet%s' % count].get_all_records()

            globals()['df%s' % count] = pd.DataFrame(globals()['rows%s' % count])
            globals()['df%s' % count].columns = globals()['df%s' % count].columns.str.title() # change column into proper case
            globals()['df%s' % count]['Event Name'] = ''
            globals()['df%s' % count]['Event Name'] = sheet_name

            # get summary detail event sheets
            globals()['df%s' % count]['Event Link'] = ''
            globals()['event_link%s' % count] = globals()['df%s' % count]['Servicing Office'].loc[globals()['df%s' % count]['Servicing Office'].str.contains('http')].to_list()
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

             # memasukan semua file
            frames.append(globals()['df%s' % count])

            print(f"Sheet {sheet_name} has {sheet.row_count} rows and {sheet.col_count} columns")
            # frames.extend([globals()['df%s' % count]])

    result = pd.concat(frames, ignore_index=True)

    return result