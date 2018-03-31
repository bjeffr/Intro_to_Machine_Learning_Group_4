from Intro_to_Machine_Learning_Group_4.data_preparation import clean_data
from Intro_to_Machine_Learning_Group_4 import grid_search
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd


df = clean_data()
df = df.drop(columns='Date')

# create the response vector (up or down movement)
today = np.log(df['PRC'] / df['PRC'].shift(-1))
direction = np.where(today >= 0, 1, 0)
y = direction

# print(forest.fit(X_train, y_train))

if __name__ == "__main__":

    df = clean_data()
    df = df.drop(columns='Date')
    clf = grid_search.grid_search(df)
    X_train, X_test, y_train, y_test = train_test_split(df, y, test_size=0.3, random_state=0, stratify=y)

    forest = RandomForestClassifier(criterion=clf.criterion, max_depth=clf.max_depth,
                                    min_samples_leaf=clf.min_samples_leaf, min_samples_split= clf.min_samples_split,
                                    random_state=0, n_jobs=-1)
    print(15*'-', 'test Score', 15*'-', '\n')
    print('Test accuracy: {0: .4f}'.format(clf.score(X_test, y_test)))

    #fit forest
    forest.fit(X_train, y_train)
    y_pred = forest.predict(X_test)

    # nice confusion matrix as pandas df
    confm = pd.DataFrame({'Predicted movement': y_pred, 'True movement': y_test})
    confm.replace(to_replace={0: 'Down', 1: 'UP'}, inplace=True)
    print(15*'-', 'Confusion Matrix', 15*'-', '\n')
    print(confm.groupby(['True movement', 'Predicted movement']).size().unstack('Predicted movement'))
