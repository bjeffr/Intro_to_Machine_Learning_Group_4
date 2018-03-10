import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
import sklearn.preprocessing

df_stock = pd.read_csv('stock_version_one.csv').set_index('TICKER')
print(df_stock.head())

#check for NA values
print(df_stock.isnull().sum())

#Impute missing values
