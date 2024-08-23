import pandas as pd

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
            globals()['df%s' % count].columns = globals()['df%s' % count].columns.str.title()
            globals()['df%s' % count]['Event Name'] = ''
            globals()['df%s' % count]['Event Name'] = sheet_name

             # memasukan semua file
            frames.append(globals()['df%s' % count])

            print(f"Sheet {sheet_name} has {sheet.row_count} rows and {sheet.col_count} columns")
            # frames.extend([globals()['df%s' % count]])

    result = pd.concat(frames, ignore_index=True)

    return result