import pandas as pd
import re
import numpy as np
from fractions import Fraction

def load_data_multiple(dir_path, file_name, cols):

    import os

    count = 0
    frames = []
    # Iterate directory
    for path in os.listdir(dir_path):
        # check if current path is a file
        if os.path.isfile(os.path.join(dir_path, path)):
            count += 1
            
            if count > 9: # jika file sudah lebih dari sepuluh
                df_path = dir_path+file_name+'0'+str(count)+'.csv'
            else:
                df_path = dir_path+file_name+'00'+str(count)+'.csv'
            
            # membuat dynamic variable
            globals()['df%s' % count] = pd.read_csv(df_path, dtype='string',usecols = cols)
            #print(globals()['df%s' % count])

            # memasukan semua file
            frames.append(globals()['df%s' % count])
            # frames.extend([globals()['df%s' % count]])

    result = pd.concat(frames, ignore_index=True)

    return result

def load_data_multiple_all(dir_path, file_name):

    import os

    count = 0
    frames = []
    # Iterate directory
    for path in os.listdir(dir_path):
        # check if current path is a file
        if os.path.isfile(os.path.join(dir_path, path)):
            count += 1
            
            if count > 9: # jika file sudah lebih dari sepuluh
                df_path = dir_path+file_name+'0'+str(count)+'.csv'
            else:
                df_path = dir_path+file_name+'00'+str(count)+'.csv'
            
            # membuat dynamic variable
            globals()['df%s' % count] = pd.read_csv(df_path, dtype='string')
            #print(globals()['df%s' % count])

            # memasukan semua file
            frames.append(globals()['df%s' % count])
            # frames.extend([globals()['df%s' % count]])

    result = pd.concat(frames, ignore_index=True)

    return result


def clean_number(df, df_columns):

  df[df_columns].replace(' ','', regex=True, inplace=True)
  df[df_columns].replace('[^0-9]','', regex=True, inplace=True) 
  
  return df[df_columns]

def con_fraction(phone):
    if phone == '':
        new_phone = ''
    else:
        new_phone = Fraction(phone)
    return new_phone

def replace_not_valid_to_empty(df, df_columns):

  df.loc[df[df_columns].str.len() < 5, df_columns] = 'empty'
  
  return df[df_columns]

def lowercase(df, df_columns):
    df_columns_lower = df[df_columns].str.lower()
    return df_columns_lower

def clean_space(df, df_columns):
    df[df_columns].replace(' ','', regex=True, inplace=True)
    return df[df_columns]

def delete_email_wrong_format(df, df_columns):

    # cek deleted row
    deleted_row = df.loc[
        (df[df_columns].str.contains('@$', regex=True))|
        (~df[df_columns].str.contains('@', regex=True)) &
        (df[df_columns] != 'empty')
    ].copy()
    

    df.drop(df.loc[
        (df[df_columns].str.contains('@$', regex=True))|
        (~df[df_columns].str.contains('@', regex=True)) &
        (df[df_columns] != 'empty')
    ].index, inplace=True)

    df.reset_index(drop=True, inplace=True)

    return deleted_row.shape[0]

def clean_not_valid_email_format(df, df_columns):
    df[df_columns] = df[df_columns].replace('\s|\`|\^|\&|\<|\>|\(|\)|\?','', regex=True)
    return df_columns


def correct_OTA(df, df_columns):
    
    filter_OTA = 'agoda|booking.com|expedia|tour'
    email_OTA = df.loc[df[df_columns].str.contains(filter_OTA, flags=re.I, regex=True), df_columns] = ''

    # replace email value yang memiliki tanda OTA
    return email_OTA

def find_OTA(df, df_columns):
    
    filter_OTA = 'agoda|booking.com|expedia|tour'
    email_OTA = df.loc[df[df_columns].str.contains(filter_OTA, flags=re.I, regex=True)]

    # replace email value yang memiliki tanda OTA
    return email_OTA

def delete_OTA(df, df_columns):
    
    filter_OTA = 'agoda|booking.com|expedia|tour'
    df.drop(df.loc[df[df_columns].str.contains(filter_OTA, flags=re.I, regex=True)].index, inplace=True)
    df.reset_index(drop=True, inplace=True)

    count_after_clean_OTA = df.shape[0]

    return count_after_clean_OTA

def find_karma(df, df_columns):
    
    # filter_karma = 'karmagroup\.com|@karma|baligetaway|krresidences\.com'
    filter_karma = 'johnspence88@hotmail\.com|baligetaway|rottnestlodge\.com\.au|hotel\.discount|balirewardscard\.com|conceptvenues\.com|discoverkarma\.com|discoveryourkarma\.com|geales\.com|haathimahal\.com|'
    filter_karma += 'adimahkota\.com|baligetaway\.co\.id|baligetaway\.com\.au|catkingproductions\.com|complementarystay-karmaexperience\.com|confirmation-karmaexperience\.com|tiketmurahbali\.com|karmasanctumsoho\.co|'
    filter_karma += 'experiencekarmaclub\.com|karmabavaria\.com|karmabeach\.com|karmaclub\.com|karmadevelopments\.com|karmaestates\.com|karmaexperience\.co\.uk|karmaexperience\.com|karmaexperience\.in|'
    filter_karma += 'karmagroup\.com|karmajimbaran\.com|karmakandara\.com|karmaminoan\.com|karmanormandy\.com|karmapelikanos\.com|karmareef\.com|karmaresorts\.com|karmaroyalexperience\.co\.uk|karmaroyalexperience\.com|'
    filter_karma += 'karmaroyalgroup\.com|karmaroyalvacations\.com|karmasalak\.com|karmasalfordhall\.com|karmastmartins\.com|karmgroup\.com|krresidences\.com|lepreverger\.com|odysseypremier\.com|rci\.com|thebaligetaway\.com'
    filter_karma += 'karmarottnest\.com\.au|karmasanctumonthegreen\.com|karmasanctumclub\.com|balifreestay\.com|karma25\.com|karmarottnest\.com\.au|karmasanctumsoho\.com|karmaroyalpromotions\.com|'
    filter_karma += 'justclickbali\.com|karmaapsara\.com|karmabahamas\.com|karmaborgodicolleoli\.com|karmacamino\.com|karmaclub\.community|karmaclubhouse\.club|karmaclubhouse\.com|karma-concierge|karmaconcierge|'
    filter_karma += 'karmaconstellation\.com|karmadestinations\.com|karmaexperiences\.com|karmaexperiences\.com|karmagroupreviews\.com|karmakasa|karmalaherizza|karmamargaretriver\.com|karmamayura\.com|'
    filter_karma += 'karmaminoan\.com|karmamykonos\.com|karmapassport\.com|karmaprivilege\.com|karmaprivileges\.com|karmaresortdestinations\.com|karmarestaurants\.com|karmaroyalbellavista\.com|karmaroyalboatlagoon\.com|'
    filter_karma += 'karmaroyalresidences\.com|karmasanctum\.com|karmasanctumspa\.com|karmaspa\.com|karmaspas\.com|karmastmartin\.com|karmaubud\.com|karmawinery\.com|krgstorage\.com|mykarmaconcierge\.com|odysseykarma\.com|'
    filter_karma += 'odysseypremier\.com|royalbalitimeshare\.com|royalperspective\.com|royalresortsasia\.com|royalresortstimeshare\.com|sanctumhotel\.com|sanctumsoho\.com|thebaligetaway\.com|thekarmaclub\.com|'
    filter_karma += 'thekarmacollection|themoleandbadger\.com|timesharebali\.com|wildheartbarandgrill\.com|wildheartsoho\.com|yuktamasya\.com'
    email_karma = df.loc[df[df_columns].str.contains(filter_karma, flags=re.I, regex=True)]

    # jika menggunakan type data array
    # filter_karma = ['karmagroup\.com','karmaspa\.com']
    # email_karma = df.loc[df[df_columns].str.contains('|'.join(filter_karma), flags=re.I, regex=True)]

    # print(filter_karma)
    # replace email value yang memiliki tanda OTA
    return email_karma

def delete_karma(df, df_columns):

   # filter_karma = 'karmagroup\.com|@karma|baligetaway|krresidences\.com'
    filter_karma = 'johnspence88@hotmail\.com|baligetaway|rottnestlodge\.com\.au|hotel\.discount|balirewardscard\.com|conceptvenues\.com|discoverkarma\.com|discoveryourkarma\.com|geales\.com|haathimahal\.com|'
    filter_karma += 'adimahkota\.com|baligetaway\.co\.id|baligetaway\.com\.au|catkingproductions\.com|complementarystay-karmaexperience\.com|confirmation-karmaexperience\.com|tiketmurahbali\.com|karmasanctumsoho\.co|'
    filter_karma += 'experiencekarmaclub\.com|karmabavaria\.com|karmabeach\.com|karmaclub\.com|karmadevelopments\.com|karmaestates\.com|karmaexperience\.co\.uk|karmaexperience\.com|karmaexperience\.in|'
    filter_karma += 'karmagroup\.com|karmajimbaran\.com|karmakandara\.com|karmaminoan\.com|karmanormandy\.com|karmapelikanos\.com|karmareef\.com|karmaresorts\.com|karmaroyalexperience\.co\.uk|karmaroyalexperience\.com|'
    filter_karma += 'karmaroyalgroup\.com|karmaroyalvacations\.com|karmasalak\.com|karmasalfordhall\.com|karmastmartins\.com|karmgroup\.com|krresidences\.com|lepreverger\.com|odysseypremier\.com|rci\.com|thebaligetaway\.com'
    filter_karma += 'karmarottnest\.com\.au|karmasanctumonthegreen\.com|karmasanctumclub\.com|balifreestay\.com|karma25\.com|karmarottnest\.com\.au|karmasanctumsoho\.com|karmaroyalpromotions\.com|'
    filter_karma += 'justclickbali\.com|karmaapsara\.com|karmabahamas\.com|karmaborgodicolleoli\.com|karmacamino\.com|karmaclub\.community|karmaclubhouse\.club|karmaclubhouse\.com|karma-concierge|karmaconcierge|'
    filter_karma += 'karmaconstellation\.com|karmadestinations\.com|karmaexperiences\.com|karmaexperiences\.com|karmagroupreviews\.com|karmakasa|karmalaherizza|karmamargaretriver\.com|karmamayura\.com|'
    filter_karma += 'karmaminoan\.com|karmamykonos\.com|karmapassport\.com|karmaprivilege\.com|karmaprivileges\.com|karmaresortdestinations\.com|karmarestaurants\.com|karmaroyalbellavista\.com|karmaroyalboatlagoon\.com|'
    filter_karma += 'karmaroyalresidences\.com|karmasanctum\.com|karmasanctumspa\.com|karmaspa\.com|karmaspas\.com|karmastmartin\.com|karmaubud\.com|karmawinery\.com|krgstorage\.com|mykarmaconcierge\.com|odysseykarma\.com|'
    filter_karma += 'odysseypremier\.com|royalbalitimeshare\.com|royalperspective\.com|royalresortsasia\.com|royalresortstimeshare\.com|sanctumhotel\.com|sanctumsoho\.com|thebaligetaway\.com|thekarmaclub\.com|'
    filter_karma += 'thekarmacollection|themoleandbadger\.com|timesharebali\.com|wildheartbarandgrill\.com|wildheartsoho\.com|yuktamasya\.com'
    df.drop(df.loc[df[df_columns].str.contains(filter_karma, flags=re.I, regex=True)].index, inplace=True)
    df.reset_index(drop=True, inplace=True)

    count_after_clean_karma = df.shape[0]

    return count_after_clean_karma

def email_correction(df, df_columns):

    df[df_columns].replace('mailto:|-primary|-pri|-Mrs|(noemailtobesent)','', regex=True, inplace=True)
    # df[df_columns] = df[df_columns].str.replace(r'(\.com).*', r'\1', regex=True)
    df[df_columns].loc[~df[df_columns].str.contains('@', df_columns, na=False)] = ''
    
    list_correction_mail = ['@mal\.','@mai\.']
    list_correction_gmail = [
        '@gmil\.','@gmaail\.','@gmailo\.','@gmai\.','@gmails\.','@gmal\.','@gmwil\.','@gamail\.','@gmailk\.','@gmzil\.', '@gtmail\.',
        '@gjail\.','@gmaip\.','@gmasil\.','@gmcil\.','@gail\.','@gimail\.','@gmailo\.','@gmaiol\.','@gmaili\.','@fgmail\.','@gamil\.',
        '@gmaill\.','@gmaile\.'
        ]
    list_correction_gmail_com = ['@gmail$','@gmail\.$', '@gmail\.cm','@gmailc\.om', '@gmail\.clm', '@gmail\.con','@@gmail\.clm','@gmail\.coj','@gmail\.cok','@gmail\.c0m',
                                 '@gmail\.comQ', '@gmail\.co$', '@gmail\.vom', '@gmail\.cim','@gmailcom','@gmail\.com;', '@gmail\.comcom\.','@gmail\.comcom;',
                                 '@gmail \.com','@gmail\.comcom-pri','@gmail\.comcom\.','@gmail\.comcom02','@gmail\.com-Daughter','@gmail\.com\.$','@gmail\.com-pri',
                                 '@gmail\.com02','@gmail\.com-Mrs','@gmail\.com-pri']
    list_correction_hotmail = ['@jotmail\.','@hotmil\.','@hotlamil\.','@h0tmail\.','@hotjail\.','@hotmaio\.']
    list_correction_hotmail_com = ['@jotmail\.dom', '@hotmail\.com,']
    list_correction_yahoo_com = ['@yahoo\.com(noemailtobesent)']
    list_correction_yahoo = ['@yahho\.','@yaho\.','@gyahoo\.','@yahoom\.', '@yaoo\.','@yehoo\.','@yahio\.','@rotmail\.','@yshoo\.']
    list_correction_yahoo_in = ['@yahoo\.co\.in-pri']

    # df[df_columns].replace('|'.join(list_correction_mail), '1', regex=True, inplace=True)
    # df[df_columns].replace('|'.join(list_correction_gmail), '2', regex=True, inplace=True)
    # df[df_columns].replace('|'.join(list_correction_gmail_com), '3', regex=True, inplace=True)
    # df[df_columns].replace('|'.join(list_correction_hotmail), '4', regex=True, inplace=True)
    # df[df_columns].replace('|'.join(list_correction_hotmail_com), '5', regex=True, inplace=True)
    # df[df_columns].replace('|'.join(list_correction_yahoo_com), '6', regex=True, inplace=True)
    # df[df_columns].replace('|'.join(list_correction_yahoo), '7', regex=True, inplace=True)
    # df[df_columns].replace('|'.join(list_correction_yahoo_in), '8', regex=True, inplace=True)

    df[df_columns].replace('|'.join(list_correction_mail), '@mail.', regex=True, inplace=True)
    df[df_columns].replace('|'.join(list_correction_gmail), '@gmail.', regex=True, inplace=True)
    df[df_columns].replace('|'.join(list_correction_gmail_com), '@gmail.com', regex=True, inplace=True)
    df[df_columns].replace('|'.join(list_correction_hotmail), '@hotmail.', regex=True, inplace=True)
    df[df_columns].replace('|'.join(list_correction_hotmail_com), '@hotmail.com', regex=True, inplace=True)
    df[df_columns].replace('|'.join(list_correction_yahoo_com), '@yahoo.com', regex=True, inplace=True)
    df[df_columns].replace('|'.join(list_correction_yahoo), '@yahoo.', regex=True, inplace=True)
    df[df_columns].replace('|'.join(list_correction_yahoo_in), '@yahoo.co.in', regex=True, inplace=True)

def clean_missing(df):
    df.replace('MISSING','', regex=True, inplace=True)


def find_phone_by_email(df, column_email, column_phone,  email):
    df_result = df.loc[
        df[column_email] == email &
        ~df[column_phone].str.contains('00000')
    ]
    #for index, row in df_test.iterrows():
        #print(row['Phone'])
    
    return str(df_result[column_email])

# Define a function to categorize contacts
def categorize_contacts(df):
    conditions = [
        (df['Email'].to_numpy() != 'empty') & (df['Phone'].to_numpy() == 'empty') & (df['Mobile'].to_numpy() == 'empty'),
        (df['Email'].to_numpy() == 'empty') & ((df['Phone'].to_numpy() != 'empty') | (df['Mobile'].to_numpy() != 'empty')),
        (df['Email'].to_numpy() != 'empty') & ((df['Phone'].to_numpy() != 'empty') | (df['Mobile'].to_numpy() != 'empty'))
    ]
    choices = ['Email Only', 'Phone Only', 'Email and Phone']
    df['Contact Type'] = np.select(conditions, choices, default='Blank')



def batch(row_count, batch_row):
    i_batch = row_count / batch_row
    result = int(i_batch) # mengubah type data index loop batch menjadi integer agar tidak menjadi float atau memiliki nilai decimal
    return result # return hasil index loop

def insert_batch_loop(df, batch_row, column_index, batch_name):
    # membuat input batch dengan loop

    row_count = df.shape[0] # mengambil total jumlah baris

    result_batch = batch(row_count, batch_row)

    i = result_batch 
    x = range(i) # membuat range data (jumlah loop) berdasarkan jumlah batch yang sudah dibuat di function batch

    # melakukan perulangan berdasarkan jumlah batch dan melakukan slice row (dengan method start:end)
    for n in x:
        start = n * batch_row
        end = start + batch_row
        
        result = str(start)+'-'+str(end) # variabel string untuk melihat range

        df.iloc[start:end,column_index] = str(batch_name)+str(n+1) # column_index(-1) adalah kolom paling terakhir, fungsi ini untuk menambahkan value batch di kolom terakhir

        if n+1 == i: # jika index loop+1 sudah mencapai maximal range loop (menggunakan +1 karena index dimulai dari 0)
            start_last = end # hasil nilai start_last diambil dari hasil nilai row terakhir yang diinputkan loop diatas 
            end_last = row_count # jumlah row keseluruhan
            result_last = str(start_last)+'-'+str(end_last) # varibel string untuk melihat range
            df.iloc[start_last:end_last, column_index] = str(batch_name)+str(i+1)   

    return df

def split_file(df, row_split, file_name, file_type, location):
    # melakukan split file dengan loop

    row_count = df.shape[0] # mengambil total jumlah baris

    result_batch = batch(row_count, row_split)

    i = result_batch
    x = range(i) # membuat range data (jumlah loop) berdasarkan jumlah batch yang sudah dibuat di function batch

    # membuat variable dictionary
    new_df = {}

    # jika jumlah split lebih besar dari jumlah baris data di file
    # maka tidak akan melakukan split file
    if row_split > row_count:

        if file_type == 'csv':
            df.to_csv(location+'\df_'+file_name+'.csv', index=False)
        else:
            df.to_excel(location+'\df_'+file_name+'.xlsx', index=False, engine='xlsxwriter')

    else:

        # melakukan perulangan berdasarkan jumlah split dan memasukannya kedalam dictionary new_df
        for n in x:
            start = n * row_split
            end = start + row_split
            
            new_df[n] = df.iloc[start:end]
            
            if n+1 == i: # jika index loop+1 sudah mencapai maximal range loop (menggunakan +1 karena index dimulai dari 0)
                start_last = end # hasil nilai start_last diambil dari hasil nilai row terakhir yang diinputkan loop diatas 
                end_last = row_count # jumlah row keseluruhan
                new_df[n+1] = df.iloc[start_last:end_last] # memasukan nilai start_last dan end_last kedalam variable terakhir

                ## melakukan export csv dengan fungsi perulangan
    
        # melakukan perulangan berdasarkan dictionary new_df dan export ke csv data split new_df
        for n in new_df:
            i = n+1

            if file_type == 'csv':
                new_df[n].to_csv(location+'\df_'+file_name+'_'+str(i)+'.csv', index=False)
            else:
                new_df[n].to_excel(location+'\df_'+file_name+'_'+str(i)+'.xlsx', index=False, engine='xlsxwriter')

