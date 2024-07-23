import pprint
import pandas as pd
import numpy as np
from normalization import setDateTime
from debounce import Debounce
deb = Debounce()

# # Find Email Not Process
# data = select('data_guestline','id,Email','meta_id >= 190 AND debounce_check=0 AND Email !="" AND Email_Status ==""')
# print(len(data), ' ROWS')
# for rw in data:
#     dd = dict()
#     print(rw)
#     print('Debonce Check')
#     deb_data = deb.validonce(rw['Email'])
#     dd = deb_data['debounce']
#     print(deb_data)
#     print('updating')
#     update('data_guestline', 'Email_Status="'+deb_data['debounce']['reason']+'",debounce_check=1', 'id='+str(rw['id']))
#     dd['created'] = setDateTime()
#     post(deb_data['debounce'], 'data_debounce')
#     print("==============")

def debounce_check(email):
    deb_data = deb.validonce(email)
    test = deb_data['debounce']['reason']
    return test

path = r'C:\Users\fajar\Documents\Python\Data\normalize_cancelled.csv'
df_past_guest = pd.read_csv(path, dtype='string', encoding='utf8')

df_past_guest['Email_status'] = df_past_guest.apply(
    lambda x: debounce_check(x['Email']),
    axis=1,
)

df_past_guest.to_csv(r'C:\Users\fajar\Documents\Python\Data\normalize_cancelled_debounce.csv', index=False, encoding='utf8')

# deb_data = deb.validonce('fajarfatonisocial@gmail.com')
# test = deb_data['debounce']['reason']
# print(test)