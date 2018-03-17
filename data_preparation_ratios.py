import pandas as pd
from Intro_to_Machine_Learning_Group_4 import data_preparation_ratios as ra


def delete_rows_by_threshold(df, thresh):
    faulty_rows = []
    for row in df.iterrows():
        if row[1].isnull().sum() >= thresh:
            faulty_rows.append(df.index[int(row[0])])
    return df.drop(faulty_rows)


def ratio_formatter():
    # load the csv file for the ratios data and store it as a dataframe
    df = pd.read_csv('ratio_version_one.csv')

    # ****************---------------***************-----------------*************-----------------
    #                       reformatting the dataframe ratios
    # ****************---------------***************-----------------*************-----------------

    # adate and qdate are redundant for our uses after closer inspection therefore we drop those columns
    # curr_ratio and inv_turn simply have to many missing values with whole companies not having any data,
    # that keeping the features can't be justified.
    df = df.drop(columns=['adate', 'qdate', 'curr_ratio', 'inv_turn'])

    # there are a few rows with lots of values missing, so we delete all rows more than 3 values missing
    df = delete_rows_by_threshold(df, 4)

    # dpr is missing for a small number of the first Visa values, we think a backwards fill is therefore adequate
    df['dpr'] = df['dpr'].bfill()

    # roe is missing for 3 quarters, upon inspection a backwards fill should be adequate
    df['roe'] = df['roe'].bfill()

    # capital ratio is still missing for the first few entries of MSF, next entries are 0 so just bfill
    df['capital_ratio'] = df['capital_ratio'].bfill()

    # all Nan of cash_debt are in Goldman Sachs, fill with median (is very near of the value prior to the Nan's
    # and fits into the pattern
    df['cash_debt'].fillna((df['capital_ratio'].mean()), inplace=True)

    # lt_ppent no data for Travelers companies found on wharton.
    # only source found on https://www.marketwatch.com/investing/stock/trv/profile but no time series
    # therefore just fill 1 so our algorithm won't be too strongly influenced
    df['lt_ppent'].fillna(1, inplace=True)

    # dltt_be bfill, fits into pattern very nicely
    df['dltt_be'] = df['dltt_be'].bfill()

    # for ptb there are a small number of values missing, all for the same company. As this ratio fluctuates
    # quite a bit, we feel filling with the average of the company is the best option
    df['ptb'].fillna(df.ptb.loc[df['permno'] == 19561].mean(), inplace=True)

    # PEG_1yrforward and PEG_ltgforward have a number of missing values with no pattern throughout the data set.
    # filling with the mean of the feature therefore seems adequate
    df['PEG_1yrforward'] = df['PEG_1yrforward'].fillna((df['PEG_1yrforward'].mean()))
    df['PEG_ltgforward'] = df['PEG_ltgforward'].fillna((df['PEG_ltgforward'].mean()))

    # ****************---------------***************-----------------*************-----------------
    #                       reformatting the dataframe stock
    # ****************---------------***************-----------------*************-----------------

    # fill all NaN values in the date columns with 0
    df['DCLRDT'] = df['DCLRDT'].fillna(0)
    df['PAYDT'] = df['PAYDT'].fillna(0)
    df['FACPR'] = df['FACPR'].fillna(0)
    df['FACSHR'] = df['FACSHR'].fillna(0)
    # next step is to fill the existing values in the date columns with a 1, therefore making it a binary variable
    # the dates are mostly somewhere in the middle of the month and because we utilize monthly data we just
    # indicate if for example a dividend was payed in that month
    for i, row in df.iterrows():
        if row['PAYDT'] != 0:
            df.set_value(i, 'PAYDT', 1)
        if row['DCLRDT'] != 0:
            df.set_value(i, 'DCLRDT', 1)

    # forwardfill for DIVAMT because $-Value per share of distribution has not only a monthly impact but is
    # rather a constant indicator, and at the end bfill the first row that was still empty
    df['DIVAMT'] = df['DIVAMT'].ffill()
    df['DIVAMT'] = df['DIVAMT'].bfill()

    # One datapoint was type string, short fix:
    s = df['RETX']
    s = pd.to_numeric(s, errors='coerce')
    df['RETX'] = s
    df['RETX'] = df['RETX'].bfill()

    # Drop a column if too many NaN or just considered unimportant
    df_stock = df.drop('HSICMG', axis=1)  # has only values for JPM, NKE and CSCO makes no sense to include
    df_stock = df.drop('SPREAD', axis=1)
    df_stock = df.drop('TICKER', axis=1)  # drop the Tickers and created a dictionary with the PERMNO codes
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
    # please only use this as the last step
    # delete rows with 'tresh' NaN's
    df = ra.delete_rows_by_threshold(df_stock, 3)

    p = df['PERMNO']
    d = df['date']
    df_stock = df_stock.drop('date', axis=1)

    df_stock['PERMNO'] = df_stock['PERMNO'].astype(str)
    df_stock = pd.get_dummies(df_stock)
    df_stock['date'] = d
    df_stock['permno'] = p

    return df
