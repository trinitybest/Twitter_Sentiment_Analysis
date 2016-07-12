"""
Author: TH
Date: 12/07/2016
Read from wikipedia page and get a list of emoticons with their meaning.
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

def get_list_of_emoticons():
	# Define the dataframe to store the list of emoticons table.
	df = pd.DataFrame(columns = ['Icon', 'Meaning']) 
	url = "https://en.wikipedia.org/wiki/List_of_emoticons"
	page = requests.get(url)
	soup = BeautifulSoup(page.content, 'html.parser')
	table = soup.find_all("table",{"class":"wikitable"})[0]
	rows = table.find_all("tr")
	for row in rows:
		columns = row.find_all("td")
		if columns:
			icon = columns[0].text
			meaning = columns[1].text
			meaning = re.sub(r'\W\d+\W',' ', meaning)
			#print("{0}, {1}".format(icon, meaning))
			df = df.append({'Icon': icon, 'Meaning': meaning}, ignore_index = True)
	print(df)
	df.to_csv('CSV/test.csv', encoding='utf-8', index=False)
	return df


if __name__ == '__main__':
	get_list_of_emoticons()
	df2 = pd.read_csv('CSV/test.csv')
	print(df2)




















