from Intro_to_Machine_Learning_Group_4 import data_preparation_stocks as sp
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn import metrics


plt.style.use('seaborn-whitegrid')
plt.rcParams['font.size'] = 14

df =

#distignuish between columns that have to be scaled and the dummy columns
cols = df.columns.values
cols_scl = cols[2:-1]
cols_dummy = cols[-1:]

# create the response vector (up or down movement)
today = np.log(df['PRC'] / df['PRC'].shift(-1))
direction = np.where(today >= 0, 1, 0)


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

