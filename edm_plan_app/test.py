import pandas as pd
import numpy as np
from datetime import datetime

import re

def load_all_sheets(file_path, cols):
    xl = pd.ExcelFile(file_path)

    sheets = xl.sheet_names  # see all sheet names
    
    count = 0
    frames = []
    sheets_array = []
    # Iterate directory
    for s in sheets:

        globals()['df%s' % count] = pd.read_excel(file_path, dtype='string', sheet_name=s, usecols=cols)
        #print(globals()['df%s' % count])

        # memasukan semua file
        frames.append(globals()['df%s' % count])
        sheets_array.append(s)

        df = pd.concat(frames, ignore_index=True)

        # # concat dataframe dan menambahkan kolom nama sheets
        # dfs = pd.concat(
        # frames, 
        # keys=sheets_array,
        # names=['Sheets Name', None],
        # ).reset_index(level=0)   
        # # reset index agar nomor indexnya berurutan
        # dfs.reset_index(drop=True, inplace=True)

    return df