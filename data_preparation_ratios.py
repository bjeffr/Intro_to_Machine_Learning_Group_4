import pandas as pd


def delete_rows_by_threshold(df, thresh):
    faulty_rows = []
    for row in df.iterrows():
        if row[1].isnull().sum() >= thresh:
            faulty_rows.append(df.index[int(row[0])])
    return df.drop(faulty_rows)


def ratio_formatter():
    # Load the csv file for the ratios data and store it as a dataframe
    df_ratio = pd.read_csv('ratio_version_one.csv')


    # ****************---------------***************-----------------*************-----------------
    #                       reformatting the dataframe stock
    # ****************---------------***************-----------------*************-----------------

    # adate and qdate are redundant for our uses after closer inspection therefore we drop those columns
    df_ratio = df_ratio.drop(columns=['adate', 'qdate'])

    # there are a few rows with lots of values missing, so we delete all rows more than 3 values missing
    df_ratio = delete_rows_by_threshold(df_ratio, 4)

    # dpr is missing for a small number of the first Visa values, we think a backwards fill is therefore adequate
    df_ratio['dpr'] = df_ratio['dpr'].bfill()

    # roe is missing for 3 quarters, upon inspection a backwards fill should be adequate
    df_ratio['roe'] = df_ratio['roe'].bfill()

    # capital ratio is still missing for the first few entries of MSF, next entries are 0 so just bfill
    df_ratio['capital_ratio'] = df_ratio['capital_ratio'].bfill()

    # All Nan of cash_debt are in Goldman Sachs, fill with median (is very near of the value prior to the Nan's
    # and fits into the pattern
    df_ratio['cash_debt'].fillna((df_ratio['capital_ratio'].mean()), inplace=True)

    # lt_ppent no data for Travelers companies found on wharton.
    # only source found on https://www.marketwatch.com/investing/stock/trv/profile but no time series
    # therefore just fill 0 so our algorithm won't be too strongly influenced
    df_ratio['lt_ppent'].fillna(0, inplace=True)

    # dltt_be bfill, fits into pattern very nicely
    df_ratio['dltt_be'] = df_ratio['dltt_be'].bfill()

    # deleting outlier
    for i , n in df_ratio['inv_turn'].iteritems():
        if n > 1000:
            df_ratio.set_value(i, 'inv_turn', 0)

    print(df_ratio.set_index('permno'))


    # print(df_ratio.isnull().sum())
    return df_ratio


ratio_formatter()
