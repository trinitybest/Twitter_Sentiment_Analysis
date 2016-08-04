"""
Author: TH
Date: 04/08/2016
"""

import pymssql
import yaml


query  = "SELECT TOP 1000 * FROM dbo.Twitter_Tweets"
keys = yaml.load(open('keys.yaml', 'r'))
server = keys['server']
user = keys['user']
password = keys['password']
database = keys['database']
conn = pymssql.connect(server, user, password, database)
cursor = conn.cursor(as_dict = True)
cursor.execute(query)


