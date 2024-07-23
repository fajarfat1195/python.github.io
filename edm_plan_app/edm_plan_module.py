import pandas as pd
import numpy as np
from datetime import datetime

import re

def load_all_sheets(file_path, cols):
    xl = pd.ExcelFile(file_path)

    sheets = xl.sheet_names  # see all sheet names
    
    count = 0
    frames = [] # list untuk wadah dataframe yang diloop
    sheets_array = [] # list untuk data nama kolom
    sheet_failed_concat = [] # list untuk sheet yang gagal diconcat karena nama kolomnya tidak ada(berbeda) di sheet tersebut

    # Iterate name sheets
    for s in sheets:
        count += 1

        globals()['df%s' % count] = pd.read_excel(file_path, dtype='string', sheet_name=s)
        #print(globals()['df%s' % count])

        df = globals()['df%s' % count]

        # konversi array biasa menjadi numpy array
        np_cols = np.array(cols)
        np_df_cols = np.array(df.columns)

        # check value eksis di salah satu array menggunakan method isin (output akan menjadi array yang memiliki nilai TRUE atau FALSE)
        check_cols = np.isin(np_cols, np_df_cols)

        # jika output numpy isin memiliki value FALSE
        if np.isin(False, check_cols):
            sheet_failed_concat.append(s) # tidak memasukan ke dalam dataframe concat, menambahkan kedalam list daftar sheet yang gagal
        else:
            frames.append(globals()['df%s' % count]) # memasukan ke dalam daftar concat
            sheets_array.append(s)

    # dfs = pd.concat(frames, ignore_index=True)
    # return dfs

    # concat dataframe dan menambahkan kolom nama sheets
    dfs = pd.concat(
    frames, 
    keys=sheets_array,
    names=['Sheets Name', None],
    ).reset_index(level='Sheets Name')   
    # reset index agar nomor indexnya berurutan
    dfs.reset_index(drop=True, inplace=True)

    cols.append('Sheets Name') # menambahkan kolom sheetname di list daftar kolom
    dfs = dfs.reindex(columns=cols) # mengatur ulang tampilan dan urutan index kolom

    return dfs