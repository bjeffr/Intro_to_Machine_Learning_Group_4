import pandas as pd
import scipy as sc
import statsmodels.api as sm
import numpy as np
#import matplotlib.pyplot as plt
from sklearn.preprocessing import Imputer

#Organize the df structure with multi indexies, whereas 'PERMNO' is the first indes and 'date' the second
df_stock = pd.read_csv('stock_version_one.csv', index_col=[0,1])
df_ratio = pd.read_csv('ratio_version_one.csv', index_col=[0,1])

#example to Print all Stock data from Microsoft, indexing is a bit special in panda...here the example to print
#out all the stock data for MSFT and the second one single dates for MSFT and KO.
# print(df_stock.loc[10107])  #all microsoft Stock data
# print(df_stock.loc[[(10107,'31/01/2006') ,(11308, '31/01/2006')]]) #prints specific PERMNO&date

#check for NA values
# print(df_stock.isnull().sum())

# Drop a column if too many NaN or just considered unimportant
# df_stock = df_stock.drop('SPREAD', axis=1)




#Impute missing values
# The imputation strategy.
#
# If “mean”, then replace missing values using the mean along the axis.
# If “median”, then replace missing values using the median along the axis.
# If “most_frequent”, then replace missing using the most frequent value along the axis.

ipr = Imputer(missing_values='Na', strategy='', axis=0)
