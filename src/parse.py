from ep.utils import *


def first_run(download=False):
    """
    Create csv files from stratch

    :param download: boolean.
        Set to False if files have been downloaded and saved to ./resources
        Set to True to download files from EIA website
    """
    setupDirectories()
    interest_dataframes = get_new_dataframes()

    for year in range(2005, END_YEAR+1):
        for month in range(12):

            datetime_object = getDateObject(month+1, year)
            file_name = getFileName(datetime_object)

            if datetime_object <= getLastDayPreviousMonth():
                print('Processing {}..'.format(file_name))
                file = getFile(file_name, download=download)

                with open(file, 'rb') as f:
                    interest_dataframes = update_dataframes_with_file(f, datetime_object, year, month, interest_dataframes)

    write_dataframes_to_csv(interest_dataframes)


def update(year, month, download):
    """
    Assuming an analyst or an automated process has identified a new file published on EIA

    Assuming existing CSVs are saved in ./csv/, this function updates all csv
    files with a new EIA file identified by the year and month parameter


    :param year: int, year of the new file, e.g. 2021
    :param month: int, month of the new file, between 1-12
    :param download: bool
        True to download from EIA
        False to find file already downloaded into ./resources/

    e.g. If apr21_base.xlsx is identified, year will be 2021, month will be 4
    """
    datetime_object = getDateObject(month, year)

    if datetime_object >= datetime.today():
        raise(ValueError(
            'Cannot download file for {}. '
            'Check the input year and month'.format(datetime_object)))

    file_name = getFileName(datetime_object)
    file = getFile(file_name, download=download)
    interest_dataframes = get_dataframes()

    with open(file, 'rb') as f:
        interest_dataframes = update_dataframes_with_file(f, datetime_object, year, month-1, interest_dataframes)

    write_dataframes_to_csv(interest_dataframes)

def main():

    # Run first_run function to build CSV files from stratch
    # first_run()

    # Run update function to update the existing CSV files with a new EIA file
    # update(year=2021, month=4, download=False)

    pass







