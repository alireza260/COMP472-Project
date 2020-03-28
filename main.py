from nltk.tokenize import word_tokenize
import string
import re


def pre_process_tweets(tweet):
    tweet = re.sub('((www\S+)|(http\S+))', '', tweet)  # remove URLs
    tweet = re.sub('@[^\s]+', '', tweet)  # remove usernames
    tweet = re.sub(r'#([^\s]+)', '', tweet)  # remove the # in #hashtag
    tweet = ''.join(c for c in tweet if c not in string.punctuation)  # remove punctuation
    tweet = re.sub('(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)', '', tweet) # remove certain special characters
    tweet = re.sub(r'\w*\d\w*', '', tweet) # remove strings containing numbers
    tweet = word_tokenize(tweet)  # remove repeated characters, guapaaaa -> guapa
    return tweet

def trunc_at_tweet(s, d, n):
    strlist = ""
    return strlist.join(s.split(d, n)[n:])

def trunc_at_language(s, d, n):
    strlist = ""
    return strlist.join(s.split(d)[n])



with open('training-tweets.txt', encoding="utf8") as training_file:
    for line in training_file:
        message = str(line)
        # if tweet is in english
        if trunc_at_language(message, "	", 2) == "en":
            print(pre_process_tweets(trunc_at_tweet(message, "	", 3)))
