from Intro_to_Machine_Learning_Group_4 import data_preparation_stocks as sp
import numpy as np
import pandas as pd


from Intro_to_Machine_Learning_Group_4.data_preparation_ratios import ratio_formatter

#Funktion die mir angibt wie viele NaN Werte in den Ratios vorkommen
df_ratio = ratio_formatter()
print(df_ratio.isnull().sum())
