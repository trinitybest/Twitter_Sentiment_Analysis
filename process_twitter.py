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
import random

df = pd.read_csv("DAL/DAL-Full-List.csv")

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
    # all words in hashtags
    hashtags_words = []
    num_twitter_tags = 0
    num_exclamation_marks = 0
    num_negations = 0
    # f1: Number of Polar (+/-) POS (JJ, RB, VB, NN)
    f1 = 0
    # f2: Number of Polar other negation words, positive words, negative words
    f2 = 0
    # f3: Number of extremely-pos., extremely-neg., positive, negative emoticons
    # -----------------------This part is forth coming--------------------
    f3 = 0
    # f4: Number of (+/-) hashtags, capitalized words, exclamation words
    f4 = 0
    f5 = 0 
    f6 = 0
    # f7: Number of hashtags, URLs, targets, newlines
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
    f7 = len(hashtags) + num_twitter_tags
    
    # Get stop words and puncts
    for tag in pos_tag_t:
        word = tag[0]
        if word in stop_words:
            stop_words_in_tweet.append(tag)
            pos_tag_t[pos_tag_t.index(tag)]=('','')
        if word in punct:
            punctuation_marks_in_tweet.append(tag)
            if word == '!':
                num_exclamation_marks += 1
            pos_tag_t[pos_tag_t.index(tag)]=('','')

    # Get negations, english words and captilized words
    for tag in pos_tag_t:
        word = tag[0]
        if re.search(r"^[0-9]*$", word):
            pass
        elif len(wn.synsets(word)) >0:
            if word == 'NOT':
                num_negations += 1
                # Should we save NOT or not???---------------------------------------
            else:
                english_words_in_tweet.append(tag)
                if word[0].isupper() and len(word)>1:
                    capitalized_words_in_tweet.append(tag)
            pos_tag_t[pos_tag_t.index(tag)]=('','')

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

    # Check the polarity of features using DAL and WordNet
    sentiment_features = []
    # remove tokens with digits and change words to lowers case
    for tag in english_words_in_tweet + other_tokens_in_tweet:
        if bool(re.search(r'\d', tag[0])) == False:
            tmp = (tag[0].lower(), tag[1])
            sentiment_features.append(tmp)
    #print(sentiment_features)
    # Save polar and non-polar tokens based on DAL library
    polar_tokens = []
    non_polar_tokens = []
    for tag in sentiment_features:
        polar = None
        word = tag[0]
        #print(tag)
        # Polar words group 1
        if word in df.word.values:
            polar = 1
            polar_tokens.append(tag)
            # Get the pleasant value from DAL
            pleasant = df.loc[df['word']==word].iloc[0]['Pleasantness']
            #print(1.1, tag)
            #print(pleasant)
            # Check if POS equals JJ, RB, VB, or NN, calculate f1
            if tag[1] == 'JJ' or tag[1] == 'RB' or tag[1] == 'VB' or tag[1] == 'NN':
                #print(1.2, tag)
                #print(pleasant)
                f8 += pleasant/3
                # if this POS is positive or negative
                if pleasant/3<0.5 or pleasant/3>0.8:
                    f1 += 1
            # Calculate f2            
            if pleasant/3<0.5 or pleasant/3>0.8:
                f2 += 1
            f9 += pleasant/3
                
        # Polar words group 2
        elif len(wn.synsets(word)) >0:
            flag = 1
            for syn in wn.synsets(word):
                for l in syn.lemmas():
                    #print('--------------',l.name())
                    if l.name() in df.word.values:
                        pleasant = df.loc[df['word']==l.name()].iloc[0]['Pleasantness']
                        #print(2, tag)
                        #print(pleasant)
                        if tag[1] == 'JJ' or tag[1] == 'RB' or tag[1] == 'VB' or tag[1] == 'NN':
                            #print(2, tag)
                            #print(pleasant)
                            f8 += pleasant/3
                            if pleasant/3<0.5 or pleasant/3>0.8:
                                f1 += 1
                        # Calculate f2
                        if pleasant/3<0.5 or pleasant/3>0.8:
                            f2 += 1
                        f9 += pleasant/3
                        polar = 1
                        flag = 0
                        break
                if flag == 0:
                    break
            if flag == 0:
                polar_tokens.append(tag)
            else:
                non_polar_tokens.append(tag)
        # Non-polar words
        else:
            #print(3, tag)
            non_polar_tokens.append(tag)
            if tag[1] == 'JJ' or tag[1] == 'RB' or tag[1] == 'VB' or tag[1] == 'NN':
                #print(3, tag)
                f5 += 1
            else:
                #print('f6', tag)
                f6 += 1
   
    # change hashtags to lowercase
    for hashtag in hashtags:
        if bool(re.search(r'\d', hashtag)) == False:
            tmp = hashtag.lower()
            hashtags_words.append(tmp)

            
    # deal with hashtags
    for hashtag in hashtags_words:
        #print('hashtag', hashtag)
        if hashtag in df.word.values:
            #print('hashtag1')
            pleasant = df.loc[df['word']==hashtag].iloc[0]['Pleasantness']
            if pleasant/3<0.5 or pleasant/3>0.8:
                f4 += 1
        elif len(wn.synsets(hashtag)) >0:   
            #print('hashtag2')  
            #print(wn.synsets(hashtag)) 
            #print(word)   
            flag = 1
            for syn in wn.synsets(word):
                for l in syn.lemmas():                   
                    if l.name() in df.word.values:
                        #print('---', word)
                        pleasant = df.loc[df['word']==l.name()].iloc[0]['Pleasantness']

                        if pleasant/3<0.5 or pleasant/3>0.8:
                            f4 += 1
                        flag = 0
                        break
                if flag == 0:
                    break
        else:
            #print('hashtag3')
            pass 
                          
    f2 += num_negations
    f4 = f4 + num_exclamation_marks + len(capitalized_words_in_tweet)
    f10 = len(capitalized_words_in_tweet)/len(all_tokens)
    if len(capitalized_words_in_tweet)+num_exclamation_marks > 0:
        f11 = 1
    else:
        f11 = 0

    """
    print("stop_words_in_tweet",stop_words_in_tweet)
    print("english_words_in_tweet",english_words_in_tweet)
    print("punctuation_marks_in_tweet",punctuation_marks_in_tweet)
    print("capitalized_words_in_tweet",capitalized_words_in_tweet)
    print("other_tokens_in_tweet",other_tokens_in_tweet)
    print('hashtags', hashtags)
    print('UandT', UandT)
    print(featureVector_stem)
    print(featureVector_full)
    print('f1', f1)
    print('f2', f2)
    print('f4', f4)
    print('f5', f5)
    print('f6', f6)
    print('f7', f7)
    print('f8', f8)
    print('f9', f9)
    print('f10', f10)
    print('f11', f11)
    print('num_exclamation_marks', num_exclamation_marks)
    print('num_negations', num_negations)
    print('length of all tokens', len(all_tokens))
    """
    return {"featureVector_stem": featureVector_stem,
            "f1": f1,
            "f2": f2,
            "f3": f3,
            "f4": f4,
            "f5": f5,
            "f6": f6,
            "f7": f7,
            "f8": f8,
            "f9": f9,
            "f10": f10,
            "f11": f11
            }
    

# Start extract_features (only unigram word features) 
def extract_features(tweet):
    tweet_words = set(tweet)
    features = {}
    for w in featureList:
        features[w] = (w in tweet_words)
    return features
 
# Start extract_features (unigram word features and sentiment features)
def extract_features_2(tweet_dict):
    tweet_words = set(tweet_dict["featureVector_stem"])
    features = {}
    for w in featureList:
        features[w] = (w in tweet_words)
    features["f1"] = tweet_dict["f1"]
    features["f2"] = tweet_dict["f2"]
    features["f3"] = tweet_dict["f3"]
    features["f4"] = tweet_dict["f4"]
    features["f5"] = tweet_dict["f5"]
    features["f6"] = tweet_dict["f6"]
    features["f7"] = tweet_dict["f7"]
    features["f8"] = tweet_dict["f8"]
    features["f9"] = tweet_dict["f9"]
    features["f10"] = tweet_dict["f10"]
    features["f11"] = tweet_dict["f11"]
    return features
    
    



    
if __name__ == "__main__":
    """
    Tweet1 = "Apple's new Swift Playgrounds for iPad is a killer app for teaching code #WWDC $AAPL http://appleinsider.com/articles/16/06/22/apples-new-swift-playgrounds-for-ipad-is-a-killer-app-for-teaching-code …pic.twitter.com/UW8JzzSQrS"
    Tweet2 = "$GOOG #AAPL #IPHONE @AustenAllred I actually closed it around $97 down from $120ish so nay bad but I would suspect $AAPL is going lower."
    Tweet3 = " CANNOT noise Not aa NEVER CANNOT heihei"
    Tweet4 = "#ApPLe abandon #iPhone. NOt Not no {cannot} cooln't Good slowdown SHOWS shows shows [shows]  up, on @Jabil bottom line, http://bizj.us/1myby0 $AAPL $JBL $155m"
    Tweet5 = "$GOOG #Bad #AAPL #IPHONE @AustenAllred actually not Closed it around $97 down from $120ish so nay bad but would not suspect $AAPL is going lower http://bizj.us/1myby0 !"
    Tweet6 = "Apple Announces New iMac (Video) http://bit.ly/k45C0J *First Look: faster with powerful graphics* #AAPL"
    process_tweet(Tweet6)
    #print(process_result)
    """
    print('................................................')
    # Read the tweets from csv file
    inpTweets = pd.read_csv('sanders-twitter-0.2/full-corpus-2-ways.csv', encoding='ISO-8859-1')
    # Get the tweet words
    tweets = []
    # Get the feature list
    featureList = []
    # Get the feature set
    featuresets = []
    # temporary tweet_dicts
    tweet_dicts = []
    count = 0
    #------------------------------------------------
    for row in range (0, len(inpTweets.index)):
    #for row in range (0, 3):
        count += 1
        if(count%100 == 0):
            print(count)
        sentiment = inpTweets.iloc[row, 1]
        tweet = inpTweets.iloc[row, 4]

        featureVector = process_tweet(tweet)['featureVector_stem']
        featureList.extend(featureVector)
        tweets.append((featureVector, sentiment))
        tweet_dicts.append((process_tweet(tweet), sentiment))
        
    # Remove featureList duplicates
    featureList = list(set(featureList))
    # Create featuresets ------------------------------------------------
    count = 0
    #for row in range (0, len(inpTweets.index)):
    #------------------------------------------------
    """
    for row in range (0, 3):
        count += 1
        if(count%100 == 0):
            print(count)
        sentiment = inpTweets.iloc[row, 1]
        tweet = inpTweets.iloc[row, 4]
        #------------------------------------------------
        #featuresets.append((extract_features_2(process_tweet(tweet)), sentiment))
        featuresets.append((extract_features(process_tweet(tweet)["featureVector_stem"]), sentiment))
    # Extract feature vector for all tweets in one shoot
    print(featuresets)
    """
    print("Extract feature vector for all tweets in one shoot")
    training_set = nltk.classify.util.apply_features(extract_features_2, tweet_dicts)
    #training_set = nltk.classify.util.apply_features(extract_features, tweets)
    print(training_set)
    #print(training_set)
    """
    # Train the classifier
    NBClassifier = nltk.NaiveBayesClassifier.train(training_set)

    # Test the classifier
    testTweet = 'Congrats @ravikiranj, i heard you wrote a new tech post on sentiment analysis'
    pre_process_result = pre_process_tweet(testTweet)
    processedTestTweet = process_tweet(pre_process_result)['featureVector']
    #print( NBClassifier.classify(extract_features(processedTestTweet)))
    #print(NBClassifier.show_most_informative_features(10))
    """
    LinearSVC_classifier = SklearnClassifier(LinearSVC())
    LinearSVC_classifier.train(training_set[0:400])
    LSVC_accuracy = nltk.classify.accuracy(LinearSVC_classifier, training_set[400:800])
    print(LSVC_accuracy)
    

