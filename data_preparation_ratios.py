import pandas as pd


def delete_rows_by_threshold(df, thresh):
    faulty_rows = []
    for row in df.iterrows():
        if row[1].isnull().sum() >= thresh:
            faulty_rows.append(df.index[int(row[0])])
    return df.drop(faulty_rows)


def ratio_formatter():
    # load the csv file for the ratios data and store it as a dataframe
    df_ratio = pd.read_csv('ratio_version_one.csv')

    # ****************---------------***************-----------------*************-----------------
    #                       reformatting the dataframe stock
    # ****************---------------***************-----------------*************-----------------

    # adate and qdate are redundant for our uses after closer inspection therefore we drop those columns
    # curr_ratio and inv_turn simply have to many missing values with whole companies not having any data,
    # that keeping the features can't be justified.
    df_ratio = df_ratio.drop(columns=['adate', 'qdate', 'curr_ratio', 'inv_turn'])

    # there are a few rows with lots of values missing, so we delete all rows more than 3 values missing
    df_ratio = delete_rows_by_threshold(df_ratio, 4)

    # dpr is missing for a small number of the first Visa values, we think a backwards fill is therefore adequate
    df_ratio['dpr'] = df_ratio['dpr'].bfill()

    # roe is missing for 3 quarters, upon inspection a backwards fill should be adequate
    df_ratio['roe'] = df_ratio['roe'].bfill()

    # capital ratio is still missing for the first few entries of MSF, next entries are 0 so just bfill
    df_ratio['capital_ratio'] = df_ratio['capital_ratio'].bfill()

    # all Nan of cash_debt are in Goldman Sachs, fill with median (is very near of the value prior to the Nan's
    # and fits into the pattern
    df_ratio['cash_debt'].fillna((df_ratio['capital_ratio'].mean()), inplace=True)

    # lt_ppent no data for Travelers companies found on wharton.
    # only source found on https://www.marketwatch.com/investing/stock/trv/profile but no time series
    # therefore just fill 1 so our algorithm won't be too strongly influenced
    df_ratio['lt_ppent'].fillna(1, inplace=True)

    # dltt_be bfill, fits into pattern very nicely
    df_ratio['dltt_be'] = df_ratio['dltt_be'].bfill()

    # for ptb there are a small number of values missing, all for the same company. As this ratio fluctuates
    # quite a bit, we feel filling with the average of the company is the best option
    df_ratio['ptb'].fillna(df_ratio.ptb.loc[df_ratio['permno'] == 19561].mean(), inplace=True)

    # PEG_1yrforward and PEG_ltgforward have a number of missing values with no pattern throughout the data set.
    # filling with the mean of the feature therefore seems adequate
    df_ratio['PEG_1yrforward'] = df_ratio['PEG_1yrforward'].fillna((df_ratio['PEG_1yrforward'].mean()))
    df_ratio['PEG_ltgforward'] = df_ratio['PEG_ltgforward'].fillna((df_ratio['PEG_ltgforward'].mean()))

    return df_ratio
