import os
import pandas as pd
import requests

from datetime import datetime, timedelta

from ep.config import *


def getDateObject(month_number, year_number):
    return datetime.strptime(str(month_number) + str(year_number), "%m%Y")


def get_dataframes():
    interest_dataframes = {}

    for interest in interest_tickers.keys():
        with open('csv/{}.csv'.format(interest), 'rb') as f:
            df = pd.read_csv(f, index_col=0, header=0)
            df.columns = pd.to_datetime(df.columns)
            interest_dataframes[interest] = df
    return interest_dataframes


def getFileName(datetime_object):

    month_name = datetime_object.strftime("%b").lower()
    year_name = datetime_object.strftime("%y")

    file_suffix = 'xlsx' if datetime_object >= START_TO_USE_XSLX else 'xls'

    file_name = month_name + year_name + '_base.' + file_suffix

    return file_name

def getFile(file_name, download=False):
    file_path = 'resources/{}'.format(file_name)

    if download:
        url = URL_BASE.format(file_name)

        print('Getting {} ...'.format(file_name))
        resp = requests.get(url)

        print('Writing {} ...'.format(file_name))
        with open(file_path, 'wb') as f:
            f.write(resp.content)
        print('Writing to {} complete'.format(file_name))

    return file_path


def get_sheet_name(datetime_object):
    if datetime_object >= NEW_FORMAT_START_DATE:
        return '2tab'
    elif datetime_object >= datetime.strptime("200508", "%Y%m"):
        return ' Prices US'
    else:
        return 'All Prices'

def update_dataframes_with_file(f, datetime_object, year, month, interest_dataframes):
    xl = pd.ExcelFile(f)
    sheet_name = get_sheet_name(datetime_object)

    tb = pd.read_excel(xl, sheet_name, index_col=0)

    look_back_years = 4 if datetime_object >= NEW_FORMAT_START_DATE else 3

    for interest, ticker in interest_tickers.items():
        if ticker not in tb.index:
            continue

        interest_data = tb.loc[ticker][1:]

        sdt = datetime(year=year - look_back_years, month=1, day=1)
        edt = datetime(year=year + 1, month=12, day=1)
        cdt = datetime(year=year, month=month + 1, day=1)

        indexes = pd.date_range(start=sdt, end=edt, freq='MS')

        interest_data.index = indexes


        interest_data.name = cdt
        df = pd.DataFrame([interest_data])

        master_df = interest_dataframes[interest]
        interest_dataframes[interest] = master_df.combine_first(df)
    return interest_dataframes

def getLastDayPreviousMonth():
    return datetime.today().replace(day=1) - timedelta(days=1)

def get_new_dataframes():
    interest_dataframes = {}
    for key in interest_tickers.keys():
        interest_dataframes[key] = pd.DataFrame()
    return interest_dataframes

def write_dataframes_to_csv(interest_dataframes):
    for interest, dataframe in interest_dataframes.items():
        with open('csv/{}.csv'.format(interest), 'w') as f:
            dataframe.to_csv(f)

def setupDirectories():

    for dir in (RESOURCE_DIR, CSV_DIR):
        if not os.path.exists(dir):
            print('Creating {} directory..')
            os.makedirs(dir)
