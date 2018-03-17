import pandas as pd
from sklearn import preprocessing as pp
from Intro_to_Machine_Learning_Group_4 import data_preparation_ratios as ra


def stock_formatter():
    # Load the csv file for the stocks data and store it as a dataframe
    df_stock = pd.read_csv('stock_version_one.csv')

    # For use with multi index:
    # example to Print all Stock data from Microsoft, indexing is a bit special in panda...here the example to print
    # out all the stock data for MSFT and the second one single dates for MSFT and KO.
    # print(df_stock.loc[10107])  #all microsoft Stock data
    # print(df_stock.loc[[(10107,'31/01/2006') ,(11308, '31/01/2006')]]) #prints specific PERMNO&date

    # ****************---------------***************-----------------*************-----------------
    #                       reformatting the dataframe stock
    # ****************---------------***************-----------------*************-----------------

    # fill all NaN values in the date columns with 0
    df_stock['DCLRDT'] = df_stock['DCLRDT'].fillna(0)
    df_stock['PAYDT'] = df_stock['PAYDT'].fillna(0)
    df_stock['FACPR'] = df_stock['FACPR'].fillna(0)
    df_stock['FACSHR'] = df_stock['FACSHR'].fillna(0)
    # next step is to fill the existing values in the date columns with a 1, therefore making it a binary variable
    # the dates are mostly somewhere in the middle of the month and because we utilize monthly data we just
    # indicate if for example a dividend was payed in that month
    for i, row in df_stock.iterrows():
        if row['PAYDT'] != 0:
            df_stock.set_value(i, 'PAYDT', 1)
        if row['DCLRDT'] != 0:
            df_stock.set_value(i, 'DCLRDT', 1)

    # forwardfill for DIVAMT because $-Value per share of distribution has not only a monthly impact but is
    # rather a constant indicator, and at the end bfill the first row that was still empty
    df_stock['DIVAMT'] = df_stock['DIVAMT'].ffill()
    df_stock['DIVAMT'] = df_stock['DIVAMT'].bfill()

    # One datapoint was type string, short fix:
    s = df_stock['RETX']
    s = pd.to_numeric(s, errors='coerce')
    df_stock['RETX'] = s
    df_stock['RETX'] = df_stock['RETX'].bfill()


    # Drop a column if too many NaN or just considered unimportant
    df_stock = df_stock.drop('HSICMG', axis=1)  # has only values for JPM, NKE and CSCO makes no sense to include
    df_stock = df_stock.drop('SPREAD', axis=1)
    df_stock = df_stock.drop('TICKER', axis=1)  # drop the Tickers and created a dictionary with the PERMNO codes
    stock_dict = {10107: 'Microsoft Corporation',
                  11308: 'The Coca-Cola Co',
                  11850: 'Exxon Mobil Corporation',
                  12060: 'General Electric Company',
                  12490: 'IBM Common Stock',
                  14541: 'Chevron Corporation',
                  14593: 'Apple Inc.',
                  17830: 'United Technologies Corporation',
                  18163: 'Procter & Gamble Co',
                  18542: 'Caterpillar Inc.',
                  19561: 'Boeing Co',
                  20626: 'DOW Chemical Co',
                  21936: 'Pfizer Inc.',
                  22111: 'Johnson & Johnson',
                  22592: '3M Co',
                  22752: 'Merck & Co., Inc.',
                  26403: 'Disney Walt Co',
                  43449: 'MC Donalds Corp',
                  47896: 'JPMorgan Chase & Co',
                  55976: 'Wal Mart Stores Inc',
                  57665: 'Nike',
                  59176: 'American Express Co',
                  59328: 'Intel Corp',
                  59459: 'Travelers Companies Inc',
                  65875: 'Verizon Communications Inc',
                  66181: 'Home Depot Inc',
                  76076: 'Cisco Systems Inc',
                  86868: 'Goldman Sachs Group Inc',
                  92611: 'Visa Inc',
                  92655: 'UnitedHealth Group Inc'}

    # delete all rows that contain more than the specified number of NaN values,
    # please only use this as the last step and check the variable row_counter to see how many rows have been deleted
    thresh = 3
    row_counter = 0
    for row in df_stock.iterrows():
        if row[1].isnull().sum()>thresh:
            df_stock.drop(df_stock.index[int(row[0])], inplace=True)
            row_counter += 1
    # print(row_counter)
    # delete rows with 'tresh' NaN's
    df_stock = ra.delete_rows_by_threshold(df_stock, 3)

    df_stock['PERMNO'] = df_stock['PERMNO'].astype(str)
    print(df_stock.columns)
    df_stock = df_stock.drop('date', axis=1)
    df_stock = pd.get_dummies(df_stock)

    print(df_stock.head())

    return df_stock
