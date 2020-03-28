import numpy as np
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

def calc_language_prob(vocabulary, t_element):

    return np.log10((vocabulary.count(t_element)) / len(vocabulary))

with open('test-tweets-given.txt', encoding="utf8") as testing_file:
    for line in testing_file:
        correct_l = trunc_at_language(str(line), "	", 2)
        message = pre_process_tweets(trunc_at_tweet(str(line), "	", 3))

        basque_prob = catalan_prob = galician_prob = spanish_prob = english_prob = portugese_prob = 0

        for x in message:
            basque_prob += calc_language_prob(basque_v, x)
            catalan_prob += calc_language_prob(catalan_v, x)
            galician_prob += calc_language_prob(galician_v, x)
            spanish_prob += calc_language_prob(spanish_v, x)
            english_prob += calc_language_prob(english_v, x)
            portugese_prob += calc_language_prob(portugese_v, x)

        most_probable_l = max(basque_prob,catalan_prob,galician_prob,spanish_prob,english_prob,portugese_prob)

        if most_probable_l == basque_prob:
            print(correct_l, ": eu")
        elif most_probable_l == catalan_prob:
            print(correct_l, ": ca")
        elif most_probable_l == galician_prob:
            print(correct_l, ": gl")
        elif most_probable_l == spanish_prob:
            print(correct_l, ": es")
        elif most_probable_l == english_prob:
            print(correct_l, ": en")
        elif most_probable_l == portugese_prob:
            print(correct_l, ": pt")









#print("basque vocabulary: ",basque_v)
#print("catalan vocabulary: ", catalan_v)
#print("galician vocabulary: ", galician_v)
#print("spanish vocabulary: ", spanish_v)
#print("english vocabulary: ", english_v)
#print("portugese vocabulary: ", portugese_v)