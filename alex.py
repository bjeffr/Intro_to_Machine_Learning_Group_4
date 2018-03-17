from Intro_to_Machine_Learning_Group_4.data_preparation import ratio_formatter
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier, export_graphviz
import graphviz
from sklearn import metrics


plt.style.use('seaborn-whitegrid')
plt.rcParams['font.size'] = 14


df = ratio_formatter()
cols = df.columns.values
cols_scl = cols[2:-1]
cols_dummy = cols[-1:]
# print(df[cols_scl].head())
today = np.log(df['PRC'] / df['PRC'].shift(-1))
direction = np.where(today >= 0, 1, 0)
# print(df.head())

#****************-------------------*********************----------------------*******************--------------------
                     #Feature Engineering, Scaling, and Cross Validation
#****************-------------------*********************----------------------*******************--------------------

#assign response vector
y = direction

X_train, X_test, y_train, y_test = train_test_split(df[cols], y, test_size=0.3, random_state=0, stratify=y)
# print(X_train.head())
stdsc = StandardScaler()

X_train_std = stdsc.fit_transform(X_train[cols_scl])
# fit & transform
X_test_std = stdsc.transform(X_train[cols_scl]) #only transform


# X_train_std = stdsc.fit_transform(X_train[['SICCD', 'DIVAMT', 'BIDLO', 'ASKHI', 'PRC', 'VOL', 'SHROUT', 'RETX', 'ewretd']])

#****************-------------------*********************----------------------*******************--------------------
                     #Feature Engineering, Scaling, and Cross Validation
#****************-------------------*********************----------------------*******************--------------------
print(cols)
tree = DecisionTreeClassifier(max_depth=4)
tree.fit(X_train, y_train)

#print peformance metrics
print('True proportions of movement >= 4k: ', y.sum() / y.shape[0])
print('Train score: ', tree.score(X_train, y_train))
print('Test score: ', tree.score(X_test, y_test))
print(37*'-')

# # ugly Confusion Matrix
y_pred = tree.predict(X_test)
# print('Confusion matrix: \n', metrics.confusion_matrix(y_test, y_pred))

# nice confusion matrix as pandas df
confm = pd.DataFrame({'Predicted movement >=4k': y_pred, 'True movement >=4k': y_test})
confm.replace(to_replace={0:'No', 1:'Yes'}, inplace=True)
print(confm.groupby(['True movement >=4k', 'Predicted movement >=4k']).size().unstack('Predicted movement >=4k'))

#graphviw draw decition tree

dot_data = export_graphviz(tree, filled=True, rounded=True,\
           class_names=['Down', 'Up'], feature_names=df[cols].columns.values,
            out_file='tree.dot')

graph = graphviz.Source(dot_data)
graph


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