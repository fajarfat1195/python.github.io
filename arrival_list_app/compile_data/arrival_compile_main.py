import pandas as pd
import re
import numpy as np
import openpyxl

def get_data_segment_single_header(sheets_name, df, arr_index, cols, key_columns):

    count_data = df.shape[0]

    start_segment = arr_index[0] # start segment ialah variabel yang berisi nilai index row yang akan digunakan sebagai awal data, dalam artian index row header
    end_segment = count_data # end segment ialah variabel yang berisi nilai akhir berdasarkan nomor index jumlah keseluruhan data akhir

    new_df = df.iloc[start_segment:end_segment].reset_index(drop=True).copy()
    new_df.columns = new_df.iloc[0] # define kolom berdasarkan row paling awal
    new_df.drop([0,0], inplace=True) # menghapus row yang sudah dijadikan kolom (karena meskipun row index 0 sudah di define sebagai kolom, row index 0 tetap ada di row record data)
    arr_df = new_df[cols].loc[~new_df[key_columns].isna()].copy() # menghapus baris data berdasarkan key_columns yang kosong
    arr_df.reset_index(drop=True, inplace=True)
    arr_df['Sheet Name'] = sheets_name
    result = arr_df

    return result

def get_data_segment_multi_header(sheets_name, df, count_header, arr_index, cols, key_columns):

    count_data = df.shape[0]

    count = 0
    frames = []
    for i in arr_index:
        count += 1
        start_segment_index = i
        end_segment_index = count

        if count == count_header: # menggunakan count sebagai kondisi agar loop terakhir bisa dicek melalui jumlah count header
            start_segment = i # start segment ialah variabel yang berisi nilai index row yang akan digunakan sebagai awal data, dalam artian index row header
            end_segment = count_data # end segment adalah nilai akhir berdasarkan jumlah data keseluruhan
            
            # # range index row tiap segment data yang digunakan
            # print('Count : '+str(count)+' Count Header : '+str(count_header)+'')
            # print(str(i)+'-'+str(count_data)+' baris terakhir')
           
        else:
            start_segment = i

            # arr_index adalah list yang terdiri dari nilai start index semua header
            # arr_index[end_segment_index] adalah data index start header "SETELAH" nilai index start header yang di loop saat ini

            # arr_index[end_segment_index] dikurangi 2 karena end segment dari columns header pertama adalah sampai columns header kedua yang dimana ada nilai title headernya
            # title header ada 2 baris dan oleh sebab itu kita row baris title headernya agar tidak masuk ke record data

            end_segment = arr_index[end_segment_index] - 2

            # range index row tiap segment data yang digunakan
            # print('Count : '+str(count)+' Count Header : '+str(count_header)+'')
            # print(str(i)+'-'+str(arr_index[end_segment_index]))
        
        globals()['new_df%s' % count] = df.iloc[start_segment:end_segment].reset_index(drop=True).copy()
        globals()['new_df%s' % count].columns = globals()['new_df%s' % count].iloc[0] # define kolom berdasarkan row paling awal
        globals()['new_df%s' % count].drop([0,0], inplace=True) # menghapus row yang sudah dijadikan kolom (karena meskipun row index 0 sudah di define sebagai kolom, row index 0 tetap ada di row record data)
        globals()['arr_df%s' % count] = globals()['new_df%s' % count][cols].loc[~globals()['new_df%s' % count][key_columns].isna()].copy() # menghapus baris data berdasarkan key_columns yang kosong
        globals()['arr_df%s' % count].reset_index(drop=True, inplace=True)
        globals()['arr_df%s' % count]['Sheet Name'] = sheets_name


        frames.append(globals()['arr_df%s' % count])

    result = pd.concat(frames, ignore_index=True)

    return result
            
def load_data_multiple(path, sheet_will_be_used, cols, key_columns):

    count = 0
    frames = []
    # print(dir_path)
    # print(sheet_will_be_used)

    for i in sheet_will_be_used:
        # print('Compiling sheets '+i+' On progress')
        sheets_progress = 'Compiling sheets ['+i+'] - On progress'
        count += 1
        globals()['df%s' % count] = pd.read_excel(path, dtype='string', sheet_name=i, index_col=None, header=None)
        # count header -> jumlah header columns yang ada di sheets (menghitung berdasarkan jumlah nilai 'key columns' yang ada di sheet tersebut)
        count_header = globals()['df%s' % count].loc[globals()['df%s' % count][0] == key_columns].shape[0]

        # kumpulan index row dari setiap header columns yang ada di sheets
        arr_index = globals()['df%s' % count].loc[globals()['df%s' % count][0] == key_columns].index

        sheet_name = i

        if count_header == 1:
            header_progress = 'Proses Single Header'
            globals()['new_df%s' % count] = get_data_segment_single_header(sheet_name, globals()['df%s' % count], arr_index, cols, key_columns)

        elif count_header > 1:
            header_progress = 'Proses Multiple Header'
            globals()['new_df%s' % count] = get_data_segment_multi_header(sheet_name, globals()['df%s' % count], count_header, arr_index, cols, key_columns)

        else:
            header_progress = 'Column Header Not Found'

        print(sheets_progress+' : '+header_progress)

        frames.append(globals()['new_df%s' % count])

    result = pd.concat(frames, ignore_index=True)

    return result