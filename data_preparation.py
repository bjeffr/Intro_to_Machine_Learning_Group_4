import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sklearn.preprocessing


plt.style.use('seaborn-whitegrid')

df_stock = pd.read_csv('stock_version_one.csv',).set_index('TICKER')

#check for NA values
print(df_stock.isnull().sum())

#Impute missing values
ipr = imputation.im