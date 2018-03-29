from Intro_to_Machine_Learning_Group_4.data_preparation import clean_data
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

from pandas.plotting import scatter_matrix


def grid_search(df):


    # create the response vector (up or down movement)
    today = np.log(df['PRC'] / df['PRC'].shift(-1))
    direction = np.where(today >= 0, 1, 0)

    delta = np.log(df['PRC'].shift(-1) / df['PRC'].shift(-2))
    df.insert(2, 'delta', delta)


    df['delta'] = df['delta'].fillna(0)

    # distignuish between columns that have to be scaled and the dummy columns
    cols = df.columns.values

    #****************-------------------*********************----------------------*******************--------------------
                         #Feature Engineering, Scaling, and Cross Validation
    #****************-------------------*********************----------------------*******************--------------------

    #assign response vector
    y = direction

    X_train, X_test, y_train, y_test = train_test_split(df, y, test_size=0.3, random_state=0, stratify=y)

    X_train, X_test, y_train, y_test = train_test_split(df[cols], y, test_size=0.3, random_state=0, stratify=y)
    # print(X_train.head())
    stdsc = StandardScaler()
    X_train_std = stdsc.fit_transform(X_train)

    # transform test set
    X_test_std = stdsc.transform(X_test)


# ------------------------------------------------------------------------------------------------
    scatter_matrix(df[cols[:3]], alpha=0.2, figsize=(6, 6), diagonal='kde')


# ------------------------------------------------------------------------------------------------



    #****************-------------------*********************----------------------*******************--------------------
                         #Grid Search
    #****************-------------------*********************----------------------*******************--------------------

    # define the hyperparameter values to be tested


    maxDepth = np.array([1,4,5,6,9])
    minSamplesNode = np.array([2,5,10,20])
    minSamplesLeaf = np.array([2,5,10,20])

    kFold = StratifiedKFold(n_splits=10, random_state=5)

    param_grid = {'criterion': ['gini', 'entropy'],
                  'max_depth': maxDepth,
                  'min_samples_split': minSamplesNode,
                  'min_samples_leaf': minSamplesLeaf}



    gs = GridSearchCV(estimator=DecisionTreeClassifier(random_state=0),
                      param_grid=param_grid,
                      scoring='accuracy',
                      cv=kFold, n_jobs=-1)
    gs = gs.fit(X_train_std, y_train)

    print(gs.best_score_)
    print(gs.best_params_)

    clf = gs.best_estimator_
    print(clf)
    print(clf.fit(X_train_std, y_train))

    # Print out score on Test dataset
    # print('Test accuracy : {0: .4 f}'.format(clf.score(X_test_std, y_test)))

if __name__ == "__main__":

    df = clean_data()
    df = df.drop(columns='Date')

    grid_search(df)


