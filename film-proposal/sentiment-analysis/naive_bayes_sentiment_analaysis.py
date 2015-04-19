# description: perform sentiment analysis on movie reviews using a naive bayes classifier
# authors: Paul Prae
# since: 4/19/2015
# modified from code written by Jacob Perkins in 2010 (http://streamhacker.com/2010/05/10/text-classification-sentiment-analysis-naive-bayes-classifier/)
# training data: nltk movie review corpus
# production data provided by: Bo Pang and Lillian Lee from their 2004 Sentiment Analysis research at Cornell. http://www.cs.cornell.edu/people/pabo/movie-review-data/
# data set: Polarity dataset (Pool of 27886 unprocessed html files). http://www.cs.cornell.edu/people/pabo/movie-review-data/polarity_html.zip
# note: tested with Python 3.3 on CentOS 7 and Windows 8 (64 bit)

import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews
 
def word_feats(words):
    return dict([(word, True) for word in words])
 
negids = movie_reviews.fileids('neg')
posids = movie_reviews.fileids('pos')
 
negfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'neg') for f in negids]
posfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'pos') for f in posids]

negcutoff = int(len(negfeats)*3/4)
poscutoff = int(len(posfeats)*3/4)

trainfeats = negfeats[:negcutoff] + posfeats[:poscutoff]
testfeats = negfeats[negcutoff:] + posfeats[poscutoff:]
print('train on ' + str(len(trainfeats)) + ' instances, test on ' + str(len(testfeats)) + ' instances')
 
classifier = NaiveBayesClassifier.train(trainfeats)
print ('accuracy: ' + str(nltk.classify.util.accuracy(classifier, testfeats)))
classifier.show_most_informative_features()
