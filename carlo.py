from data_preparation_ratios import ratio_formatter

#Funktion die mir angibt wie viele NaN Werte in den Ratios vorkommen
df_ratio = ratio_formatter()
print(df_ratio.isnull().sum())
