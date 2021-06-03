"""
This script processes the US embassy data for Dhaka in preparation for visuals. 

In practice it concatenates all the data files (each full year + most recent year + 
most recent month's data) into one data file. 

"""


import pandas as pd
from pathlib import Path
from datetime import datetime

def format_todays_month(todays_date):
    """Returns current month as two digit string e.g. '05' for May & '02' for Feb."""
    return str(f'{todays_date.month:02d}')


def combine_data_files(todays_date, data_files_path):
    """
    Combines the data files for all previous full years with current year and
    current month. 

    Parameters
    ----------
    todays_date : datetime object
        The date when run.
    data_files_path : PosixPath object
        The filepath where the data is stored.

    Returns
    -------
    df : TYPE
        DESCRIPTION.

    """
    current_month = format_todays_month(todays_date)
    df = pd.concat([pd.read_csv(data_files_path.joinpath(f'Dhaka_PM2.5_{year}_YTD.csv'), 
                                parse_dates=['Date (LT)'], 
                                index_col='Date (LT)') 
                    for year in list_of_years])
    df = pd.concat([df, 
                    pd.read_csv(data_files_path.joinpath(f'Dhaka_PM2.5_{current_year}_{current_month}_MTD.csv'), 
                                parse_dates=['Date (LT)'], 
                                index_col='Date (LT)')])
    return df


todays_date = datetime.today()
current_year = todays_date.year


data_files_path = Path.cwd().joinpath('data', 'bronze', 'us_embassy')

list_of_years = [*range(2016, current_year+1)]

df = combine_data_files(todays_date, data_files_path)

# Makes use of the quality control flag and removes invalid data
df_valid = df[df['QC Name']=='Valid']

# An additional quality control step removes negative AQI values which aren't valid.
df_valid = df_valid[df_valid['AQI']>0]

output_file = Path.cwd().joinpath('data', 
                                  'silver', 
                                  'us_embassy', 
                                  'collated_dhaka_air_data.csv')

df_valid.to_csv(output_file)



