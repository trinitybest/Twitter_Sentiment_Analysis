"""
Author: TH
Date: 14/07/2016
Collect all the slang from http://www.noslang.com/dictionary/
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd 
import string
from urllib.parse import urljoin

def get_list_of_slang():
    df = pd.DataFrame(columns = ['term', 'definition'])
    for c in string.ascii_lowercase:
        print("Downloading slang {0}.".format(c))
        page = requests.get(urljoin("http://www.noslang.com/dictionary/", c))
        soup = BeautifulSoup(page.content, "html.parser")
        table = soup.find_all("table")[1]
        dts = soup.find_all("dt")
        for dt in dts:
            term = dt.find_all("a")[0].get("name")
            definition = dt.find_all("abbr")[0].get("title")
            #print(term, definition)
            df = df.append({"term": term, "definition": definition}, ignore_index = True)
        #print(df)

    df.to_csv("CSV/list_of_slang.csv", encoding="utf-8", index = False)
    print("Successfully downloaded slang.")
    return df

if __name__ == "__main__":
    get_list_of_slang()
