import pandas as pd
from sklearn.preprocessing import Imputer
import numpy as np
import matplotlib.pyplot as plt

df_stock = pd.read_csv('stock_version_one.csv')
print(df_stock.loc[df_stock['TICKER'] == 'MSFT'])