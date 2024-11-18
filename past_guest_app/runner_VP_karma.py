
import pandas as pd
import re
import numpy as np
from normalization import Norm_Email, Norm_Phone, Norm_Low, Norm_Title
from rule import check_OPTIN,check_OPTOUT,staffMail
from sqlite3 import Error
from pprint import pprint
from normalization import setDateTime

import json
from pandas import json_normalize

def getCSV(file):
    data = pd.read_csv(file, low_memory=False ,encoding='utf-8')
    df = pd.DataFrame(data)
    df = df.replace(np.nan, '', regex=True)
    return df

file_df_EP = r'C:\Users\fajar\Documents\Python\Data\Debounce\debounce_backup.csv'
df_EP =  getCSV(file_df_EP)
df_EP = df_EP[(~df_EP['EMAIL'].duplicated())]

def FindDep(email):   
    ff = df_EP.loc[df_EP['EMAIL'] == email]
    if ff.shape[0] > 0:
        # return '1'
        return ff.iloc[0]['RESULT']
    else:
        return ''
    # return  ff.shape[0]

def findOTA(email):
    email = Norm_Email(str(email))
    if email.__contains__('agoda') or email.__contains__('booking.com'):
        return ''
    elif email.__contains__('expedia') or email.__contains__('tour'):
        return ''
    elif email.__contains__('.null') or email.__contains__('karmagroup.com') or email.__contains__('@karma'):
        return ''
    elif email.__contains__('baligetaway') or email.__contains__('krresidences.com'):
        return ''
    else:
        return email

def process(result):
    try:
        id = result
        print(id)
    except Error as e: 
        print(e)

def BookingStatus(x):
    if str(x) == 'Cancelled':
        return str(x).upper()
    else:
        return x

def OdysseyMember(x):
    x = str(x).lower().strip()
    if x == 'yes':
        return True
    else:
        return False

def GuestType(x):
    if x == 'Cancelled':
        return x
    else:
        return 'Booking'

def getYOB(x):
    x = str(x)
    if x:
        return x[:4]

def normContactType(x):
    x = str(x).title().strip()
    return x

def copyMobile(x, y):
    if x: 
        return x
    elif x == '' and y: 
        return y

def checkStatus(member):
    if member:
        return 'BLOCK'
    else:
        return 'Pendding'

# CANCELLED
file = r'C:\Users\fajar\Documents\Python\Data\ZOHO - GL & VP - Guest Checked Out till 04-11-2024 - Viewpoint.csv'
df = getCSV(file)
df['Email'] = df['Email'].apply(findOTA)
df['Phone'] = df.apply(lambda x: Norm_Phone(x['Phone'],x['Country']),axis=1)
df['Mobile'] = df.apply(lambda x: Norm_Phone(x['Mobile'],x['Country']),axis=1)
df['Contact Type'] = df['Contact Type'].apply(normContactType)

df['Firstname'] = df['Firstname'].apply(Norm_Title)
df['Lastname'] = df['Lastname'].apply(Norm_Title)
df = df.drop(df[df['Contact Type'] == 'Blank'].index)

df_email = df[(
    df['Email'] != ''
)]

# df_email_unique = df_email[(~df_email['Email'].duplicated())]
df_email_unique = df_email[(~df_email.duplicated(subset=['Email','Lead Locations']))]

df_phone = df[(
    (df['Email'] == '') &
    (
        (df['Phone'] != '') |
        (df['Mobile'] != '') |
        (df['Phone'].str.len() <= 4 )
    )
)]

# df_phone_unique = df_phone[(~df_phone['Phone'].duplicated())]
df_phone_unique = df_phone[(~df_phone.duplicated(subset=['Phone','Lead Locations']))]

df_new = df_email_unique._append(df_phone_unique)
# Drop data with staff email
# df_new = df_new.drop(df_new[df_new["Email"].str.contains("@karmagroup.com")].index)
df_new = df_new.drop(df_new[df_new["Email"].str.contains('|'.join(staffMail()), flags=re.I)].index)

new_df = []

for index, row in df_new.iterrows():
    # addMapp = dict(
    #     # BookRef              = BookRef(row['Lead Locations'], row['BookingNo']),
    #     BookRef              = row['BookingNo'],
    #     Email_Opt_In         = check_OPTIN(row['Exclude From Mailing']),
    #     Email_Opt_Out        = check_OPTOUT(row['Exclude From Mailing']),
    #     Brand                = 'Karma Resorts',
    #     Lead_Sub_Brand       = 'Other', 
    #     Lead_Source          = 'Past Guests', 
    #     Lead_Source_Description = 'Viewpoint', 
    #     Lead_Locations       = row['Lead Locations'],
    #     Guest_Type           = GuestType('Checked-Out'),
    #     Booking_Status       = BookingStatus('Checked-Out'),
    #     Arrival_Date         = row['CheckInDate'],
    #     Departure_Date       = row['CheckOutDate'],
    #     Street               = row['AddressLine1'],
    #     Street2              = '',
    #     City                 = row['Town'],
    #     State                = row['State'],
    #     Country              = row['Country'],
    #     Nationality          = row['Nationality'],
    #     Zip_Code             = row['PostCode'],
    #     Phone                = copyMobile(row['Phone'], row['Mobile']),
    #     Mobile               = row['Mobile'],
    #     Email                = row['Email'],
    #     # Odyssey_Members      = False,
    #     Odyssey_Members      = OdysseyMember(row['Odyssey Members']),
    #     Salutation           = row['Title'],
    #     First_Name           = row['Firstname'],
    #     Last_Name            = row['Lastname'],
    #     Birthdate            = row['DOB'],
    #     Year_of_Birth        = getYOB(row['DOB']),
    #     Contact_type         = row['Contact Type'],
    #     Email_status         = FindDep(row['Email']), 
    #     IDzoho               = '',
    #     meta_id              = 186,
    #     zoho_check           = False,
    #     debounce_check       = False, 
    #     process_status       = checkStatus(OdysseyMember(row['Odyssey Members'])),
    #     process_date         = '',
    #     created              = setDateTime(),  
    # )

    # print(addMapp)
    # process(addMapp)

    new_df.append({
        'BookRef'              : row['BookingNo'],
        'Email_Opt_In'         : check_OPTIN(row['Exclude From Mailing']),
        'Email_Opt_Out'        : check_OPTOUT(row['Exclude From Mailing']),
        'Brand'                : 'Karma Resorts',
        'Lead_Sub_Brand'       : 'Other', 
        'Lead_Source'          : 'Past Guests', 
        'Lead_Source_Description' : 'Viewpoint', 
        'Lead_Locations'       : row['Lead Locations'],
        'Guest_Type'           : GuestType('Checked-Out'),
        'Booking_Status'       : BookingStatus('Checked-Out'),
        'Arrival_Date'         : row['CheckInDate'],
        'Departure_Date'       : row['CheckOutDate'],
        'Street'               : row['AddressLine1'],
        'Street2'              : '',
        'City'                 : row['Town'],
        'State'                : row['State'],
        'Country'              : row['Country'],
        'Nationality'          : row['Nationality'],
        'Zip_Code'             : row['PostCode'],
        'Phone'                : copyMobile(row['Phone'], row['Mobile']),
        'Mobile'               : row['Mobile'],
        'Email'                : row['Email'],
        # Odyssey_Members      : False,
        'Odyssey_Members'      : OdysseyMember(row['Odyssey Members']),
        'Salutation'           : row['Title'],
        'First_Name'           : row['Firstname'],
        'Last_Name'            : row['Lastname'],
        'Birthdate'            : row['DOB'],
        'Year_of_Birth'        : getYOB(row['DOB']),
        'Contact_type'         : row['Contact Type'],
        'Email_status'         : FindDep(row['Email']), 
        'IDzoho'               : '',
        'meta_id'              : 186,
        'zoho_check'           : False,
        'debounce_check'       : False, 
        'process_status'       : checkStatus(OdysseyMember(row['Odyssey Members'])),
        'process_date'         : '',
        'created'              : setDateTime()
    })


dict = json_normalize(new_df)
response_df = pd.DataFrame(dict)

# df_new.to_csv(r'C:\Users\fajar\Documents\Python\Data\before-vp-normalize.csv', index=False)
response_df.to_csv(r'C:\Users\fajar\Documents\Python\Data\normalize_viewpoint.csv', index=False)
    