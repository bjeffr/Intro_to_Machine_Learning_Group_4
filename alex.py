from Intro_to_Machine_Learning_Group_4 import data_preparation_stocks as sp
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


from sklearn import metrics
plt.style.use('seaborn-whitegrid')
plt.rcParams['font.size'] = 14


df_stock = sp.stock_formatter()

today = np.log(df_stock['PRC'] / df_stock['PRC'].shift(-1))
direction = np.where(today >= 0, 1, 0)
print(df_stock.head())

#****************-------------------*********************----------------------*******************--------------------
                     #Feature Engineering, Scaling, and Cross Validation
#****************-------------------*********************----------------------*******************--------------------

#assign response vector
y = direction

X_train, X_test, y_train, y_test = train_test_split(df_stock, y, test_size=0.3, random_state=0, stratify=y)

stdsc = StandardScaler()
X_train_std = stdsc.fit_transform(X_train[['SICCD', 'DIVAMT', 'BIDLO', 'ASKHI', 'PRC', 'VOL', 'SHROUT', 'ewretd']])

# X_train_std = stdsc.fit_transform(X_train[['SICCD', 'DIVAMT', 'BIDLO', 'ASKHI', 'PRC', 'VOL', 'SHROUT', 'RETX', 'ewretd']])



#****************-------------------*********************----------------------*******************--------------------
                     #Linear and Quadratic Discriminant Analysis
#****************-------------------*********************----------------------*******************--------------------

# for permno, new_df in df_stock.groupby(level=0):
#     today = np.log(new_df['PRC'] / new_df['PRC'].shift(-1))
#     direction = np.where(today >= 0, 1, 0)
#
#     X_train = new_df[['DCLRDT', 'PAYDT', 'BIDLO', 'ASKHI', 'PRC', 'VOL', 'SHROUT', 'RETX', 'ewretd']]
   # print(X_train)


#****************-------------------*********************----------------------*******************--------------------
                      #k-Nearest Neighbors
#****************-------------------*********************----------------------*******************--------------------


# df_stock = df_stock.set_index(['PERMNO', 'date'])
#
# for permno, new_df in df_stock.groupby(level=0):
#
#     today = np.log(new_df['PRC']/new_df['PRC'].shift(-1))
#     # print(new_df.head())
#     direction = np.where(today >= 0, 1, 0)
#
#     direction = pd.DataFrame(direction, index=today.index)
#     new_df['direction'] = direction.values
#     #print(new_df.loc[[(permno)]])
#     break








# Impute missing values
# The imputation strategy.
#
# If “mean”, then replace missing values using the mean along the axis.
# If “median”, then replace missing values using the median along the axis.
# If “most_frequent”, then replace missing using the most frequent value along the axis.

# ipr = Imputer(missing_values='NaN', strategy='most_frequent', axis=0)
# ipr = ipr.fit(df_stock.values)
# imputed_data = ipr.transform(df_stock.values)
# # same for ratios
# ipr = Imputer(missing_values='Na', strategy='mean', axis=0)
# ipr = ipr.fit(df_ratio.values)
# imputed_data = ipr.transform(df_ratio.values)