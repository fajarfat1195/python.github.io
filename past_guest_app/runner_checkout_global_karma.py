import pprint
import pandas as pd
import re
import numpy as np
from normalization import Norm_Email, Norm_Phone, Norm_Low, Norm_Title, setLang
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
    if str(x) == 'Checked-Out':
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
    if x == 'Checked-Out':
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


file = r'C:\Users\fajar\Documents\Python\Data\ZOHO - GL & VP - Guest Checked Out till 25-11-2024 - Checked-Out.csv'
df = getCSV(file)
df['EMail'] = df['EMail'].apply(findOTA)
df['TelNo'] = df.apply(lambda x: Norm_Phone(x['TelNo'],x['Country']),axis=1)
df['MobileNo'] = df.apply(lambda x: Norm_Phone(x['MobileNo'],x['Country']),axis=1)
df['Contact Type'] = df['Contact Type'].apply(normContactType)

df['PrimaryGuestForename'] = df['PrimaryGuestForename'].apply(Norm_Title)
df['PrimaryGuestSurname'] = df['PrimaryGuestSurname'].apply(Norm_Title)
df['Language'] = df['Language'].apply(Norm_Title)
df = df.drop(df[df['Contact Type'] == 'Blank'].index)

df_email = df[(
    df['EMail'] != ''
)]

# df_email_unique = df_email[(~df_email['EMail'].duplicated())]
df_email_unique = df_email[(~df_email.duplicated(subset=['EMail','Lead Location']))]

df_phone = df[(
    (df['EMail'] == '') &
    (
        (df['TelNo'] != '') |
        (df['MobileNo'] != '') |
        (df['TelNo'].str.len() <= 4 )
    )
)]

# df_phone_unique = df_phone[(~df_phone['TelNo'].duplicated())]
df_phone_unique = df_phone[(~df_phone.duplicated(subset=['TelNo','Lead Location']))]

df_new = df_email_unique._append(df_phone_unique)

# Drop data with staff email
# df_new = df_new.drop(df_new[df_new["EMail"].str.contains("@karmagroup.com")].index)
df_new = df_new.drop(df_new[df_new["EMail"].str.contains('|'.join(staffMail()), flags=re.I)].index)

# df_new.to_csv(f'./data/CLEAN - ZOHO - GL & VP - Guest Checked Out till 24-08-2022 - Checked-Out.csv')

new_df = []

for index, row in df_new.iterrows():
    # print(row['BookRef'], row['EMail'], row['TelNo'], row['Lead Location'])
    # addMapp = dict(
    #     BookRef              = row['BookRef'],
    #     Email_Opt_In         = check_OPTIN(row['ExcludeFromMailings']),
    #     Email_Opt_Out        = check_OPTOUT(row['ExcludeFromMailings']),
    #     Brand                = row['Lead Brand'],
    #     Lead_Sub_Brand       = row['Lead Sub-Brand'], 
    #     Lead_Source          = row['Lead Source'], 
    #     Lead_Locations       = row['Lead Location'],
    #     Guest_Type           = GuestType(row['BookingStatus']),
    #     Booking_Status       = BookingStatus(row['BookingStatus']),
    #     Arrival_Date         = row['DateArrive'],
    #     Departure_Date       = row['DateDepart'], 
    #     Street               = row['Street'],
    #     Street2              = '',  
    #     City                 = row['Town'],
    #     State                = row['Area'], 
    #     Country              = row['Country'],
    #     Nationality          = row['Nationality'],
    #     Zip_Code             = row['PostCode'],
    #     Phone                = copyMobile(row['TelNo'], row['MobileNo']),
    #     Mobile               = row['MobileNo'],
    #     Email                = row['EMail'],
    #     # Odyssey_Members      = False,
    #     Odyssey_Members      = OdysseyMember(row['Odyssey Members']),
    #     PrimaryGuestProfileRef = row['PrimaryGuestProfileRef'],
    #     Salutation           = row['PrimaryGuestTitle'],
    #     First_Name           = row['PrimaryGuestForename'],
    #     Last_Name            = row['PrimaryGuestSurname'],
    #     Birthdate            = row['DOB'],
    #     Year_of_Birth        = getYOB(row['DOB']),
    #     Gender               = row['Gender'],
    #     Media_Source_Code    = row['MediaSourceCode'], 
    #     Market_Segment       = row['MarketSegment'],
    #     Adult                = row['Adults'],
    #     Children             = row['Children'], 
    #     Infant               = row['Infants'],
    #     Contact_type         = row['Contact Type'],
    #     Language             = setLang(row['Nationality'], row['Language']),
    #     Email_status         = FindDep(row['EMail']), 
    #     IDzoho               = '',
    #     meta_id              = 185,
    #     zoho_check           = False,
    #     debounce_check       = False, 
    #     process_status       = checkStatus(OdysseyMember(row['Odyssey Members'])),
    #     process_date         = '',
    #     created              = setDateTime(),  
    # )

    # print(addMapp)
    # process(addMapp)

    new_df.append({
                    'BookRef '             : row['BookRef'],
                    'Email_Opt_In'         : check_OPTIN(row['ExcludeFromMailings']),
                    'Email_Opt_Out'        : check_OPTOUT(row['ExcludeFromMailings']),
                    'Brand '               : row['Lead Brand'],
                    'Lead_Sub_Brand'       : row['Lead Sub-Brand'], 
                    'Lead_Source'          : row['Lead Source'], 
                    'Lead_Locations'       : row['Lead Location'],
                    'Guest_Type'           : GuestType(row['BookingStatus']),
                    'Booking_Status'       : BookingStatus(row['BookingStatus']),
                    'Arrival_Date'         : row['DateArrive'],
                    'Departure_Date'       : row['DateDepart'], 
                    'Street'               : row['Street'],
                    'Street2'              : '',  
                    'City'                 : row['Town'],
                    'State'                : row['Area'], 
                    'Country'              : row['Country'],
                    'Nationality'          : row['Nationality'],
                    'Zip_Code'             : row['PostCode'],
                    'Phone'                : copyMobile(row['TelNo'], row['MobileNo']),
                    'Mobile'              : row['MobileNo'],
                    'Email'                : row['EMail'],
                    # Odyssey_Members      : False,
                    'Odyssey_Members'      : OdysseyMember(row['Odyssey Members']),
                    'PrimaryGuestProfileRef' : row['PrimaryGuestProfileRef'],
                    'Salutation'           : row['PrimaryGuestTitle'],
                    'First_Name'           : row['PrimaryGuestForename'],
                    'Last_Name'            : row['PrimaryGuestSurname'],
                    'Birthdate'            : row['DOB'],
                    'Year_of_Birth'        : getYOB(row['DOB']),
                    'Gender'               : row['Gender'],
                    'Media_Source_Code'    : row['MediaSourceCode'], 
                    'Market_Segment'       : row['MarketSegment'],
                    'Adult'                : row['Adults'],
                    'Children'             : row['Children'], 
                    'Infant'               : row['Infants'],
                    'Contact_type'         : row['Contact Type'],
                    'Language'             : setLang(row['Nationality'], row['Language']),
                    'Email_status'         : FindDep(row['EMail']), 
                    'IDzoho'               : '',
                    'meta_id '             : 185,
                    'zoho_check'           : False,
                    'debounce_check'       : False, 
                    'process_status'       : checkStatus(OdysseyMember(row['Odyssey Members'])),
                    'process_date'         : '',
                    'created'              : setDateTime(),  
                })


dict = json_normalize(new_df)
response_df = pd.DataFrame(dict)

# df_new.to_csv(r'C:\Users\fajar\Documents\Python\Data\before-normalize.csv', index=False)
response_df.to_csv(r'C:\Users\fajar\Documents\Python\Data\normalize_checkout.csv', index=False)


    