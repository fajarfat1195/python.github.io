def check_exists(df1, df2, cols1, cols2, cols_fill):
    df1.loc[df1[cols1].isin(df2[cols2]), cols_fill] = 'Exists'
    df1.loc[~df1[cols1].isin(df2[cols2]), cols_fill] = 'Not Exists'
    
    return 'success'


