"""
Author: TH
Date: 04/08/2016
"""

import pyodbc
import yaml
import pickle
from process_twitter import process_tweet, extract_features_3


def strip_non_ascii(string):
    ''' Returns the string without non ASCII characters'''
    stripped = (c for c in string if 0 < ord(c) < 127)
    return ''.join(stripped)

# query to run
query  = "SELECT TOP 1 * FROM dbo.Twitter_Tweets"
# database connection string
keys = yaml.load(open('keys.yaml', 'r'))
server = keys['server']
user = keys['user']
password = keys['password']
database = keys['database']
conn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+user+';PWD='+password)
cursor = conn.cursor()
cursor.execute(
"""
SELECT * 
FROM dbo.Twitter_Tweets
WHERE 
(HashTags LIKE '%#AAPL%'
OR HashTags LIKE '%GOOG%'
OR HashTags LIKE '%GOOGL%'
OR HashTags LIKE '%MSFT%'
OR HashTags LIKE '%BRK.A%'
OR HashTags LIKE '%BRK.B%'
OR HashTags LIKE '%XOM%'
OR HashTags LIKE '%FB%'
OR HashTags LIKE '%JNJ%'
OR HashTags LIKE '%GE%'
OR HashTags LIKE '%AMZN%'
OR HashTags LIKE '%WFC%')
AND CreatedAt > '2015-12-31 00:00:00.0000000'
""")
rows = cursor.fetchall()
print(len(rows))
# load featureList 
load_featureList = open("pickled/v1/featureList_2_ways.pickle", "rb")
featureList = pickle.load(load_featureList)
load_featureList.close()
# load LinearSVC_classifier
load_LinearSVC_classifier = open("pickled/v1/LinearSVC_classifier_2_ways.pickled", "rb")
LinearSVC_classifier = pickle.load(load_LinearSVC_classifier)
load_LinearSVC_classifier.close()

"""
Tweet5 = "øΩ Vintage GE Motors Ashtray  #vintage #GE #mantique http://etsy.me/1ev70Qw pic.twitter.com/Duztcj7xUj"
Tweet5 = strip_non_ascii(Tweet5)
print(Tweet5)
print(LinearSVC_classifier.classify(extract_features_3(featureList, process_tweet(Tweet5))))
"""
count = 0
for row in rows:
    #print('-------------------------------------------------')
    #print(row.TweetId, row.Text)
    count += 1
    if count % 1000 == 0:
        print(count)
    try:
        classified_sentiment = LinearSVC_classifier.classify(extract_features_3(featureList, process_tweet(row.Text)))
        #print("classified_sentiment", classified_sentiment)
        update_query = "UPDATE dbo.Twitter_Tweets SET Sentiment=? WHERE TweetId = ?"
        cursor.execute(update_query, [classified_sentiment, row.TweetId])
        conn.commit()
    except Exception as e1:
        #print(1, e1)
        try:
            classified_sentiment = LinearSVC_classifier.classify(extract_features_3(featureList, process_tweet(strip_non_ascii(row.Text))))
            #print("classified_sentiment", classified_sentiment)
            update_query = "UPDATE dbo.Twitter_Tweets SET Sentiment=? WHERE TweetId = ?"
            cursor.execute(update_query, [classified_sentiment, row.TweetId])
            conn.commit()
        except Exception as e2:
            print(2, e2)



