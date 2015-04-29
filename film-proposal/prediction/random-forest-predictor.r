# description: predict the revenue of films based on aspects of production using http://en.wikipedia.org/wiki/Random_forest.
# author: Ben Adelman (Original), Paul Prae
# since: 4/10/2015
# citation: inspired by a tutorial for a Kaggle competition written by Trevor Stephens: https://github.com/trevorstephens/titanic

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
full_data <- read.csv("./data/film_data.csv")
#possible_data <- read.csv("./data/possible_films.csv")

## adjusting some data types
full_data$Budget <- as.numeric(as.character(full_data$Budget))
full_data$Revenue <- as.numeric(as.character(full_data$Revenue))
full_data$Weekend_Total <- as.numeric(as.character(full_data$Revenue))

##  75% of the sample size for train (used for evaluation run, not final run)
smp_size <- floor(0.75 * nrow(full_data))

## set the seed to make your partition reproducible (a random number seed)
set.seed(123)
train_ind <- sample(seq_len(nrow(full_data)), size = smp_size)

##  now let's split into test vs. training data
train <- full_data[train_ind, ]
test <- full_data[-train_ind, ]

##  set up the random forest model for predicting Total Revenue
# configuratioin: as.numeric, importance=TRUE, ntree=2000
fit_Revenue <- randomForest(as.numeric(Revenue) ~ Budget + MPAA_Rating + Release_in_Winter + Release_in_Spring + Release_in_Summer + Release_in_Fall + Release_in_Holiday + Actor_Morgan_Freeman + Actor_Dennis_Hopper + Actor_Henry_Fonda + Actor_Bruce_Willis + Actor_Samuel_L__Jackson + Actor_Robert_De_Niro + Actor_Burt_Lancaster + Actor_Donald_Sutherland + Actor_Christopher_Lee + Actor_John_Wayne + Actor_Keanu_Reeves + Actor_Nick_Nolte + Actor_Nicolas_Cage + Actor_Gene_Hackman + Actor_Michael_Caine + Actor_Sean_Connery + Actor_Oliver_Hardy + Actor_Stan_Laurel + Actor_Robert_Duvall + Actor_Susan_Sarandon + Actor_Jack_Nicholson + Actor_Robert_Downey_Jr_ + Actor_Christopher_Walken + Actor_Willem_Dafoe + Actor_James_Stewart + Actor_Dustin_Hoffman + Actor_Robin_Williams + Actor_John_Goodman + Actor_Dennis_Quaid + Actor_Harvey_Keitel + Director_Blake_Edwards + Director_Sidney_Lumet + Director_Steven_Spielberg + Director_Spike_Lee + Director_John_Ford + Director_Robert_Altman + Director_Charlie_Chaplin + Director_Vincente_Minnelli + Director_Woody_Allen + Director_Clint_Eastwood + Director_Martin_Scorsese + Director_Ingmar_Bergman + Director_Howard_Hawks + Director_John_Huston + Director_Raoul_Walsh + Director_Chuck_Jones + Director_Werner_Herzog + Director_Fritz_Lang + Director_Steven_Soderbergh + Director_Michael_Curtiz + Director_Francis_Ford_Coppola + Director_Roger_Corman + Director_Alfred_Hitchcock + Director_Friz_Freleng + Director_Anthony_Mann + Director_Norman_Taurog + Director_Akira_Kurosawa + Genre_comedy + Genre_drama + Genre_romantic + Genre_science_fiction + Genre_crime + Genre_action + Genre_thriller + Genre_horror + Genre_animated, data=train, importance=TRUE, ntree=2000)

##  Now to make the prediction... using the model against the test data...
varImpPlot(fit_Revenue)
PredictionRevenue <- predict(fit_Revenue, test, OOB=TRUE, type = "response")
test$RevenuePrediction <- PredictionRevenue

write.csv(test, file = "./data/test_predictions.csv", row.names = TRUE)
