# description: pull film reviews from rotten tomatoes. store them locally.
# input: list of film titles and release years e.g. https://github.com/praeducer/big-data-analytics-for-competitive-advantage/blob/master/film-proposal/data-collection/data/film_data_part_2.csv
# output: a csv of the film title, film year, rotten tomatoes ID, and a string of all review quotes.
# author: Paul Prae (@praeducer)
# since: 4/12/2015
# TODO: test

import sys
import csv
import requests

# TODO: consider doing the film review query in the same for loop for efficiency. 
# returns a list of film data: [(id, title, year, critics_consensus), ...]
def build_film_index(inputFile):
	films = []
	filmDataReader = csv.reader(open(filmDataFilename, encoding="utf8"));
	filmDataReader.__next__();
	count = 0;
	for filmData in filmDataReader:
		count += 1;
		title = filmData[0];
		year = filmData[3];
		filmData = query_film(title, year)


# TODO: have one for querying films and another for reviews. figure out what is the same between them.
# returns (id, title, year, critics_consensus)
def query_film(title, year=None):
	yearQuery = '+' + str(year) if year else ""
	# TODO: never share. link to local file that is gitignored
	secret = ""
	titlePlus = title.replace(" ", "+")
	url = 'http://api.rottentomatoes.com/api/public/v1.0/movies.json?apikey=' + secret + '&q=' + titlePlus + yearQuery + '&page_limit=1'
	# TODO: URL encode
	try:
		response = requests.get(url)
	except requests.exceptions.RequestException:
		print('Exception: Bad Request for ' + title + ' -> ' + url);

if __name__=="__main__":

	inputFile = '../data-collection/data/film_data_part_2.csv'
	filmIndex = build_film_index(inputFile)