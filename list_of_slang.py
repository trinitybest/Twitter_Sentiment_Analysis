"""
Author: TH
Date: 14/07/2016
Collect all the slang from http://www.noslang.com/dictionary/
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd 

page = requests.get("http://www.noslang.com/dictionary/a/")
soup = BeautifulSoup(page.content, "html.parser")
#print(soup)
table = soup.find_all("table")[1]
#print(table)
dts = soup.find_all("dt")
for dt in dts:
    print(dt)

