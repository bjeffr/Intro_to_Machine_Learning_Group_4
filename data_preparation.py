import pandas as pd
import scipy as sc
import statsmodels.api as sm
import numpy as np
#import matplotlib.pyplot as plt
from sklearn.preprocessing import Imputer

#Organize the df structure with multi indexies, whereas 'PERMNO' is the first indes and 'date' the second
df_stock = pd.read_csv('stock_version_one.csv')
df_ratio = pd.read_csv('ratio_version_one.csv', index_col=[0,1])

#example to Print all Stock data from Microsoft, indexing is a bit special in panda...here the example to print
#out all the stock data for MSFT and the second one single dates for MSFT and KO.
# print(df_stock.loc[10107])  #all microsoft Stock data
# print(df_stock.loc[[(10107,'31/01/2006') ,(11308, '31/01/2006')]]) #prints specific PERMNO&date

#check for NA values
# for i, row in df_stock.iterrows():
#     if type(row['DCLRDT'])==float:
#         df_stock.set_value(i, 'DCLRDT', '0')
#     if type(row['PAYDT'])==float:
#         df_stock.set_value(i, 'PAYDT', '0')
#     df_stock.set_value(i, 'TICKER', '')

#forwardfill for DIVAMT because $-Value per share of distribution has not only a monthly impact but is rather a constant
#indicator
df_stock['DCLRDT'] = df_stock['DCLRDT'].fillna(0)
df_stock['PAYDT'] = df_stock['PAYDT'].fillna(0)
df_stock['FACPR'] = df_stock['FACPR'].fillna(0)
df_stock['FACSHR'] = df_stock['FACSHR'].fillna(0)

df_stock['DIVAMT'] = df_stock['DIVAMT'].ffill()


# Drop a column if too many NaN or just considered unimportant
df_stock = df_stock.drop('HSICMG', axis=1) #has only values for JPM, NKE and CSCO makes no sense to include
df_stock = df_stock.drop('SPREAD', axis=1)
print(df_stock.isnull().sum())
# print(df_ratio.isnull().sum())
# print(df_stock)



# Impute missing values
# The imputation strategy.
#
# If “mean”, then replace missing values using the mean along the axis.
# If “median”, then replace missing values using the median along the axis.
# If “most_frequent”, then replace missing using the most frequent value along the axis.

# ipr = Imputer(missing_values='NaN', strategy='mean', axis=0)
# ipr = ipr.fit(df_stock.values)
# imputed_data = ipr.transform(df_stock.values)
# same for ratios
# ipr = Imputer(missing_values='Na', strategy='mean', axis=0)
# ipr = ipr.fit(df_ratio.values)
# imputed_data = ipr.transform(df_ratio.values)