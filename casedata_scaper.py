#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 16:40:49 2020.

@author: tim
"""
import scrapy
from scrapy.crawler import CrawlerProcess
import pandas as pd

# Create the Spider class
class CaseSpider(scrapy.Spider):
    def start_requests( self ):
        yield scrapy.Request(url=url, callback=self.parse_front)

    # First parsing method
    def parse_front(self, response):
        course_blocks = response.xpath('//tr[contains(@class,"sectiontableentry")]/td')
        links_to_follow = course_blocks.xpath('./a/@href').extract()
        dates = course_blocks.xpath('./a/text()').extract()
        for url, date in zip(links_to_follow, dates):
            date = date.strip()[24:]
            yield response.follow(url = url, callback = self.parse_pages, meta={'date':date})
    
    # Second parsing method
    def parse_pages(self, response):
        data_table = response.xpath('//table[@class="mceItemTable"]')
        df = pd.read_html(data_table.extract_first())[0]
        date = response.meta['date'].replace('/','-')
        df.to_csv(date+'.csv')

url = "http://case.doe.gov.bd/index.php?option=com_content&view=category&id=8&Itemid=32"

# Run the Spider
process = CrawlerProcess()
process.crawl(CaseSpider)
process.start()
