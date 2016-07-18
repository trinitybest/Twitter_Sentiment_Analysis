"""
Author: TH
Date: 15/07/2016
"""
import re
from nltk.tokenize import StanfordTokenizer 
from nltk.corpus import stopwords
def pre_process_tweet(tweet):
    """ pre-process the tweets:
        a)replace all the emoticons with a their sentiment po- larity by looking up the emoticon dictionary
        b)replace all URLs with a tag ||U||
        c)replace targets (e.g. “@John”) with tag ||T||
        d)replace all nega- tions (e.g. not, no, never, n’t, cannot) by tag “NOT”
        e)replace a sequence of repeated characters by three characters, for example, convert coooooooool to coool. We
    """
    # step a to be continued
    pre_process_a = tweet
    print(tweet)
    #print(re.search(r"(?P<url>https?://[^\s]+)", pre_process_a).group("url"))
    pre_process_b = re.sub(r"(?P<url>https?://[^\s]+)", "||U||", pre_process_a)
    pre_process_c = re.sub(r'@[^\s]+', "||T||", pre_process_b)
    pre_process_d = re.sub(r"\s[N|n][O|o][T|t]\s|\s[N|n][O|o]\s|\snever\s|\sNEVER\s|[N|n]'[T|t]|\scannot\s|\sCANNOT\s", " NOT ", pre_process_c)
    pre_process_e = re.sub(r"([a-z|A-Z])\1{3,20}", r'\1\1\1', pre_process_d)
    print(pre_process_e)
    return pre_process_e
def process_tweet(tweet):
    """ process the tweets
        a) tokenize the tweets using Stanford tokenizer
        b) identify stop words
        c) English words in WordNet(Fell- baum, 1998)
        d) identify punctuation (Penn Treebank)
    """
    print(type(tweet))
    tokenized_tweet = StanfordTokenizer().tokenize(tweet)
    stop_words = set(stopwords.words('english'))
    print(tokenized_tweet)
if __name__ == "__main__":
    Tweet1 = "Apple's new Swift Playgrounds for iPad is a killer app for teaching code #WWDC $AAPL http://appleinsider.com/articles/16/06/22/apples-new-swift-playgrounds-for-ipad-is-a-killer-app-for-teaching-code …pic.twitter.com/UW8JzzSQrS"
    Tweet2 = "@AustenAllred I actually closed it around $97 down from $120ish so nay bad but I would suspect $AAPL is going lower."
    Tweet3 = " CANNOT noise Not aa NEVER CANNOT heihei"
    Tweet4 = "#Apple #iPhone slowdown shows up on @Jabil bottom line http://bizj.us/1myby0 $AAPL $JBL"
    pre_process_result = pre_process_tweet(Tweet4)
    process_tweet(pre_process_result)
