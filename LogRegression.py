
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
from sklearn import metrics
from Intro_to_Machine_Learning_Group_4.data_preparation import clean_data


def response_vector(df, column):

    today = np.log(df[column] / df[column].shift(-1))
    return np.where(today >= 0, 1, 0)


def log_reg(df):

    df = df.drop(columns='Date')
    df.VOL = pd.DataFrame(df.VOL, dtype='float')
    df.SHROUT = pd.DataFrame(df.SHROUT, dtype='float')

    df['SICCD'] = df['SICCD'].astype(str)
    df = pd.get_dummies(df)

    df['Response'] = response_vector(df, 'PRC')
    df = df.drop(columns='PRC')
    print(len(df[df['Response'] == 1])/df.Response.count())

    # Assign features to matrix X and response to y
    x = df.drop(columns='Response')
    y = df.Response

    logisticRegr = LogisticRegression()
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)

    logisticRegr.fit(x_train, y_train)
    score = logisticRegr.score(x_test, y_test)
    print(score)
    predictions = logisticRegr.predict(x_test)
    cm = metrics.confusion_matrix(y_test, predictions)
    print(cm)

    cols_scl = list(x.select_dtypes(include=['float64']).columns)

    mms = MinMaxScaler()
    x_train_norm = mms.fit_transform(x_train[cols_scl])  # fit & transform
    x_test_norm = mms.transform(x_test[cols_scl])  # ONLY transform
    logisticRegr.fit(x_train_norm, y_train)
    score = logisticRegr.score(x_test_norm, y_test)
    print(score)

    stdsc = StandardScaler()
    x_train_std = stdsc.fit_transform(x_train[cols_scl])  # fit & transform
    x_test_std = stdsc.transform(x_test[cols_scl])  # ONLY transform
    logisticRegr.fit(x_train_std, y_train)
    score = logisticRegr.score(x_test_std, y_test)
    print(score)

pd.set_option('display.height', 500)
pd.set_option('display.max_rows', 500)
log_reg(clean_data())
