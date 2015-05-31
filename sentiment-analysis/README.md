# Sentiment Analysis Overview
Using Python, I performed sentiment analysis on movie reviews.

## Lexicon Description
For training our classifier, we used the ‘movie_review’ corpus provided by the Natural Language Toolkit (NLTK) 3.0 (http://www.nltk.org/). It was derived from the Sentiment Polarity Dataset Version 2.0 provided by Bo Pang and Lillian Lee and introduced in the Proceedings of ACL of 2004. It was released to the public June, 2004. It has 1000 positive and 1000 negative processed reviews. "pos" and "neg", indicate the true classification (sentiment) of the component files according to their automatic rating classifier. They parsed movie reviews from IMDB and labeled strings of text as positive or negative according to various ordinal review systems. 
+ download: http://www.nltk.org/nltk_data/packages/corpora/movie_reviews.zip
+ source: http://www.cs.cornell.edu/people/pabo/movie-review-data/ 
+ readme (which contains much of our evaluation of this lexicon): http://www.cs.cornell.edu/people/pabo/movie-review-data/poldata.README.2.0.txt 

### Advantages of this lexicon
+ NLTK has built-in support for this corpus and trained models (http://www.nltk.org/nltk_data/).
+ It was easy to access within NLTK through the NLTK corpus downloader (http://www.nltk.org/data.html).
+ It labeled the samples in a simple and straightforward way, ‘pos’ and ‘neg’ making it useful for many types of classifiers. 
+ It was prepared and evaluated by industry recognized natural language experts.
+ The lexicon, and the research of its creators, is widely cited.

### Disadvantages of this lexicon
+ The original html files do not have consistent formats -- a review may not have the author's rating with it, and when it does, the rating can appear at different places in the file in different forms. They only recognize some of the more explicit ratings, which are extracted via a set of ad-hoc rules. This caused them to only choose reviews from certain sources.
+ Only the rating information upon which the rating decision was based is guaranteed to have been removed. Thus, if the original review contains several instances of rating information, potentially given in different forms, those not recognized as valid ratings remain part of the review text. This could cause classifiers to identify these ratings which could bias the models.
+ It only classifies text on a boolean scale, positive or negative. It does not distinguish extremes in any way. So a movie that is “kind of bad” and a movie that is “the worst movie of all time” are still put in the same category. A scale such as -4 to +4 may be more informative.
+ It is a relatively small training set (2,000) for this new era of big data.

## The method used to run sentiment analysis
We used the Naive Bayes Classifier implemented by NLTK (http://www.nltk.org/_modules/nltk/classify/naivebayes.html). As we learned in class, “Naive Bayes classifiers are a family of simple probabilistic classifiers based on applying Bayes' theorem with strong (naive) independence assumptions between the features. Naive Bayes is a simple technique for constructing classifiers: models that assign class labels to problem instances, represented as vectors of feature values, where the class labels are drawn from some finite set.” ~ http://en.wikipedia.org/wiki/Naive_Bayes_classifier

### Advantages of this method
+ It was simple to implement, especially given the classes provided by NLTK: http://www.nltk.org/howto/classify.html.
+ There is a lot of documentation and instruction on how to apply this type of classifier to natural language problems: e.g. http://www.nltk.org/book/ch06.html and http://streamhacker.com/2010/05/10/text-classification-sentiment-analysis-naive-bayes-classifier/
+ It runs incredibly fast. For the over 20,000 reviews we processed, it finishes within a minute on a single 8GB dual-core 64-bit operating system.
+ It reaches about 73% accuracy on a relatively small training set, which approaches human accuracy for classifying text agreeably (http://www.informationweek.com/software/information-management/expert-analysis-is-sentiment-analysis-an-80--solution/d/d-id/1087919). 
+ Every word gets an even say in determining which label should be assigned to a given input value.
+ Despite their naive design and apparently oversimplified assumptions, naive Bayes classifiers have worked quite well in many complex real-world situations. In 2004, an analysis of the Bayesian classification problem showed that there are sound theoretical reasons for the apparently implausible efficacy of naive Bayes classifiers. ~ Zhang, Harry. The Optimality of Naive Bayes. FLAIRS2004 conference.

### Disadvantages of this method
+ It does not account for the relationships between words. The naive independence of the classifier loses the structure of sentences. “One problem that arises is that the classifier can end up ‘double-counting’ the effect of highly correlated features, pushing the classifier closer to a given label than is justified.” ~ Section 5.4 http://www.nltk.org/book/ch06.html 
+ The ‘bag-of-words’ model is used (http://en.wikipedia.org/wiki/Bag-of-words_model). This has its advantages given its simplicity but it disregards grammar and word order. 
+ We do not have the multiplicity principle from the bag-of-words model. For each review, it only counts each word once. So if ‘hate’ appeared several times, this only accounts for it once. We lose term frequency in this implementation.
+ A comprehensive comparison with other classification algorithms in 2006 showed that Bayes classification is outperformed by other approaches, such as boosted trees or random forests. ~ Caruana, R.; Niculescu-Mizil, A. (2006). An empirical comparison of supervised learning algorithms. Proc. 23rd International Conference on Machine Learning. CiteSeerX: 10.1.1.122.5901.

## Descriptive statistics, accuracy, and error measures
We first assessed the model against training and test data. We first trained on 1500 instances and tested on 500 instances. Here are some statistics around the performance of our approach as provided by NLTK’s metrics package (http://www.nltk.org/api/nltk.metrics.html) and our classifiers utility class (http://www.nltk.org/_modules/nltk/classify/util.html).
+ Accuracy: 0.728
+ Our most informative features:
  + magnificent = True		pos : neg	=	15.0 : 1.0
  + outstanding = True		pos : neg	=	13.6 : 1.0
  + insulting = True		neg : pos	=	13.0 : 1.0
  + vulnerable = True		pos : neg	=	12.3 : 1.0
  + ludicrous = True		neg : pos	=	11.8 : 1.0
  + uninvolving = True		neg : pos	=	11.7 : 1.0
  + avoids = True			pos : neg	=	11.7 : 1.0
  + fascination = True		pos : neg	=	10.3 : 1.0
  + astounding = True		pos : neg	=	10.3 : 1.0
  + idiotic = True			neg : pos	=	9.8 : 1.0
+ Precision of identifying positive sentiment: 0.651595744680851
+ Recall for identifying positive sentiment: 0.98
+ F-measure of positive sentiment labeling: 0.7827476038338657
+ Precision of identifying negative sentiment: 0.9596774193548387
+ Recall for identifying negative sentiment:0.476
+ F-measure of negative sentiment labeling: 0.6363636363636364

After we were comfortable with our test results, we ran the model on our production data set gathered from the IMDb archive of the rec.arts.movies.reviews newsgroup, see http://www.cs.cornell.edu/people/pabo/movie-review-data/ and http://reviews.imdb.com/Reviews for more information. We were able to process a total of 21,707 movie reviews. Most of them resulted in positive sentiment. They were also mostly from certain years, biased by our data source.

![Total Negative Positive Sentiment](https://github.com/praeducer/big-data-analytics-for-competitive-advantage/blob/master/sentiment-analysis/TotalNegativePositiveSentiment.jpg "Total Negative Positive Sentiment")

![Sentiments Over Years](https://github.com/praeducer/big-data-analytics-for-competitive-advantage/blob/master/sentiment-analysis/SentimentsOverYears.jpg "Sentiments Over Years")

![Distribution Sentiments Over Years](https://github.com/praeducer/big-data-analytics-for-competitive-advantage/blob/master/sentiment-analysis/DistributionSentimentsOverYears.jpg "Distribution Sentiments Over Years")

## Evaluation of this approach
Much of the evaluation was already discussed under the advantages and disadvantages of our training lexicon and of our method. Here we will elaborate a little more and discuss our steps moving forward.

### How reliable and valid is it
Our accuracy is acceptable for such a naive approach. Our errors rates, though, varied greatly in quality depending on which measure we were examining. Please see our section on statistics above for the results of our calculations. Our model is excellent at identifying positive sentiment when it is present. Our 98% recall was great to see. The problem was that our classifier was overly optimistic, so to say. It often thought sentiment was positive when it was not, giving us barely over 65% precision for positive sentiment. On the flip-side to this, the classifier was not able to identify all of the positives because it labeled a good portion of them as negative. We had only 47% recall of negative sentiment. In the case of our negative sentiment precision, it was up there at almost 96%. This left us with few false positives in this case at least. Overall, not bad and plenty of room for improvement. Another good part about this classifier is that it is completely predictable and easily reproducible. It perform at this effectiveness every time. 

### How it could be improved
We would start by addressing the disadvantages mentioned in the bullets above. Given more time, there is a lot of testing we could do. Simply running through several methods and algorithms and comparing their accuracy and error measures would be an excellent start. To truly calculate if the sentiments are acceptable, it would be best to cross-reference our results with IMBd and Rotten Tomatoes ratings. 

Assuming we try to improve our approach with a naive bayes classifier:
+ We could take into account term frequency in our bag-of-words model.
+ Given a higher-quality, more diverse, and bigger lexicon, we could see even better results. 
+ We could pass in n-grams of words instead of single words. This may help establish meaningful relationships between the words. Even up to a trigram may have provided great results. 
+ We could remove words that proved not to be informative, or can typically be misleading, from the training set. Cleaning up the lexicon in general to prepare it for this specific type of classifier would be a great step.

If we are to test other methods:
+ We could run through the same type of approach but with other types of classifiers known to be more accurate such as random forests, boosted trees, or neural networks. 
+ Just like as above, with a higher-quality, more diverse, and bigger lexicon, we could see even better results. We could even test multiple approaches against multiple lexicons to see which combination is best.

## Early Challenges
We did attempt to use Rotten Tomatoes for gathering reviews for the films we were assessing in our prediction model. We planned to use their API since they do not allow web crawling, especially at high volumes. We began this approach after obtaining our developer keys. Our code for this could be found here: https://github.com/praeducer/big-data-analytics-for-competitive-advantage/blob/master/film-proposal/sentiment-analysis/download_rotten_reviews.py. We were also going to use Rotten Tomatoes for cross-referencing our sentiment results to help determine reliability. Despite what was claimed in their documentation as of April 2015 and earlier, http://developer.rottentomatoes.com/docs, the API is not free. After waiting many days for our developer keys to get approved, we emailed them to see what the delay was. As was discussed through email, they now charge for the API.
