# description: perform sentiment analysis on movie reviews using a naive bayes classifier.
# authors: Paul Prae
# since: 4/19/2015
# modified from code written by Jacob Perkins in 2010 (http://streamhacker.com/2010/05/10/text-classification-sentiment-analysis-naive-bayes-classifier/)
# training data: nltk movie review corpus
# production data provided by: Bo Pang and Lillian Lee from their 2004 Sentiment Analysis research at Cornell. http://www.cs.cornell.edu/people/pabo/movie-review-data/
# data set: Polarity dataset (Pool of 27886 unprocessed html files). http://www.cs.cornell.edu/people/pabo/movie-review-data/polarity_html.zip
# note: tested with Python 3.3 on CentOS 7 and Windows 8 (64 bit)
# TODO: Test production classifier on all data.

import csv
import nltk.metrics
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews
 
# loop over every word. place it in a dict and assign True to that word
# creates a dict out of a list of tuples
# a tuple is (some_word, True)
# the dict() constructor builds dictionaries directly from sequences of key-value pairs
# each word simply maps to True in the returned dict
# note: even if a word repeats itself in the review, it will only be represented once
def word_feats(words):
    return dict([(word, True) for word in words])

### setup data for training ###
# get the ids from the training set for all negatively reviewed and positively reviewed movies respectively
negids = movie_reviews.fileids('neg')
posids = movie_reviews.fileids('pos')
 
# create a list of words that are negative and another list of words that are positive
# these lists (feats) will be a list of tuples e.g. [(word_feats_dict, sentiment)...]
# each word_feats dict (the first value in the tuple) will be associated with positive or negative sentiment
# note: movie_reviews.words(fileids=[f]) is just a list of words from a single review
#negfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'neg') for f in negids]
#posfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'pos') for f in posids]

### training ###
# build training set. classify training set.
#trainfeats = negfeats + posfeats
# TODO: should we shuffle these? Not sure how all positive upfront affects the classifier.
# e.g. import random; random.shuffle(trainfeats)
#classifier = NaiveBayesClassifier.train(trainfeats)

### classify production data ###
# open csv with our movie reviews in it
filmDataFilename = './data/film_review_data.csv';
filmDataReader = csv.reader(open(filmDataFilename, encoding="utf8"));
filmDataReader.__next__();
outputFile = './data/film_review_sentiment.csv'
filmWriter = csv.writer(open(outputFile, 'w', newline='', encoding="utf8"))
filmWriter.writerow(['review_id', 'title', 'release_year', 'review_sentiment'])
# loop over production movie review data
count = 0;
for filmData in filmDataReader:
	count += 1;
	# pull out film review text and make it lowercase
	# TODO: null or/and empty string check
	review = filmData[3].lower();
	# turn each review string into a list of words
	reviewWords = review.split(' ')

	# pass the list of words into word_feats
	reviewWordsFeats = word_feats(reviewWords)

	# classify production data. http://www.nltk.org/api/nltk.classify.html
	sentiment = "pos/neg" # classifier.classify(reviewWordsFeats)

	# write results to a file.
	# note: same format as input data except instead of a review column there is a sentiment column.
	filmWriter.writerow([filmData[0], filmData[1], filmData[2], sentiment])
	# TODO: remove ater testing
	if count == 10:
		exit(0)
