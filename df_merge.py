from Intro_to_Machine_Learning_Group_4.data_preparation_ratios import ratio_formatter
from Intro_to_Machine_Learning_Group_4.data_preparation_stocks import stock_formatter

df_ratio = ratio_formatter()
df_stock = stock_formatter()


print(df_ratio.shape)

print(df_stock.shape)

df = df_stock.merge(df_ratio, left_on=['permno', 'date'], right_on=['permno', 'public_date'], how='left')


print(df.shape)

df = df.drop('date', axis=1)
df = df.drop('permno', axis=1)
#
print(df.isnull().sum())
#
# print(df.columns)