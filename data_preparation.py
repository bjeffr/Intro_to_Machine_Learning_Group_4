import pandas as pd

df_stock = pd.read_csv('stock_version_one.csv',).set_index('TICKER')

print(df_stock.head())

print(df_stock[[]['MSFT']])



