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

basque_c = catalan_c = galician_c = spanish_c = english_c = portugese_c = 0

nb_of_tweets = 0
nb_of_tweets_testing = 0

accuracy_score = 0

print("vocabulary value (0,1 or 2):")
voc_value = int(input())

while voc_value < 0 or voc_value > 2:
    print("v value (0,1 or 2):")
    voc_value = int(input())

print("smoothing value (between 0 and 1):")
smoothing_value = float(input())

while smoothing_value < 0 or smoothing_value > 1:
    print("smoothing value (between 0 and 1):")
    smoothing_value = float(input())

def pre_process_tweets(tweet):
    tweet = re.sub('((www\S+)|(http\S+))', '', tweet)  # remove URLs
    tweet = re.sub('@[^\s]+', '', tweet)  # remove usernames
    tweet = re.sub(r'#([^\s]+)', '', tweet)  # remove the # in #hashtag

    if voc_value == 2:
        tweet = ''.join(c if c.isalpha() else ' ' for c in tweet) # isalpha

    elif voc_value == 1 or voc_value == 0:
        tweet = ''.join(c for c in tweet if c not in string.punctuation)  # remove punctuation
        tweet = re.sub('(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)', '', tweet)  # remove certain special characters
        tweet = re.sub(r'\w*\d\w*', '', tweet)  # remove strings containing numbers
        if voc_value == 0:
            tweet = tweet.lower()  # transform all characters to lowercase


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

        #count number of tweets in testing file
        nb_of_tweets += 1

        # if tweet is in basque
        if trunc_at_language(message, "	", 2) == "eu":
            basque_c += 1
            basque_v.extend(pre_process_tweets(trunc_at_tweet(message, "	", 3)))

            # if tweet is in catalan
        elif trunc_at_language(message, "	", 2) == "ca":
            catalan_c += 1
            catalan_v.extend(pre_process_tweets(trunc_at_tweet(message, "	", 3)))

            # if tweet is in galician
        elif trunc_at_language(message, "	", 2) == "gl":
            galician_c += 1
            galician_v.extend(pre_process_tweets(trunc_at_tweet(message, "	", 3)))

            # if tweet is in spanish
        elif trunc_at_language(message, "	", 2) == "es":
            spanish_c += 1
            spanish_v.extend(pre_process_tweets(trunc_at_tweet(message, "	", 3)))

            # if tweet is in english
        elif trunc_at_language(message, "	", 2) == "en":
            english_c += 1
            english_v.extend(pre_process_tweets(trunc_at_tweet(message, "	", 3)))

            # if tweet is in portugese
        elif trunc_at_language(message, "	", 2) == "pt":
            portugese_c += 1
            portugese_v.extend(pre_process_tweets(trunc_at_tweet(message, "	", 3)))

    total_v = basque_v + catalan_v + galician_v + spanish_v + english_v + portugese_v

    #set prior probability values
    basque_prior = np.log10(basque_c / nb_of_tweets)
    catalan_prior = np.log10(catalan_c / nb_of_tweets)
    galician_prior = np.log10(galician_c / nb_of_tweets)
    spanish_prior = np.log10(spanish_c / nb_of_tweets)
    english_prior = np.log10(english_c / nb_of_tweets)
    portugese_prior = np.log10(portugese_c / nb_of_tweets)

def calc_language_prob(vocabulary, t_element, total_v):

    return np.log10((vocabulary.count(t_element) + smoothing_value) / (len(vocabulary) + smoothing_value*len(total_v)))

with open('test-tweets-given.txt', encoding="utf8") as testing_file:
    for line in testing_file:
        correct_l = trunc_at_language(str(line), "	", 2)
        message = pre_process_tweets(trunc_at_tweet(str(line), "	", 3))

        # count number of tweets in testing file
        nb_of_tweets_testing += 1

        basque_prob = basque_prior
        catalan_prob = catalan_prior
        galician_prob = galician_prior
        spanish_prob = spanish_prior
        english_prob = english_prior
        portugese_prob = portugese_prior

        for x in message:
            basque_prob += calc_language_prob(basque_v, x, total_v)
            catalan_prob += calc_language_prob(catalan_v, x, total_v)
            galician_prob += calc_language_prob(galician_v, x, total_v)
            spanish_prob += calc_language_prob(spanish_v, x, total_v)
            english_prob += calc_language_prob(english_v, x, total_v)
            portugese_prob += calc_language_prob(portugese_v, x, total_v)

        most_probable_l = max(basque_prob,catalan_prob,galician_prob,spanish_prob,english_prob,portugese_prob)

        if most_probable_l == basque_prob:
            print(correct_l, ": eu")
            if correct_l == "eu":
                accuracy_score += 1
        elif most_probable_l == catalan_prob:
            print(correct_l, ": ca")
            if correct_l == "ca":
                accuracy_score += 1
        elif most_probable_l == galician_prob:
            print(correct_l, ": gl")
            if correct_l == "gl":
                accuracy_score += 1
        elif most_probable_l == spanish_prob:
            print(correct_l, ": es")
            if correct_l == "es":
                accuracy_score += 1
        elif most_probable_l == english_prob:
            print(correct_l, ": en")
            if correct_l == "en":
                accuracy_score += 1
        elif most_probable_l == portugese_prob:
            print(correct_l, ": pt")
            if correct_l == "pt":
                accuracy_score += 1
        print("score: ", accuracy_score, "/ ", nb_of_tweets_testing)

#print("basque vocabulary: ",basque_v)
#print("catalan vocabulary: ", catalan_v)
#print("galician vocabulary: ", galician_v)
#print("spanish vocabulary: ", spanish_v)
#print("english vocabulary: ", english_v)
#print("portugese vocabulary: ", portugese_v)