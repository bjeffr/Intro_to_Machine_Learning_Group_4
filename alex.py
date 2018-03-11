from Intro_to_Machine_Learning_Group_4 import data_preparation_stocks as sp
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')
plt.rcParams['font.size'] = 14


df_stock = sp.stock_formatter()

#****************-------------------*********************----------------------*******************--------------------

#****************-------------------*********************----------------------*******************--------------------


df_stock = df_stock.set_index(['PERMNO', 'date'])

for permno, new_df in df_stock.groupby(level=0):

    today = np.log(new_df['PRC']/new_df['PRC'].shift(-1))
    # print(new_df.head())
    direction = np.where(today >= 0, 1, 0)

    direction = pd.DataFrame(direction, index=today.index)
    new_df['direction'] = direction.values
    print(new_df.loc[[(permno)]])
    break








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