# description: perform sentiment analysis on movie reviews using a naive bayes classifier.
#	this file tests and evaluates my approach.
# authors: Paul Prae
# since: 4/19/2015
# modified from code written by Jacob Perkins in 2010 (http://streamhacker.com/2010/05/10/text-classification-sentiment-analysis-naive-bayes-classifier/)
# training data: nltk movie review corpus
# note: tested with Python 3.3 on CentOS 7 and Windows 8 (64 bit)

import collections
import nltk.metrics
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

### stats ###
# TODO: Consider seeing the distribution: http://www.nltk.org/howto/classify.html
# print('%.4f %.4f' % (pdist.prob('neg'), pdist.prob('pos')))
print ('accuracy: ' + str(nltk.classify.util.accuracy(classifier, testfeats)))
classifier.show_most_informative_features()

refsets = collections.defaultdict(set)
testsets = collections.defaultdict(set)
 
for i, (feats, label) in enumerate(testfeats):
    refsets[label].add(i)
    observed = classifier.classify(feats)
    testsets[observed].add(i)

print ('pos precision:' + str(nltk.metrics.precision(refsets['pos'], testsets['pos'])))
print ('pos recall:' + str(nltk.metrics.recall(refsets['pos'], testsets['pos'])))
print ('pos F-measure:' + str(nltk.metrics.f_measure(refsets['pos'], testsets['pos'])))
print ('neg precision:' + str(nltk.metrics.precision(refsets['neg'], testsets['neg'])))
print ('neg recall:' + str(nltk.metrics.recall(refsets['neg'], testsets['neg'])))
print ('neg F-measure:' + str(nltk.metrics.f_measure(refsets['neg'], testsets['neg'])))
