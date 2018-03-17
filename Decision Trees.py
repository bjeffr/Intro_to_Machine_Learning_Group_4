from Intro_to_Machine_Learning_Group_4.data_preparation import clean_data
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn import metrics
import graphviz


plt.style.use('seaborn-whitegrid')
plt.rcParams['font.size'] = 14

df = clean_data()
df = df.drop(columns='public_date')

# create the response vector (up or down movement)
today = np.log(df['PRC'] / df['PRC'].shift(-1))
direction = np.where(today >= 0, 1, 0)

delta = np.log(df['PRC'].shift(-1) / df['PRC'].shift(-2))
df.insert(2, 'delta', delta)


print(type(today[3]))
df['delta'] = df['delta'].fillna(0)

# distignuish between columns that have to be scaled and the dummy columns
cols = df.columns.values
cols_scl = cols[:37]
cols_dummy = cols[37:]


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
tree = DecisionTreeClassifier(max_depth=5, min_samples_leaf=10)
tree.fit(X_train, y_train)

#print peformance metrics
print('True proportions of up Movements movement: ', y.sum() / y.shape[0])
print('Train score: ', tree.score(X_train, y_train))
print('Test score: ', tree.score(X_test, y_test))
print(37*'-')

# # ugly Confusion Matrix
y_pred = tree.predict(X_test)
# print('Confusion matrix: \n', metrics.confusion_matrix(y_test, y_pred))

# nice confusion matrix as pandas df
confm = pd.DataFrame({'Predicted movement UP': y_pred, 'True movement UP': y_test})
confm.replace(to_replace={0:'No', 1:'Yes'}, inplace=True)
print(confm.groupby(['True movement UP', 'Predicted movement UP']).size().unstack('Predicted movement UP'))



#graphviw draw decition tree

dot_data = export_graphviz(tree, filled=True, rounded=True,\
           class_names=['Down', 'Up'], feature_names=df[cols].columns.values,
            out_file='tree.dot')

graph = graphviz.Source(dot_data)
graph



# dot -Tpng tree.dot
# dot tree.dot -Tpng -o image.png