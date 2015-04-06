Data pulled from "The Open Movie Database", http://www.omdbapi.com/. It was pulled through their "Monthly Database Dump", http://beforethecode.com/projects/omdb/download.aspx.

# IMDB and Rotten Tomatoes Data Dump
Using OMDB, I acquired a database dump of 952,449 international films from IMDB, http://www.imdb.com/. It includes data such as Title, IMDB Rating, Release Date, Genre, Director, Cast, Plot and more. They are all laid out in a tab separated format. This is an insane amount of information to get creative with! We could even do some natural language processing with IBM Watson on the 'Plot' text (imagine assessing the personality of each movie: https://www.ibm.com/smarterplanet/us/en/ibmwatson/developercloud/personality-insights.html). So much potential here.

Along with this data, we have 95,287 films from Rotten Tomatoes, http://www.rottentomatoes.com/. This data contains many different kinds of ratings and user reviews, though is sparse. Lots of sentiment to analyze regardless! Note: I have not tried yet, but it looks like we can join IMDB up to Rotten Tomatoes using the 'ID' column. 

Besides the full set, I broke the data up into smaller samples for experimenting with.

Have fun!
