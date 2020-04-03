import nltk
import os
import numpy as np
from nltk.tokenize import word_tokenize
from collections import Counter
import string
import re

basque_v = []
catalan_v = []
galician_v = []
spanish_v = []
english_v = []
portugese_v = []

#count of each language in training file
basque_c = catalan_c = galician_c = spanish_c = english_c = portugese_c = 0

#count of each language in testing file
basque_nb = catalan_nb = galician_nb = spanish_nb = english_nb = portugese_nb = 0

#true positive of each language
basque_tp = catalan_tp = galician_tp = spanish_tp = english_tp = portugese_tp = 0

#true negative of each language
#basque_tn = catalan_tn = galician_tn = spanish_tn = english_tn = portugese_tn = 0

#false positive of each language
basque_fp = catalan_fp = galician_fp = spanish_fp = english_fp = portugese_fp = 0

#false negative of each language
basque_fn = catalan_fn = galician_fn = spanish_fn = english_fn = portugese_fn = 0

nb_of_tweets = 0
nb_of_tweets_testing = 0

accuracy_score = 0

print("vocabulary value (0,1 or 2):")
voc_value = int(input())

while voc_value < 0 or voc_value > 2:
    print("v value (0,1 or 2):")
    voc_value = int(input())

print("size of n-grams (1,2 or 3):")
n_gram_value = int(input())

while n_gram_value < 1 or n_gram_value > 3:
    print("n-gram value (1,2 or 3):")
    n_gram_value = int(input())

print("smoothing value (between 0 and 1):")
smoothing_value = float(input())

while smoothing_value < 0 or smoothing_value > 1:
    print("smoothing value (between 0 and 1):")
    smoothing_value = float(input())

def n_gram(n_input, tweet_string):
    n_grams = []

    spaced = ''
    for ch in tweet_string:
        spaced = spaced + ch + ' '

    tokenized = spaced.split(" ")

    if n_input == 1:
        for i in tokenized:
            n_grams.append((''.join([w + '' for w in i])).strip())

        n_grams = [x for x in n_grams if "*" not in x and len(x) is 1]

    elif n_input == 2:

        myList = list(nltk.bigrams(tokenized))

        for i in myList:
            n_grams.append((''.join([w + '' for w in i])).strip())

        n_grams = [x for x in n_grams if "*" not in x and len(x) is 2]
    elif n_input == 3:

        myList = list(nltk.trigrams(tokenized))

        for i in myList:
            n_grams.append((''.join([w + '' for w in i])).strip())

        n_grams = [x for x in n_grams if "*" not in x and len(x) is 3]

    return n_grams


def pre_process_tweets(tweet):
    tweet = re.sub('((www\S+)|(http\S+))', '', tweet)  # remove URLs
    tweet = re.sub('@[^\s]+', '', tweet)  # remove usernames

    if voc_value == 2:
        tweet = ''.join(c if c.isalpha() or c is ' ' else '*' for c in tweet ) # replace if not isalpha

    elif voc_value == 1 or voc_value == 0:
        #tweet = ''.join(c for c in tweet if c not in string.punctuation)  # remove punctuation
        tweet = re.sub('(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)', '*', tweet)  # replace special characters
        tweet = re.sub('[0-9]', '*', tweet)  # remove strings containing numbers
        if voc_value == 0:
            tweet = tweet.lower()  # transform all characters to lowercase


    tweet = word_tokenize(tweet)  # separate into individual words

    tweet = [x for x in tweet]

    for tweet_string in tweet:

        if "*" in tweet_string:

            if tweet_string[0] is not "*" and tweet_string[len(tweet_string)-1] is not "*":

                return n_gram(n_gram_value, tweet_string)

    tweet = [x.replace('*', '') for x in tweet]

    tweet = [x for x in tweet if x]


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
    total_unique = Counter(total_v)

    #set prior probability values
    basque_prior = np.log10(basque_c / nb_of_tweets)
    catalan_prior = np.log10(catalan_c / nb_of_tweets)
    galician_prior = np.log10(galician_c / nb_of_tweets)
    spanish_prior = np.log10(spanish_c / nb_of_tweets)
    english_prior = np.log10(english_c / nb_of_tweets)
    portugese_prior = np.log10(portugese_c / nb_of_tweets)

def calc_language_prob(vocabulary, t_element, total_unique):

    return np.log10((vocabulary.count(t_element) + smoothing_value) / (len(vocabulary) + smoothing_value*len(total_unique)))

# if trace file already exists, wipe the data before appending new data
if os.path.exists("trace_" + str(voc_value) + "_" + str(n_gram_value) + "_" + str(smoothing_value) + ".txt"):
    with open("trace_" + str(voc_value) + "_" + str(n_gram_value) + "_" + str(smoothing_value) + ".txt", "w", encoding="utf8") as trace_output_file:
        trace_output_file.write("")

# if eval file already exists, wipe the data before appending new data
if os.path.exists("eval_" + str(voc_value) + "_" + str(n_gram_value) + "_" + str(smoothing_value) + ".txt"):
    with open("eval_" + str(voc_value) + "_" + str(n_gram_value) + "_" + str(smoothing_value) + ".txt", "w", encoding="utf8") as eval_output_file:
        eval_output_file.write("")


def precision(true_positive, false_positive):

    return (true_positive/ (true_positive + false_positive))

def recall(true_positive, false_negative):

    return (true_positive/ (true_positive + false_negative))

def f1(true_positive, false_positive, false_negative):

    prec = true_positive/ (true_positive + false_positive)

    rec = true_positive/ (true_positive + false_negative)

    return 2*(prec*rec)/(prec+rec)

def macro_f1():
    return (f1(basque_tp, basque_fp, basque_fn) + f1(catalan_tp, catalan_fp, catalan_fn) + f1(galician_tp, galician_fp, galician_fn) +
           f1(spanish_tp, spanish_fp, spanish_fn) + f1(english_tp, english_fp, english_fn) + f1(portugese_tp, portugese_fp, portugese_fn))/6

def w_a_f1():
    return (basque_nb*f1(basque_tp, basque_fp, basque_fn) + catalan_nb*f1(catalan_tp, catalan_fp, catalan_fn) + galician_nb*f1(galician_tp, galician_fp, galician_fn) +
           spanish_nb*f1(spanish_tp, spanish_fp, spanish_fn) + english_nb*f1(english_tp, english_fp, english_fn) +
            portugese_nb*f1(portugese_tp, portugese_fp, portugese_fn))/nb_of_tweets_testing



with open('test-tweets-given.txt', encoding="utf8") as testing_file:
    try:
        for line in testing_file:
            right_or_wrong_a = "wrong"
            correct_l = trunc_at_language(str(line), "	", 2)
            tweet_ID = trunc_at_language(str(line), "	", 0)
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
                basque_prob += calc_language_prob(basque_v, x, total_unique)
                catalan_prob += calc_language_prob(catalan_v, x, total_unique)
                galician_prob += calc_language_prob(galician_v, x, total_unique)
                spanish_prob += calc_language_prob(spanish_v, x, total_unique)
                english_prob += calc_language_prob(english_v, x, total_unique)
                portugese_prob += calc_language_prob(portugese_v, x, total_unique)

            most_probable_l = max(basque_prob,catalan_prob,galician_prob,spanish_prob,english_prob,portugese_prob)

            with open("trace_" + str(voc_value) + "_" + str(n_gram_value) + "_" + str(smoothing_value) + ".txt", "a", encoding="utf8") as trace_output_file:

                if correct_l == "eu":
                    basque_nb += 1
                elif correct_l == "ca":
                    catalan_nb += 1
                elif correct_l == "gl":
                    galician_nb += 1
                elif correct_l == "es":
                    spanish_nb += 1
                elif correct_l == "en":
                    english_nb += 1
                elif correct_l == "pt":
                    portugese_nb += 1
                if most_probable_l == basque_prob:
                    if correct_l == "eu":
                        accuracy_score += 1
                        basque_tp += 1

                        #catalan_tn += 1
                        #galician_tn += 1
                        #spanish_tn += 1
                        #english_tn += 1
                        #portugese_tn += 1

                        right_or_wrong_a = "correct"

                    else:
                        basque_fp += 1
                    trace_output_file.write(tweet_ID + "  eu  " + str(most_probable_l) + "  " + correct_l + "  " + right_or_wrong_a + "\n")

                elif most_probable_l != basque_prob:
                    if correct_l == "eu":
                        basque_fn += 1

                if most_probable_l == catalan_prob:
                    if correct_l == "ca":
                        accuracy_score += 1
                        catalan_tp += 1

                        #basque_tn += 1
                        #galician_tn += 1
                        #spanish_tn += 1
                        #english_tn += 1
                        #portugese_tn += 1

                        right_or_wrong_a = "correct"
                    else:
                        catalan_fp += 1
                    trace_output_file.write(tweet_ID + "  ca  " + str(most_probable_l) + "  " + correct_l + "  " + right_or_wrong_a + "\n")

                elif most_probable_l != catalan_prob:
                    if correct_l == "ca":
                        catalan_fn += 1

                if most_probable_l == galician_prob:
                    if correct_l == "gl":
                        accuracy_score += 1
                        galician_tp += 1

                        #basque_tn += 1
                        #catalan_tn += 1
                        #spanish_tn += 1
                        #english_tn += 1
                        #portugese_tn += 1

                        right_or_wrong_a = "correct"
                    else:
                        galician_fp += 1
                    trace_output_file.write(tweet_ID + "  gl  " + str(most_probable_l) + "  " + correct_l + "  " + right_or_wrong_a + "\n")

                elif most_probable_l != galician_prob:
                    if correct_l == "gl":
                        galician_fn += 1

                if most_probable_l == spanish_prob:
                    if correct_l == "es":
                        accuracy_score += 1
                        spanish_tp += 1

                        #basque_tn += 1
                        #catalan_tn += 1
                        #galician_tn += 1
                        #english_tn += 1
                        #portugese_tn += 1

                        right_or_wrong_a = "correct"
                    else:
                        spanish_fp += 1
                    trace_output_file.write(tweet_ID + "  es  " + str(most_probable_l) + "  " + correct_l + "  " + right_or_wrong_a + "\n")

                elif most_probable_l != spanish_prob:
                    if correct_l == "es":
                        spanish_fn += 1

                if most_probable_l == english_prob:
                    if correct_l == "en":
                        accuracy_score += 1
                        english_tp += 1

                        #basque_tn += 1
                        #catalan_tn += 1
                        #galician_tn += 1
                        #spanish_tn += 1
                        #portugese_tn += 1

                        right_or_wrong_a = "correct"
                    else:
                        english_fp += 1
                    trace_output_file.write(tweet_ID + "  en  " + str(most_probable_l) + "  " + correct_l + "  " + right_or_wrong_a + "\n")

                elif most_probable_l != english_prob:
                    if correct_l == "en":
                        english_fn += 1

                if most_probable_l == portugese_prob:
                    if correct_l == "pt":
                        accuracy_score += 1
                        portugese_tp += 1

                        #basque_tn += 1
                        #catalan_tn += 1
                        #galician_tn += 1
                        #spanish_tn += 1
                        #english_tn += 1

                        right_or_wrong_a = "correct"
                    else:
                        portugese_fp += 1
                    trace_output_file.write(tweet_ID + "  pt  " + str(most_probable_l) + "  " + correct_l + "  " + right_or_wrong_a + "\n")

                elif most_probable_l != portugese_prob:
                    if correct_l == "pt":
                        portugese_fn += 1

                print(nb_of_tweets_testing)

    except (IndexError):
        pass

    print("score:", accuracy_score, "/", nb_of_tweets_testing)

with open("eval_" + str(voc_value) + "_" + str(n_gram_value) + "_" + str(smoothing_value) + ".txt", "a", encoding="utf8") as eval_output_file:
    eval_output_file.write(str(accuracy_score/nb_of_tweets_testing) + "\n")

    eval_output_file.write(str(precision(basque_tp, basque_fp)) + "  " + str(precision(catalan_tp, catalan_fp)) + "  " + str(precision(galician_tp, galician_fp)) + "  " +
                           str(precision(spanish_tp, spanish_fp)) + "  " + str(precision(english_tp, english_fp)) + "  " + str(precision(portugese_tp, portugese_fp)) + "\n")

    eval_output_file.write(str(recall(basque_tp, basque_fn)) + "  " + str(recall(catalan_tp, catalan_fn)) + "  " + str(recall(galician_tp, galician_fn)) + "  " +
        str(recall(spanish_tp, spanish_fn)) + "  " + str(recall(english_tp, english_fn)) + "  " + str(recall(portugese_tp, portugese_fn)) + "\n")

    eval_output_file.write(str(f1(basque_tp, basque_fp, basque_fn)) + "  " + str(f1(catalan_tp, catalan_fp, catalan_fn)) + "  " + str(f1(galician_tp, galician_fp, galician_fn)) + "  " +
        str(f1(spanish_tp, spanish_fp, spanish_fn)) + "  " + str(f1(english_tp, english_fp, english_fn)) + "  " + str(f1(portugese_tp, portugese_fp, portugese_fn)) + "\n")

    eval_output_file.write(str(macro_f1()) + "  " + str(w_a_f1()))





#print("basque vocabulary: ",basque_v)
#print("catalan vocabulary: ", catalan_v)
#print("galician vocabulary: ", galician_v)
#print("spanish vocabulary: ", spanish_v)
#print("english vocabulary: ", english_v)
#print("portugese vocabulary: ", portugese_v)