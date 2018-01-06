# Big Data Analytics For Competitive Advantage
Work from a course titled, "Big Data Analytics For Competitive Advantage". This course provides an introduction to the use of big data analytics as a strategic resource in creating competitive advantage for businesses. A focus is placed on integrating the knowledge of analytics tools with an understanding of how companies could leverage data analytics to gain strategic advantage. An emphasis is placed on developing the ability to think critically about complex problems/questions in real world data science and business analytics challenges.

## Course Objectives
1. Understand the role of big data analytics in organizational strategy and how organizations can
leverage useful data/information to gain competitive advantage and acquire insights.
2. Gain an introductory knowledge of the data science and business analytics tools that are useful in
extracting intelligence and value from data.
3. Apply big data analytics tools to reveal business opportunities and threats.
4. Using actual business cases/examples, develop data-driven strategies that enhance stakeholder
relationships, open new market opportunities, and/or better position the organization for
competitive advantage during industry transition.

# Term Project Overview
###### Predicting the Features of a Film that Maximize ROI
## Business Need
Understand trends in the film industry in order to use predictive analysis to determine what type of movie will yield the highest return on investment.

## Conclusion
Assuming a $100MM budget, our predicted successful film is a science fiction movie starring Samuel L. Jackson directed by Steven Spielberg released in the summer.

## Tools used
+ Data Sources - Wikipedia, Box Office Mojo, Rotten Tomatoes
+ Processing Platform - A Linux (CentOS) instance hosted on Amazon EC2 
+ Data Storage - Microsoft Excel or CSV’s on a local file system
+ Data Mining and Processing - Python 3 (Main libraries: BeautifulSoup, Wikipedia, NLTK, urllib, requests)
+ Data Transformation and Analysis - Microsoft Excel, SAS
+ Data Vizualization – Tableau, Microsoft Excel
+ Predictive Modeling - R
+ Version Control - Git

## Data Collection Summary
Using Python, we performed the following steps:

1. Created a primary list of all movies listed in the alphabetical indexes found in the following link: http://en.wikipedia.org/wiki/Lists_of_films#Alphabetical_indices.
2. Downloaded each movie page locally to prevent repeated web requests.
3. Extracted the relevant data fields by web mining the local files. Most of the data was extracted from Wikipedia’s Summary table from the HTML source of the film’s Wikipedia page. Increased speed of our data collection script by following a MapReduce paradigm. Fields extracted from Wikipedia:
    1. Release Date
    2. Budget
    3. Revenue
    4. Director(s)
    5. Starring Actors(s)
    6. Production Company(s)
4. We still needed to extract Genre for each movie, which was more challenging due to the fact that it was contained within the text of the Wikipedia page itself.  We used Python to perform some basic natural language processing. Here were our steps:
    1. Target the introductory paragraph on each film’s Wikipedia page
    2. Split the paragraph into sentences
    3. Target the first sentence of the paragraph, where the Genre name was commonly found
    4. Remove any non-alphabetical characters
    5. Split that sentence into words
    6. Check that list of words against a list of Genres
    7. Return the word if a match was found
5. Web mined additional data fields from Box Office Mojo (IMDB): 
    1. Created a primary list of film urls listed on Box Office Mojo’s alphabetical index.
    2. Visited each film page and extracted the following fields:
        1. Movie name
        2. MPAA rating
        3. Run time
        4. Opening Weekend total sales
        5. Domestic total sales
        6. Global total sales
        7. Number of theaters (widest release)
        8. Release date.
6. After the film data extraction, we stored each movie as a row and each associated piece of data as a column in a CSV.
7. Web mined lists (saved initially as CSV’s) of notable actors, producers, and directors found at the URL’s listed below. These lists were gathered and stored as separate tables in the Excel database for later analysis:
    1. Actors - http://en.wikipedia.org/wiki/Screen_Actors_Guild_Award
    2. Producers - http://en.wikipedia.org/wiki/List_of_film_production_companies
    3. Directors - http://en.wikipedia.org/wiki/Film_director
8. Finally, SAS was used to clean some of the data (e.g. to remove single quotes, duplicates, etc.), to create our Excel Database, and to create a sample report.

## Data Processing and Analysis Summary:
1. We used SAS to: reformat data; parse and create flags (0/1) forexistence of notable directors, producers, and actors; generate the updated Excel database.
2. Our next challenge was joining the two datasets together (Wikipedia and Box Office Mojo), which we accomplished using SAS and the film title and release year fields.
3. Once the datasets were combined into a single database, we manually cleaned up any fields that did not have complete data.  We removed rows based on the following criteria: no match in the Box Office Mojo dataset, missing Revenue or Budget fields, missing predictive fields.
4. After the final dataset was created, we used R to run a random forest predictive model on a number of key fields. We created a training and test dataset using the final version of our Excel database.
5. Once the predictive model was trained, we used Python to generate a very large dataset containing all possible combinations of our chosen genres, directors, release seasons, MPAA ratings, and budgets.
6. To arrive at our final predictions we passed the generated dataset through the predictive model that was trained on our original data and then sorted by predicted global total revenue to see which combination of characteristics combined to yield the highest revenue. We did the same for opening weekend sales.
7. To perform sentiment analysis, we extracted the review text, film title, and film year from a pool of 27,886 HTML files from the IMDB archive.
8. We then created and evaluated a Naïve Bayes Classifier written in Python that assigns positive or negative sentiment to lists of text.
9. Once trained and tested, we ran the classifier over the unlabeled reviews from IMDB’s archives. The results were then joined to our final Excel database.
