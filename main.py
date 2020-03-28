from nltk.tokenize import word_tokenize
import string
import re

basque_v = []
catalan_v = []
galician_v = []
spanish_v = []
english_v = []
portugese_v = []


def pre_process_tweets(tweet):
    tweet = re.sub('((www\S+)|(http\S+))', '', tweet)  # remove URLs
    tweet = re.sub('@[^\s]+', '', tweet)  # remove usernames
    tweet = re.sub(r'#([^\s]+)', '', tweet)  # remove the # in #hashtag
    tweet = ''.join(c for c in tweet if c not in string.punctuation)  # remove punctuation
    tweet = re.sub('(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)', '', tweet) # remove certain special characters
    tweet = re.sub(r'\w*\d\w*', '', tweet) # remove strings containing numbers
    tweet = word_tokenize(tweet)  # separate into individual words
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
        # if tweet is in basque
        if trunc_at_language(message, "	", 2) == "eu":
            basque_v.extend(pre_process_tweets(trunc_at_tweet(message, "	", 3)))

            # if tweet is in catalan
        elif trunc_at_language(message, "	", 2) == "ca":
            catalan_v.extend(pre_process_tweets(trunc_at_tweet(message, "	", 3)))

            # if tweet is in galician
        elif trunc_at_language(message, "	", 2) == "gl":
            galician_v.extend(pre_process_tweets(trunc_at_tweet(message, "	", 3)))

            # if tweet is in spanish
        elif trunc_at_language(message, "	", 2) == "es":
            spanish_v.extend(pre_process_tweets(trunc_at_tweet(message, "	", 3)))

            # if tweet is in english
        elif trunc_at_language(message, "	", 2) == "en":
            english_v.extend(pre_process_tweets(trunc_at_tweet(message, "	", 3)))

            # if tweet is in portugese
        elif trunc_at_language(message, "	", 2) == "pt":
            portugese_v.extend(pre_process_tweets(trunc_at_tweet(message, "	", 3)))


#print("basque vocabulary: ",basque_v)
#print("catalan vocabulary: ", catalan_v)
#print("galician vocabulary: ", galician_v)
#print("spanish vocabulary: ", spanish_v)
print("english vocabulary: ", english_v)
#print("portugese vocabulary: ", portugese_v)