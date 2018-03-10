import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sklearn.preprocessing


<<<<<<< HEAD
plt.style.use('seaborn-whitegrid')
=======
print(df_stock[[]['MSFT']])
>>>>>>> 8e649acd2d517fb222d44c706eab3743bcb65f44

df_stock = pd.read_csv('stock_version_one.csv',).set_index('TICKER')

#check for NA values
print(df_stock.isnull().sum())

#Impute missing values
ipr = imputation.im