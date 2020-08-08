#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 17:10:09 2020

@author: tim
"""

import requests
from scrapy import Selector
import pandas as pd


url = "http://case.doe.gov.bd/index.php?option=com_xmap&sitemap=1&Itemid=14"
#url = "http://case.doe.gov.bd/index.php?option=com_content&view=category&id=8&Itemid=32"
req = requests.get(url)
url_content = req.content
sel = Selector(text=url_content)
course_blocks = sel.xpath('//a[contains(@href,"aqi-archives")]')
course_links = course_blocks.xpath('@href')
var = course_blocks.xpath('text()').extract()

url = ''.join(['http://case.doe.gov.bd/', course_links.extract_first()])
print(url)
req = requests.get(url)
url_content = req.content
sel2 = Selector(text=url_content)
date = sel2.xpath('//span[contains(., "Date")]')
data_table = sel2.xpath('//table[@class="mceItemTable"]')
df = pd.read_html(data_table.extract_first())[0]

