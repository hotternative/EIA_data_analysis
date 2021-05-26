import matplotlib.pyplot as plt
import pandas as pd

from ep.utils import get_dataframes


def is_last_index_actual(last_index, col):
    last_index = pd.to_datetime(last_index)
    return last_index > col

def find_forecast_error(idx, df):

    cur_month = pd.to_datetime(idx)

    error_usd = []
    error_percentage = []

    # for each row in the dataframe, find the actual and the prediction for time horizons from 1 month to 12 months
    for months in range(12):
        col = cur_month + pd.DateOffset(months=months)
        data_in_a_month = df[col]

        # It's observed that actual price can be modified after some time,
        # hence we use the latest available actual price rather that the first actual price
        last_index = data_in_a_month.last_valid_index()
        is_actual = is_last_index_actual(last_index, col)
        actual = data_in_a_month[last_index] if is_actual else None

        prediction = data_in_a_month[idx]

        error_in_usd = (actual - prediction) if actual else None
        error_usd.append(error_in_usd)

        error_percent = (actual - prediction) / prediction * 100 if actual else None
        error_percentage.append(error_percent)

    return error_usd, error_percentage

def analyze_dataframe(df):

    usd_df = pd.DataFrame(columns=range(1,13))
    percent_df = pd.DataFrame(columns=range(1, 13))

    for row in df.iterrows():
        idx = row[0]

        error_usd, error_percent = find_forecast_error(idx, df)

        forecast_error_in_usd = pd.Series(error_usd, index=range(1,13), name=idx)
        forecast_error_percent = pd.Series(error_percent, index=range(1,13), name=idx)

        usd_df = usd_df.append(forecast_error_in_usd)
        percent_df = percent_df.append(forecast_error_percent)

    return usd_df, percent_df


def analyze_all(save_files=False):
    interest_dataframes = get_dataframes()

    for interest, df in interest_dataframes.items():
        print('Analyzing {} dataframe..'.format(interest))

        usd_df, percent_df = analyze_dataframe(df)

        if save_files:
            with open('error_csv/{}_usd.csv'.format(interest), 'w') as f:
                usd_df.to_csv(f)
            with open('error_csv/{}_percent.csv'.format(interest), 'w') as f:
                percent_df.to_csv(f)


def analysis_demo1(interest='WTI', time_horizon=12):
    # Plot out the forecast error in percentage for
    # a given interest and a given time horizon

    interest_dataframes = get_dataframes()
    df = interest_dataframes[interest]
    usd_df, percent_df = analyze_dataframe(df)

    ax = percent_df[time_horizon].plot()
    ax.axhline(0, color="red", linestyle="--")
    ax.grid()

    title = "{} {} month forecast error in percentage".format(interest, time_horizon)
    plt.title(title)
    plt.show(block=True)

def analysis_demo2(interest='WTI'):
    # Find the mean absolute error in USD for each time horizon for a given interest
    interest_dataframes = get_dataframes()
    df = interest_dataframes[interest]
    usd_df, percent_df = analyze_dataframe(df)
    usd_df = abs(usd_df)
    m = usd_df.mean()
    ax = m.plot()
    ax.grid()
    plt.show(block=True)


# analysis_demo1()
analysis_demo2()