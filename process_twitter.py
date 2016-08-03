"""
Author: TH
Date: 15/07/2016
"""
import re
import nltk
from nltk.tokenize import StanfordTokenizer 
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from nltk.stem import PorterStemmer
import string
import csv
import pandas as pd
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.svm import SVC, LinearSVC, NuSVC
import pickle
import pandas as pd

df = pd.read_csv("DAL/DAL-Full-List.csv")
#print(df)

def process_tweet(tweet):
    """ pre-process the tweets:
        a)replace all the emoticons with a their sentiment po- larity by looking up the emoticon dictionary
        b)replace all URLs with a tag ||U||
        c)replace all nega- tions (e.g. not, no, never, n’t, cannot) by tag “NOT”
        d)replace targets (e.g. “@John”) with tag ||T|| 
        e)replace a sequence of repeated characters by three characters, for example, convert coooooooool to coool. 
        we add the f) step
        f)replace $cashtag with tag ||T|| and remove # for hashtags
    """
    # step a to be continued
    pre_process_a = tweet
  
    pre_process_b = re.sub(r"((www\.[^\s]+)|(https?://[^\s]+))", "||U||", pre_process_a)    
    pre_process_c = re.sub(r"\s[N|n][O|o][T|t]|\s[N|n][O|o]\s|\snever\s|\sNEVER\s|[N|n]'[T|t]|cannot|CANNOT", " NOT ", pre_process_b)
    pre_process_d = re.sub(r'@[^\s]+', "||T||", pre_process_c)
    pre_process_e = re.sub(r"([a-z|A-Z])\1{3,20}", r'\1\1\1', pre_process_d)
    #pre_process_f = re.sub(r"(#[^\s]+)|(\$[^\s]+)","||T||",pre_process_e)
    pre_process_f = re.sub(r"(\$[^\s\d]+)","||T||",pre_process_e)
    # Get all the hastags
    hashtags = re.findall(r"#([^\s]+)", pre_process_f)
    pre_process_f = re.sub(r"#([^\s]+)",lambda pat: pat.group(1).lower() ,pre_process_f)

    tweet = pre_process_f
    
    """ process the tweets
        a) tokenize the tweets using Stanford tokenizer
        b) identify stop words
        c) English words in WordNet(Fell- baum, 1998)
        d) identify punctuation (Penn Treebank)
    """
    ps = PorterStemmer()
    #lists to save stop words, english words, punctuation marks and captalized words.
    stop_words_in_tweet = []
    english_words_in_tweet = []
    punctuation_marks_in_tweet = []
    capitalized_words_in_tweet = []
    # feature vector after the words has been stemmed.
    featureVector_stem = []
    # feature vector of original words
    featureVector_full = []
    UandT = []
    num_twitter_tags = 0
    num_exclamation_marks = 0
    num_negations = 0
    f1 = 0
    f2 = 0
    f3 = 0
    f4 = 0
    f5 = 0 
    f6 = 0
    f7 = 0
    f8 = 0
    f9 = 0
    f10 = 0
    f11 = 0
    # Tokenize the tweet using Stanford Tokenizer.
    tokenized_tweet = StanfordTokenizer().tokenize(tweet)
    all_tokens = list(tokenized_tweet)
    # Get the stop words in english.
    stop_words = set(stopwords.words('english'))
    # Get a list of punctuation. 
    punct = list(string.punctuation)
    punct.append('-LRB-')
    punct.append('-RRB-')
    punct.append('-LCB-')
    punct.append('-RCB-')
    
    #print(tokenized_tweet)
    pos_tag_t = nltk.pos_tag(all_tokens)
    #print(pos_tag_t) 
    #for tag in pos_tag_t:
        #print(tag)


    
    # Count Tags
    for tag in pos_tag_t:
        word = tag[0]
        if word =='U' or word=='T':
            num_twitter_tags += 1
            UandT.append(tag)
            pos_tag_t[pos_tag_t.index(tag)]=('','')
            #tokenized_tweet[tokenized_tweet.index(word)] =''
    f7 = len(hashtags) + num_twitter_tags
    # Get stop words and puncts
    for tag in pos_tag_t:
        word = tag[0]
        if word in stop_words:
            stop_words_in_tweet.append(tag)
            pos_tag_t[pos_tag_t.index(tag)]=('','')
            #tokenized_tweet[tokenized_tweet.index(word)] =''
        if word in punct:
            punctuation_marks_in_tweet.append(tag)
            if word == '!':
                num_exclamation_marks += 1
            pos_tag_t[pos_tag_t.index(tag)]=('','')
            #tokenized_tweet[tokenized_tweet.index(word)] =''
    # Get negations, english words and captilized words
    for tag in pos_tag_t:
        word = tag[0]
        if re.search(r"^[0-9]*$", word):
            pass
        elif len(wn.synsets(word)) >0:
            if word == 'NOT':
                num_negations += 1
            else:
                english_words_in_tweet.append(tag)
                if word[0].isupper() and len(word)>1:
                    capitalized_words_in_tweet.append(tag)
            pos_tag_t[pos_tag_t.index(tag)]=('','')
            #tokenized_tweet[tokenized_tweet.index(word)] =''
    # Remove empty strings from the list and get remaining tokens without duplication
    """
    seen = set()
    other_tokens_in_tweet = []
    for item in pos_tag_t:
        if item[0]:
            if item not in seen:
                seen.add(item)
                other_tokens_in_tweet.append(item)
    """ 

    other_tokens_in_tweet = []
    for item in pos_tag_t:
        if item[0]:
            other_tokens_in_tweet.append(item)   

    for w in english_words_in_tweet + other_tokens_in_tweet + UandT:
        #check if the word stats with an alphabet
        val = re.search(r"^[a-zA-Z][a-zA-Z0-9]*$", w[0])
        if val is None:
            continue
        else:
            # change all the feature vector to lower case
            featureVector_full.append(w[0].lower())
            featureVector_stem.append(ps.stem(w[0].lower()))
    #print(nltk.pos_tag(['full']))
    # Check the polarity of features using DAL and WordNet
    sentiment_features = []
    # remove tokens with digits and change words to lowers case
    for tag in english_words_in_tweet + other_tokens_in_tweet:
        if bool(re.search(r'\d', tag[0])) == False:
            tmp = (tag[0].lower(), tag[1])
            sentiment_features.append(tmp)
    print(sentiment_features)
    polar_tokens = []
    non_polar_tokens = []
    for tag in sentiment_features:
        #print(feature)
        polar = None
        word = tag[0]
        print(tag)
        print(word in df.word.values)
        if word in df.word.values:
            #print(df.loc[df['word']==feature].iloc[0]['Pleasantness'])
            polar = 1
            polar_tokens.append(tag)
            #print(word)
            pleasant = df.loc[df['word']==word].iloc[0]['Pleasantness']

            if tag[1] == 'JJ' or tag[1] == 'RB' or tag[1] == 'VB' or tag[1] == 'NN':
                print(tag)
                print(pleasant)
                if pleasant/3<0.5 or pleasant/3>0.8:
                    f1 += 1

        elif len(wn.synsets(word)) >0:
            flag = 1
            for syn in wn.synsets(word):
                for l in syn.lemmas():
                    #print('--------------',l.name())
                    if l.name() in df.word.values:
                        #print(df.loc[df['word']==l.name()].iloc[0]['Pleasantness'])
                        pleasant = df.loc[df['word']==word].iloc[0]['Pleasantness']

                        if tag[1] == 'JJ' or tag[1] == 'RB' or tag[1] == 'VB' or tag[1] == 'NN':
                            print(tag)
                            print(pleasant)
                            if pleasant/3<0.5 or pleasant/3>0.8:
                                f1 += 1
                        polar = 1
                        flag = 0
                        break
                if flag == 0:
                    break
            if flag == 0:
                polar_tokens.append(tag)
            else:
                non_polar_tokens.append(tag)
        else:
            non_polar_tokens.append(tag)

                   




    print("stop_words_in_tweet",stop_words_in_tweet)
    print("english_words_in_tweet",english_words_in_tweet)
    print("punctuation_marks_in_tweet",punctuation_marks_in_tweet)
    print("capitalized_words_in_tweet",capitalized_words_in_tweet)
    print("other_tokens_in_tweet",other_tokens_in_tweet)
    print(featureVector_stem)
    print(featureVector_full)
    print(f7)
    print(f1)
    print(num_exclamation_marks)
    print(num_negations)
    
    return {"featureVector_stem": featureVector_stem, "featureVector_full": featureVector_full}
    

# Start extract_features   
def extract_features(tweet):
    tweet_words = set(tweet)
    features = {}
    for w in featureList:
        features[w] = (w in tweet_words)
    return features
    
    



    
if __name__ == "__main__":

    Tweet1 = "Apple's new Swift Playgrounds for iPad is a killer app for teaching code #WWDC $AAPL http://appleinsider.com/articles/16/06/22/apples-new-swift-playgrounds-for-ipad-is-a-killer-app-for-teaching-code …pic.twitter.com/UW8JzzSQrS"
    Tweet2 = "$GOOG #AAPL #IPHONE @AustenAllred I actually closed it around $97 down from $120ish so nay bad but I would suspect $AAPL is going lower."
    Tweet3 = " CANNOT noise Not aa NEVER CANNOT heihei"
    Tweet4 = "#ApPLe abandon #iPhone. NOt Not no {cannot} cooln't Good slowdown SHOWS shows shows [shows]  up, on @Jabil bottom line, http://bizj.us/1myby0 $AAPL $JBL $155m"
    Tweet5 = "$GOOG #AAPL #IPHONE @AustenAllred actually closed it around $97 down from $120ish so nay bad but would suspect $AAPL is going lower."
    
    process_tweet(Tweet5)
    #print(process_result)
    """
    print('................................................')
    # Read the tweets from csv file
    inpTweets = pd.read_csv('sanders-twitter-0.2/full-corpus-2-ways.csv', encoding='ISO-8859-1')
    # Get the tweet words
    tweets = []
    # Get the feature list
    featureList = []
    #------------------------------------------------------------------change back!!!
    count = 0
    for row in range (0, len(inpTweets.index)):
    #for row in range (0, 3):
        count += 1
        if(count%100 == 0):
            print(count)
        sentiment = inpTweets.iloc[row, 1]
        tweet = inpTweets.iloc[row, 4]

        pre_process_result = pre_process_tweet(tweet)
        featureVector = process_tweet(pre_process_result)['featureVector']
        featureList.extend(featureVector)
        tweets.append((featureVector, sentiment))
    # Remove featureList duplicates
    featureList = list(set(featureList))
    
    # Extract feature vector for all tweets in one shoot
    print("Extract feature vector for all tweets in one shoot")
    training_set = nltk.classify.util.apply_features(extract_features, tweets)
    #print(training_set)
    # Train the classifier
    NBClassifier = nltk.NaiveBayesClassifier.train(training_set)

    # Test the classifier
    testTweet = 'Congrats @ravikiranj, i heard you wrote a new tech post on sentiment analysis'
    pre_process_result = pre_process_tweet(testTweet)
    processedTestTweet = process_tweet(pre_process_result)['featureVector']
    #print( NBClassifier.classify(extract_features(processedTestTweet)))
    #print(NBClassifier.show_most_informative_features(10))
    LinearSVC_classifier = SklearnClassifier(LinearSVC())
    LinearSVC_classifier.train(training_set)
    LSVC_accuracy = nltk.classify.accuracy(LinearSVC_classifier, training_set)
    print(LSVC_accuracy)
    """

