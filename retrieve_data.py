"""
Check whether latest data is avaiable locally and download latest data from
web if not.

The air quality data archive is structured with:
  - Complete annual data for previous years stored in ..<year>_YTD.. files
  - Current year's data stored in ..<current year>_YTD.. file up to beginning
    of current month.
  - Current month data is stored in ..<month>_MTD.. file.

This code checks whether latest monthly data file is stored locally. If not,
then it downloads the latest monthly data file and latest annual data file.
If latest month's file exists, the code checks whether the latest date in that
file is within 48 hours of the current date. If not, the monthly data file is
updated by downloading latest monthly data file. 
"""

from datetime import date
from pathlib import Path
import pandas as pd
import requests

def download_files(baseurl, filename, output):
    """
    Download requested file.

    Parameters
    ----------
    baseurl : str
        The base url path of the file to be downloaded.
    filename : str
        The name of the specific file to download.
    output : PosixPath
        The full filepath for destination for downloaded file.

    Returns
    -------
    None.

    """
    url = baseurl+filename
    req = requests.get(url)
    url_content = req.content
    with open(output, 'wb') as f:
        print("Downloaded file:", filename)
        f.write(url_content)


today = date.today()
day = today.day
month = str(f'{today.month:02d}')
year = str(today.year)

monthfilename = ''.join(['Dhaka_PM2.5_2020_', month, '_MTD.csv'])
monthfilepath = Path.cwd().joinpath('data', monthfilename)

yearfilename = ''.join(['Dhaka_PM2.5_', year, '_YTD.csv'])
yearfilepath = Path.cwd().joinpath('data', yearfilename)

base_url = 'http://dosairnowdata.org/dos/historical/Dhaka/2020/'

if monthfilepath.exists():
    print(f"Latest monthy data file exists. Checking data in {monthfilename} ..")
    df = pd.read_csv(monthfilepath)
    latest_day = int(df.Day.tail(1))
    if latest_day < (day-2):  # measurements appear to be uploaded within 48 hours
        print('More recent data is available online. Beginning download:')
        download_files(base_url, monthfilename, monthfilepath)
    else:
        print('Local data files are up to date.')
else:
    print("Latest monthly data file does not exist.\nDownloading latest data files..")
    download_files(base_url, monthfilename, monthfilepath)
    download_files(base_url, yearfilename, yearfilepath)
