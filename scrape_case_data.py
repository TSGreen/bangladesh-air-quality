"""
Script for web scraper to crawl through CASE (Govt of Bangladesh) data archive.

Data archive found at: https://bit.ly/31t9vxr
Leading to html table of a day's data (for example: https://bit.ly/3a5DYWc)

Data is avaiable from February 2014, but is not exhaustive, with some dates
missing data. Also different dates have different locations available.
Care needed when concatenating the daily figures.

Script returns a dataframe version of each day's data.

Updated (06/21) to only scrape dates after the most scrapping date.

Created August 2020.
Updated June 2021
@author: Timothy Green

"""

import scrapy
from scrapy.crawler import CrawlerProcess
import pandas as pd
from pathlib import Path
from datetime import datetime
import re


def return_formated_date(date):
    """Return date string as datetime."""
    date = date.split('/')
    if len(date[2])==2:
        date[2] = '20'+date[2]
    date = '/'.join(date)
    return datetime.strptime(date, '%d/%m/%Y')


class CaseSpider(scrapy.Spider):
    """
    Web scraper to crawl through CASE AQI data archive.

    Links for daily data are extracted from the data archive page in first
    parse as well as the date information.
    HTML data table extracted for each day during second parse and converted
    to pandas dataframe.
    """

    name = 'CASE_spider'

    def start_requests(self):
        """Enter the desired webpage."""
        yield scrapy.Request(url=url, callback=self.parse_front)

    def parse_front(self, response):
        """First parsing to retrieve link to each daily data page."""
        html_blocks = response.xpath('//a[contains(@href,"aqi-archives")]')
        links_to_follow = html_blocks.xpath('@href').extract()
        descriptions = html_blocks.xpath('text()').extract()
        for url, text in zip(links_to_follow, descriptions):
            date_list = re.findall('[0-9]+/[0-9]+/[0-9]+', text)
            if date_list:
                date = date_list[0]
            else:
                date = re.findall('[0-9]+.[0-9]+.[0-9]+', text)[0]
                date = date.replace('.', '/')
            date_formatted = return_formated_date(date)
            if date_formatted > last_scraped:
                yield response.follow(url=url,
                                      callback=self.parse_pages,
                                      meta={'date': date})

    def parse_pages(self, response):
        """Second parsing to extract data table and convert to dataframe."""
        data_table = response.xpath('//table[@class="mceItemTable"]')
        df = pd.read_html(data_table.extract_first(), header=0, index_col=0)[0]
        date = response.meta['date'].replace('/', '-')
        df = pd.concat({date: df}, names=['Date'])
        if datafile.exists():
            df.to_csv(datafile, mode='a', header=False)
        else: 
            df.to_csv(datafile)


url = "http://case.doe.gov.bd/index.php?option=com_xmap&sitemap=1&Itemid=14"

datafile = Path.cwd().joinpath('data', 'bronze', 'case', 'case_data.csv')
if datafile.exists():
    df = pd.read_csv(datafile)
    df['Date'] = pd.to_datetime(df['Date'], 
                                errors='coerce', 
                                dayfirst=True)
    last_scraped = df.Date.max()
    #os.remove(datafile)

# Run the Spider
process = CrawlerProcess()
process.crawl(CaseSpider)
process.start()
