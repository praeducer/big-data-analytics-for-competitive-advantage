# description: predict the revenue of films based on aspects of production using http://en.wikipedia.org/wiki/Random_forest.
# author: 

library(rpart)
install.packages('rattle')
install.packages('rpart.plot')
install.packages('RColorBrewer')
library(rattle)
library(rpart.plot)
library(RColorBrewer)
install.packages('randomForest')
library(randomForest)
install.packages('party')
library(party)

##  load the full file into R
full_data <- read.csv("./data/test_film_data.csv")

## trying to handle/correct some data types
full_data$Release_Date <- as.Date(full_data$Release_Date, "%m/%d/%Y")
full_data$Budget <- as.numeric(as.character(full_data$Budget))
full_data$Revenue <- as.numeric(as.character(full_data$Revenue))

##  now let's split into test vs. training data
##  75% of the sample size for train
smp_size <- floor(0.75 * nrow(full_data))

## set the seed to make your partition reproductible (a random number seed)
set.seed(123)
train_ind <- sample(seq_len(nrow(full_data)), size = smp_size)

train <- full_data[train_ind, ]
test <- full_data[-train_ind, ]

##  set up the random forest model for predicting ROI
#fit_ROI <- randomForest(as.factor(ROI) ~ release_year + Budget + Revenue + Release.Day.of.Week + Notable_Actor + Notable_Director + Notable_Production_co + Genre_comedy + Genre_drama, data=train, importance=TRUE, ntree=2000)

##  set up the random forest model for predicting Total Sales 
fit_Sales <- randomForest(as.factor(Revenue) ~ release_year + Budget + Release.in.Winter + Release.Day.of.Week + Release.in.Spring + Release.in.Summer + Release.in.Fall + Release.in.Holiday + Notable_Actor + Notable_Director + Notable_Production_co + Genre_comedy + Genre_drama, data=train, importance=TRUE, ntree=2000)

##  set up the random forest model for predicting Opening Weekend
#fit_OpenWkend <- randomForest(as.factor(Opening_Weekend) ~ release_year + Budget + Revenue + Release.in.Winter + Release.Day.of.Week + Release.in.Spring + Release.in.Summer + Release.in.Fall + Release.in.Holiday + Notable_Actor + Notable_Director + Notable_Production_co + Genre_comedy + Genre_drama, data=train, importance=TRUE, ntree=2000)

##  Now to make the prediction... using the model against the test data...
#PredictionROI <- predict(fit_ROI, test, OOB=TRUE, type = "response")
#test$ROIPrediction <- PredictionROI

PredictionRevenue <- predict(fit_Sales, test, OOB=TRUE, type = "response")
test$PredictedRevenue <- PredictionRevenue

## submit <- data.frame(Row.name = test$row.names, ROI = Prediction)
write.csv(test, file = "PredictedRevenue.csv", row.names = TRUE)