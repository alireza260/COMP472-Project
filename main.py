from nltk.tokenize import word_tokenize
import string
import re

message = "@GaleHunterJkun + Como te salgas ahora te mataré!"

def pre_process_tweets(tweet):
    tweet = re.sub('((www\S+)|(http\S+))', '', tweet) # remove URLs
    tweet = re.sub('@[^\s]+', '', tweet)  # remove usernames
    tweet = re.sub(r'#([^\s]+)', '', tweet)  # remove the # in #hashtag
    tweet = re.sub(r'\d+', 'contnum', tweet)
    tweet = ''.join(c for c in tweet if c not in string.punctuation)  # remove punctuation
    tweet = word_tokenize(tweet)  # remove repeated characters, guapaaaa -> guapa
    return tweet

print(pre_process_tweets(message))