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

