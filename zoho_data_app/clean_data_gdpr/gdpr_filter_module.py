import pandas as pd
import numpy as np
from datetime import datetime

import re

def get_eu():
    eu = ['Russia', 'Germany', 'France', 'Italy', 'Spain','Ukraine','Poland','Romania','Netherlands','Belgium','Czechia','Greece','Portugal','Sweden','Hungary',
        'Belarus','Austria','Serbia','Switzerland','Bulgaria','Denmark','Finland','Slovakia','Norway','Ireland','Croatia','Moldova','Bosnia','Herzegovina','Albania','Lithuania',
        'North Macedonia','Slovenia','Latvia','Kosovo','Estonia','Montenegro','Luxembourg','Malta','Iceland','Andorra','Monaco','Liechtenstein','San Marino','Holy See',
        'Czech Republic','Israel','New Caledonia','Republic of Cyprus']
    return eu

def get_uk():
    uk = ['England', 'United Kingdom', 'Wales', 'Scotland', 'Northern ireland']
    return uk


def eu_teritory(df):
    f_1 = (df['Country'].str.contains('|'.join(get_eu()), regex=True, flags=re.I))
    f_2 = (df['EU Territory'] == 'false')
    final_filter = (
        f_1 &
        f_2
    )

    return final_filter

def uk_teritory(df):
    f_1 = (df['Country'].str.contains('|'.join(get_uk()), regex=True, flags=re.I))
    f_2 = (df['United Kingdom'] == 'false')
    final_filter = (
        f_1 &
        f_2
    )

    return final_filter

