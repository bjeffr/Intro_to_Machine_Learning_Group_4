from Intro_to_Machine_Learning_Group_4.data_preparation import clean_data
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn import metrics
import graphviz

def set_style():
    plt.style.use('seaborn-whitegrid')
    plt.rcParams['font.size'] = 14


def test_function():

    df = clean_data()
    df = df.drop(columns='Date')
    print(df.head())
    # create the response vector (up or down movement)
    today = np.log(df['PRC'] / df['PRC'].shift(-1))
    direction = np.where(today >= 0, 1, 0)

    delta = np.log(df['PRC'].shift(-1) / df['PRC'].shift(-2))
    df.insert(2, 'delta', delta)


    df['delta'] = df['delta'].fillna(0)

    # distignuish between columns that have to be scaled and the dummy columns
    cols = df.columns.values
    cols_scl = cols[:36]
    cols_dummy = cols[36:]


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
                         #Feature Engineering, Scaling, and Cros
    # s Validation
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

    # dot -Tpng tree.dot
    # dot tree.dot -Tpng -o image.png

    #****************-------------------*********************----------------------*******************--------------------
                         #Grid Search
    #****************-------------------*********************----------------------*******************--------------------

    # define the hyperparameter values to be tested

    #
    # maxDepth = np.array([1,4,5,6,9])
    # minSamplesNode = np.array([2,5,10,20])
    # minSamplesLeaf = np.array([2,5,10,20])
    #
    # kFold = StratifiedKFold(n_splits=10, random_state=10)
    #
    # param_grid = {'criterion': ['gini', 'entropy'],
    #               'max_depth': maxDepth,
    #               'min_samples_split': minSamplesNode,
    #               'min_samples_leaf': minSamplesLeaf}
    #
    #
    #
    # gs = GridSearchCV(estimator=DecisionTreeClassifier(random_state=0),
    #                   param_grid=param_grid,
    #                   scoring='accuracy',
    #                   cv=kFold, n_jobs=3)
    # gs = gs.fit(X_train, y_train)
    #
    # print(gs.best_score_)
    # print(gs.best_params_)
    # clf = gs.best_estimator_
    # clf.fit(X_train, y_train)

    #****************-------------------*********************----------------------*******************--------------------
                          #Support Vector Machines
    #****************-------------------*********************----------------------*******************--------------------

    # from sklearn.svm import SVC
    #
    # # create object
    #
    # svm_linear = SVC(kernel='linear', C=1.0)
    #
    # # Fit linear SVM to standardized training set
    # svm_linear.fit(X_train, y_train)
    #
    # print("Observed probability of Up: ")



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

if __name__ == "__main__":
    set_style()
    test_function()


