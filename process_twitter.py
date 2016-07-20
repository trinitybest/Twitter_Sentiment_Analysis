"""
Author: TH
Date: 15/07/2016
"""
import re
from nltk.tokenize import StanfordTokenizer 
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
import string
def pre_process_tweet(tweet):
    """ pre-process the tweets:
        a)replace all the emoticons with a their sentiment po- larity by looking up the emoticon dictionary
        b)replace all URLs with a tag ||U||
        c)replace all nega- tions (e.g. not, no, never, n’t, cannot) by tag “NOT”
        d)replace targets (e.g. “@John”) with tag ||T|| 
        e)replace a sequence of repeated characters by three characters, for example, convert coooooooool to coool. 
        we add the f) step
        f)replace #hashtag and $cashtag with tag ||T||
    """
    # step a to be continued
    pre_process_a = tweet
    print(tweet)
    #print(re.search(r"(?P<url>https?://[^\s]+)", pre_process_a).group("url"))
    pre_process_b = re.sub(r"(?P<url>https?://[^\s]+)", "||U||", pre_process_a)    
    pre_process_c = re.sub(r"\s[N|n][O|o][T|t]|\s[N|n][O|o]\s|\snever\s|\sNEVER\s|[N|n]'[T|t]|cannot|CANNOT", " NOT ", pre_process_b)
    pre_process_d = re.sub(r'@[^\s]+', "||T||", pre_process_c)
    pre_process_e = re.sub(r"([a-z|A-Z])\1{3,20}", r'\1\1\1', pre_process_d)
    pre_process_f = re.sub(r"(#[^\s]+)|(\$[^\s]+)","||T||",pre_process_e)
    print(pre_process_f)
    return pre_process_f
def process_tweet(tweet):
    """ process the tweets
        a) tokenize the tweets using Stanford tokenizer
        b) identify stop words
        c) English words in WordNet(Fell- baum, 1998)
        d) identify punctuation (Penn Treebank)
    """
    stop_words_in_tweet = []
    english_words_in_tweet = []
    punctuation_marks_in_tweet = []
    capitalized_words_in_tweet = []
    num_twitter_tags = 0
    num_exclamation_marks = 0
    num_negations = 0

    tokenized_tweet = StanfordTokenizer().tokenize(tweet)
    all_tokens = tokenized_tweet
    stop_words = set(stopwords.words('english'))
    punct = list(string.punctuation)
    punct.append('-LRB-')
    punct.append('-RRB-')
    punct.append('-LCB-')
    punct.append('-RCB-')
    print(tokenized_tweet)

    for word in tokenized_tweet:
        if word =='U' or word=='T':
            num_twitter_tags += 1
            tokenized_tweet[tokenized_tweet.index(word)] =''
    for word in tokenized_tweet:
        if word in stop_words:
            stop_words_in_tweet.append(word)
            tokenized_tweet[tokenized_tweet.index(word)] =''
        if word in punct:
            punctuation_marks_in_tweet.append(word)
            if word == '!':
                num_exclamation_marks += 1
            tokenized_tweet[tokenized_tweet.index(word)] =''
    for word in tokenized_tweet:

        
        if len(wn.synsets(word)) >0:

            
            if word == 'NOT':
                num_negations += 1
            else:
                english_words_in_tweet.append(word)
                if word[0].isupper():
                    capitalized_words_in_tweet.append(word)
            

            tokenized_tweet[tokenized_tweet.index(word)] =''

    seen = set()
    other_tokens_in_tweet = []
    for item in tokenized_tweet:
        if item:
            if item not in seen:
                seen.add(item)
                other_tokens_in_tweet.append(item)


    print("stop_words_in_tweet",stop_words_in_tweet)
    print("english_words_in_tweet",english_words_in_tweet)
    print("punctuation_marks_in_tweet",punctuation_marks_in_tweet)
    print("capitalized_words_in_tweet",capitalized_words_in_tweet)
    print("other_tokens_in_tweet",other_tokens_in_tweet)

    print(num_twitter_tags)
    print(num_exclamation_marks)
    print(num_negations)

    

    
if __name__ == "__main__":
    Tweet1 = "Apple's new Swift Playgrounds for iPad is a killer app for teaching code #WWDC $AAPL http://appleinsider.com/articles/16/06/22/apples-new-swift-playgrounds-for-ipad-is-a-killer-app-for-teaching-code …pic.twitter.com/UW8JzzSQrS"
    Tweet2 = "@AustenAllred I actually closed it around $97 down from $120ish so nay bad but I would suspect $AAPL is going lower."
    Tweet3 = " CANNOT noise Not aa NEVER CANNOT heihei"
    Tweet4 = "#Apple #iPhone. NOt Not no {cannot} cooln't Good slowdown shows shows [shows]  up, on @Jabil bottom line, http://bizj.us/1myby0 $AAPL $JBL"
    pre_process_result = pre_process_tweet(Tweet4)
    process_tweet(pre_process_result)
