import pandas as pd
from sklearn.preprocessing import Imputer
import numpy as np
#import matplotlib.pyplot as plt
from sklearn.preprocessing import Imputer

df_stock = pd.read_csv('stock_version_one.csv').set_index('TICKER')
print(df_stock.date['MSFT'])

#check for NA values
print(df_stock.isnull().sum())

#Impute missing values
# The imputation strategy.
#
# If “mean”, then replace missing values using the mean along the axis.
# If “median”, then replace missing values using the median along the axis.
# If “most_frequent”, then replace missing using the most frequent value along the axis.

ipr = Imputer(missing_values='Na', strategy='')
