# Predicting the Features of a Film that Maximize ROI

R libraries used:
+	randomForest – This machine learning library was used to create the prediction model by generating a large number of random decision trees which were then used to train the predictive algorithm.

### generate-possible-films.py
Since we decided to use a decision tree to calculate the highest grossing film, we needed to generate all possible films we could propose. We decided to narrow it down based on several important features. Using combinatorics and Python, we combined these features in all possible unique ways.

#### Input
We created a series of matrices using lists and dictionaries in Python to represent all of the unique values. We then looped over all of them. Here were the starting values:
![Potential Film Features](https://github.com/praeducer/big-data-analytics-for-competitive-advantage/blob/master/prediction/data/input/PotentialFilmFeatures.PNG "Potential Film Features")

#### Output
possible_films.csv. The result was exactly 364,500 possibilities. 

### randomForest_model.r
For prediction we used the R programming language, specifically the Random Forest decision tree machine learning model.  We trained this model with a subset of our collected data using random_forest_predictor_testing.r and calculated its effectiveness. Once trained, we then processed our generated production data that contained all of the possibilities of a subset of our variables.  After running this data against our trained model, the sorted results yielded the final suggested set of variables to present to the Production Company. We predicted both Revenue and Opening Weekend Sales.

#### Input
+ For training: film_data.csv
+ For prediction: possible_films.csv

#### Output
New csv’s identical to the inputs but with new columns for Revenue and Opening Weekend Sales.

## Evaluating Our Model
Overview:
+ To provide a measure of how well observed outcomes are replicated by our model, we calculated the squared correlation coefficient. With an R-squared of 0.3485844, this means that about 35% of the variance of our model is explained.
+ Representative of our R-squared value, after plotting Estimated Revenue compared to Actual Revenue we can see that our predictions are somewhat inline with our observed values.
+ To measure the importance of our film features  (i.e. how much each variable influenced our prediction in a good way), we observed the increase in mean squared error. After plotting this for all variables, Budget is the most influential factor. Shortly following is having Steven Spielberg as a director and releasing in the summer, which are both attributes we settled on for our proposed film.
+ Another measure we used to understand the accuracy of our model was the normalized root-mean-square error (NRMSE). It is a frequently used measure of the differences between values predicted by a model or an estimator and the values actually observed. At about 8% NRMSE, we do not have much residual variance (i.e. unexplained variance) according to this metric.

### Measuring Variability: Squared Correlation Coefficient (R-squared)
To provide a measure of how well observed outcomes are replicated by our model, we calculated the squared correlation coefficient. We measured the variability of the data set using the total sum of squares formula (which is proportional to the variance of the data).

![Coefficient of determination](http://upload.wikimedia.org/math/6/7/9/67976e7df3f8a29ef9867a4a35e5c4db.png "Coefficient of determination")

~ http://en.wikipedia.org/wiki/Coefficient_of_determination

We know this formula is effective for linear regression models, which random forest algorithms can be. Using the programming language R, we calculated this as follows to assess our model:

> cor(RevenuePrediction, test$Revenue)^2

Our updated model produced the following value:
0.3485844

This means that about 35% of the variance of our model is explained. This is our ‘goodness of fit’, it describes how well our model fits the observations we provided. R-squared is the fraction by which the variance of the errors is less than the variance of the dependent variable. For such a complex model as ours, with 74 independent variables, I believe this to be a decent goodness of fit. This is especially true since this is only the second iteration of the first model we tried. It is low enough though that it warrants more experimentation, especially with other models and film feature sets.

### Estimated Revenue Compared to Actual Revenue
![Estimated Revenue Compared to Actual Revenue](https://github.com/praeducer/big-data-analytics-for-competitive-advantage/blob/master/prediction/data/output/estimated_revenue_vs_observed_numeric_minimal_pretty.png "Estimated Revenue Compared to Actual Revenue")

Representative of our R-squared value, we can see that our predictions are somewhat inline with our observed values. We need to be careful that the values we settle on for our proposed film are not so heavily influenced by the outliers. Removing these outliers and using more predictive features may improve this outcome further.

### Variable Importance: Mean Squared Error
To measure the importance of our film features  (i.e. how much each variable influenced our prediction in a good way), we observed the increase in mean squared error.

“The mean squared error (MSE) of an estimator measures the average of the squares of the ‘errors’, that is, the difference between the estimator and what is estimated. The difference occurs because of randomness or because the estimator doesn't account for information that could produce a more accurate estimate.”
If ![Vector of predictions](http://upload.wikimedia.org/math/f/3/e/f3e3835fc00ac33904a281e254e2580f.png "Vector of predictions") is a vector of *n* predictions, and ![Vector of true values](http://upload.wikimedia.org/math/5/7/c/57cec4137b614c87cb4e24a3d003a3e0.png "Vector of true values") is the vector of the true values, then the (estimated) MSE of the predictor is:

![mean squared error](http://upload.wikimedia.org/math/0/9/7/0978fe57785f6ce707efd6bd90550552.png "mean squared error")

~ http://en.wikipedia.org/wiki/Mean_squared_error

Luckily for us, this formula is built into the library that hosts our random forest implementation. This library calculates the increase in MSE of any given variable by taking that variable and assigning it random values to see how this random assignment affects the quality of the prediction. If the variable is important, these random variations of its values should inflict worse predictions. Otherwise, this random assignment would not have any effect and we can conclude this variable does not matter. So, if the model’s MSE goes up during the random permutation of this given variable, this means the model performed worse. The greater the value of the percentage increase in MSE, the better (i.e. the more important that variable is to making an accurate prediction).

We calculated this increase in MSE using the programming language R, as follows:
> varImpPlot(fit_Revenue, type=1)

This result is a plot of the most important variables:
![most important variables](https://github.com/praeducer/big-data-analytics-for-competitive-advantage/blob/master/prediction/data/output/incmse_numeric_minimal_columns.png "most important variables")

As you can see, Budget is the most influential factor. Shortly following is having Steven Spielberg as a director and releasing in the summer, which are both attributes we settled on for our proposed film. Even MPAA_Rating is up there. This is great news for us! These results definitely increase our confidence in our predictions.

## Another Measurement for Accuracy: Normalized Root-Mean-Square Error
Another measure we used to understand the accuracy of our model was the root-mean-square deviation (RMSD) or root-mean-square error (RMSE). 

“It is a frequently used measure of the differences between values (sample and population values) predicted by a model or an estimator and the values actually observed. Basically, the RMSD represents the sample standard deviation of the differences between predicted values and observed values.”
The RMSD of predicted values ![predicted values](http://upload.wikimedia.org/math/b/1/8/b1859f53476576f41148b5ef77bafa19.png "predicted values") for times *t* of a regression's dependent variable ![dependent variable](http://upload.wikimedia.org/math/4/1/5/415290769594460e2e485922904f345d.png "dependent variable") is computed for n different predictions as the square root of the mean of the squares of the deviations:

![root mean squared deviation](http://upload.wikimedia.org/math/1/7/3/173e0dd312ace976dbc640af8f9014b8.png "root mean squared deviation")

~ http://en.wikipedia.org/wiki/Root-mean-square_deviation

We executed this same formula in the programming language R:

> RMSE <- (sum((RevenuePrediction-test$Revenue)^2)/length(test$Revenue))^(1/2)

Our result was 161,201,459.

The fact that it is a large variation may be influenced by some outliers in our data and some huge blockbusters (think movies like Star Wars that have franchises). This, of course, is not as useful without placing it in the context of the magnitude of our values, which can get quite large themselves. The minimum and maximum values of our observed revenue variable are:

> maxRevenue <- max(test$Revenue)
> maxRevenue
[1] 2,064,855,361

> minRevenue <- min(test$Revenue)
> minRevenue
[1] 3,840.19
 
Using those values, we can effectively normalize the RMSE to make it easier to compare our results to other data sets and models.

“Normalizing the RMSD facilitates the comparison between datasets or models with different scales. Though there is no consistent means of normalization in the literature, the range of the measured data defined as the maximum value minus the minimum value is a common choice:

![normalized root mean squared deviation](http://upload.wikimedia.org/math/e/a/5/ea585ff954c73cc34084e4cee2693a4d.png "normalized root mean squared deviation")

This value is commonly referred to as the normalized root-mean-square deviation or error (NRMSD or NRMSE), and often expressed as a percentage, where lower values indicate less residual variance.”

~ http://en.wikipedia.org/wiki/Root-mean-square_deviation#Normalized_root-mean-square_deviation 

In the programming language R, we calculated this as follows:

> NRMSE <- (RMSE/(maxRevenue - minRevenue))
> NRMSE
[1] 0.07806927

At about 8%, we do not have much residual variance (i.e. unexplained variance). Using this measurement of accuracy, our model appears to be significantly better than what R2 estimated (it indicated 65% unexplained variance). One thing should be noted that each of the formulas used have several variations. There are even some formulas for R2 that incorporate MSE into it’s definition. Moving forward, other variations of the formulas could be tested and we could perform more research to see which formulas are the most valid ways to measure the performance of our model.
