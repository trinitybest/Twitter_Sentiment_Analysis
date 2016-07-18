"""
Author: TH
Date: 15/07/2016
"""
import re
#pre process the each tweet
def pre_process_tweet(tweet):
    pre_process_a = tweet.lower()
    #print(re.search(r"(?P<url>https?://[^\s]+)", pre_process_a).group("url"))
    pre_process_b = re.sub(r"(?P<url>https?://[^\s]+)", "||U||", pre_process_a)
    pre_process_c = re.sub(r'@[^\s]+', "||T||", pre_process_b)
    pre_process_d = re.sub(r"\snot\s|\sno\s|\snever\s|n't|\scannot\s", " NOT ", pre_process_c)
    pre_process_e = re.sub(r"([a-z])\1{3,20}", r'\1\1\1', pre_process_d)
    print(pre_process_e)
if __name__ == "__main__":
    Tweet1 = "Apple's new Swift Playgrounds for iPad is a killer app for teaching code #WWDC $AAPL http://appleinsider.com/articles/16/06/22/apples-new-swift-playgrounds-for-ipad-is-a-killer-app-for-teaching-code …pic.twitter.com/UW8JzzSQrS"
    Tweet2 = "@AustenAllred I actually closed it around $97 down from $120ish so nay bad but I would suspect $AAPL is going lower."
    Tweet3 = "noise not aa no noa never n't cannot heihei'"
    Tweet4 = "coaaaaaaaaaaaool"
    pre_process_tweet(Tweet4)