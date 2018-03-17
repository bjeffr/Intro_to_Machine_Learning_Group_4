from Intro_to_Machine_Learning_Group_4.data_preparation_ratios import ratio_formatter
from Intro_to_Machine_Learning_Group_4.data_preparation_stocks import stock_formatter
import pandas as pd

)
df_ratio = pd.read_csv('ratio_version_one.csv')
count = 0
for i, n in df_stock['date'].iteritems():
    print(i, n)
print(df_ratio[1])

# print(df_stock['date'])
# print(df_ratio['public_date'])


# print(df_ratio.shape)
#
# print(df_stock.shape)
#
# df = df_stock.merge(df_ratio, left_on=['permno', 'date'], right_on=['permno', 'public_date'], how='left')
#
#
# print(df.shape)
#
# df = df.drop('date', axis=1)
# df = df.drop('permno', axis=1)
# #
# print(df.isnull().sum())
# #
# # print(df.columns)