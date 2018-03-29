import pandas as pd


def delete_rows_by_threshold(data_frame, threshold):
    faulty_rows = []
    for row in data_frame.iterrows():
        if row[1].isnull().sum() >= threshold:
            faulty_rows.append(data_frame.index[int(row[0])])
    return data_frame.drop(faulty_rows)


def clean_data():
    # Load the csv file for the ratios data and store it as a dataframe
    df = pd.read_csv('df.csv', delimiter=';')

    # ****************---------------***************-----------------*************-----------------
    #                                   Reformatting the dataframe
    # ****************---------------***************-----------------*************-----------------

    # adate and qdate are redundant for our uses after closer inspection therefore we drop those columns
    # curr_ratio and inv_turn simply have to many missing values with whole companies not having any data,
    # that keeping the features can't be justified.
    # HSICMG has only values for JPM, NKE and CSCO makes no sense to include.
    # FACPR and FACSHR have only two rows with a value that is not 0 and seem hardly significant.
    # date and permo are duplicate features due to the merging of two data sets and are redundant.
    df = df.drop(columns=['adate', 'qdate', 'curr_ratio', 'inv_turn', 'HSICMG', 'FACPR', 'FACSHR', 'SPREAD', 'TICKER', 'date', 'permno'])

    # dpr is missing for a small number of the first Visa values, we think a backwards fill is therefore adequate
    df['dpr'] = df['dpr'].bfill()

    # roe is missing for 3 quarters, upon inspection a backwards fill should be adequate
    df['roe'] = df['roe'].bfill()

    # pe_op_basic and pe_exi are missing for a entry, a backwards fill seems adequate
    df['pe_op_basic'] = df['pe_op_basic'].bfill()
    df['pe_exi'] = df['pe_exi'].bfill()

    # capital ratio is still missing for the first few entries of MSF, next entries are 0 so just bfill
    df['capital_ratio'] = df['capital_ratio'].bfill()

    # All NaN of cash_debt are in Goldman Sachs, fill with median (is very near of the value prior to the NaN's
    # and fits into the pattern)
    df['cash_debt'].fillna((df['capital_ratio'].mean()), inplace=True)

    # lt_ppent no data for Travelers companies found on wharton.
    # Only source found on https://www.marketwatch.com/investing/stock/trv/profile but no time series
    # therefore just fill 1 so our algorithm won't be too strongly influenced
    df['lt_ppent'].fillna(1, inplace=True)

    # dltt_be bfill, fits into pattern very nicely
    df['dltt_be'] = df['dltt_be'].bfill()

    # For ptb there are a small number of values missing, all for the same company. As this ratio fluctuates
    # quite a bit, we feel filling with the average of the company is the best option.
    df['ptb'].fillna(df.ptb.loc[df['PERMNO'] == 19561].mean(), inplace=True)

    # PEG_1yrforward and PEG_ltgforward have a number of missing values with no pattern throughout the data set.
    # Filling with the mean of the feature therefore seems adequate
    df['PEG_1yrforward'] = df['PEG_1yrforward'].fillna((df['PEG_1yrforward'].mean()))
    df['PEG_ltgforward'] = df['PEG_ltgforward'].fillna((df['PEG_ltgforward'].mean()))

    # Forward fill for DIVAMT because $-Value per share of distribution has not only a monthly impact but is
    # rather a constant indicator, and at the end bfill the first row that was still empty
    df['DIVAMT'] = df['DIVAMT'].ffill()
    df['DIVAMT'] = df['DIVAMT'].bfill()

    # One datapoint was type string, short fix:
    df['RETX'] = pd.to_numeric(df['RETX'], errors='coerce')
    df['RETX'] = df['RETX'].bfill()

    # ****************---------------***************-----------------*************-----------------
    #                                  Creating Dummy Date Variables
    # ****************---------------***************-----------------*************-----------------

    # We have a few variables indicating a specific date, like a dividend payout date.
    # We convert these two dummy variables to get rid of the massive amount of resulting NaN values.
    # First fill all NaN values in the date columns with 0:
    df['DCLRDT'] = df['DCLRDT'].fillna(0)
    df['PAYDT'] = df['PAYDT'].fillna(0)

    # Next step is to fill the existing values in the date columns with a 1, therefore making it a binary variable
    # the dates are mostly somewhere in the middle of the month and because we utilize monthly data we just
    # indicate if for example a dividend was payed in that month.
    for i, row in df.iterrows():
        if row['PAYDT'] != 0:
            df.at[i, 'PAYDT'] = 1
        if row['DCLRDT'] != 0:
            df.at[i, 'DCLRDT'] = 1

    df['PAYDT'] = pd.to_numeric(df['PAYDT'], errors='coerce')
    df['DCLRDT'] = pd.to_numeric(df['DCLRDT'], errors='coerce')

    # ****************---------------***************-----------------*************-----------------
    #                            Converting PERMNO Codes to Dummy Variables
    # ****************---------------***************-----------------*************-----------------

    # So the algorithms can differentiate the different companies, we have to convert
    # the PERMNO codes to dummy variables.
    d = df['public_date']
    df = df.drop('public_date', axis=1)
    df['PERMNO'] = df['PERMNO'].astype(str)
    df = pd.get_dummies(df)
    df['public_date'] = d

    # We can now rename all these columns to more usable names and move the Date column to the front.
    permno_codes = ['Microsoft', 'Coca_Cola', 'Exxon_Mobil', 'General_Electric', 'IBM', 'Chevron', 'Apple',
                    'United_Technologies', 'Procter_Gamble', 'Caterpillar', 'Boeing', 'DOW_Chemical', 'Pfizer',
                    'Johnson_Johnson', '3M', 'Merck', 'Disney', 'McDonalds', 'JPMorgan_Chase', 'Wal_Mart', 'Nike',
                    'American_Express', 'Intel', 'Travelers', 'Verizon', 'Home_Depot', 'Cisco', 'Goldman_Sachs',
                    'Visa', 'UnitedHealth']
    for i in range(0, 30):
        df.columns.values[i+35] = permno_codes[i]

    df.rename(columns={'public_date': 'Date'}, inplace=True)
    cols = list(df)
    cols.insert(0, cols.pop(cols.index('Date')))
    df = df.ix[:, cols]

    # there are a few rows left with lots of values missing, so we delete all rows with 6 or more values missing
    df = delete_rows_by_threshold(df, 6)

    return df
