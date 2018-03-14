import pandas as pd

def ratio_formatter():

    df_ratio = pd.read_csv('ratio_version_one.csv', index_col=[0,1])
    return df_ratio
