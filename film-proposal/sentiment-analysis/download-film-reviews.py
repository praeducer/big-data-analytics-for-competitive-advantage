# TODO: Convince Rotten Tomatoes to let me use their API for less than $30,000 a year.
# TODO: FINISH
# description: pull film reviews from rotten tomatoes. store them locally.
# input: list of film titles and release years e.g. https://github.com/praeducer/big-data-analytics-for-competitive-advantage/blob/master/film-proposal/data-collection/data/film_data_part_2.csv
# output: a csv of the film title, film year, rotten tomatoes ID, and a string of all review quotes.
# author: Paul Prae (@praeducer)
# since: 4/12/2015

import sys
import csv
import requests

# TODO: consider doing the film review query in the same for loop for efficiency. 
# returns a list of film data: [(id, title, year, critics_consensus), ...]
def download_film_reviews(filmDataFilename):
	filmDataReader = csv.reader(open(filmDataFilename, encoding="utf8"))
	filmDataReader.__next__()
	count = 0
	for wikiFilmData in filmDataReader:
		count += 1
		title = wikiFilmData[0] if len(wikiFilmData) else None
		if title:
			title = title.replace("'", "").replace("(film)", "")
			year = wikiFilmData[3] if wikiFilmData[3] else None
			if year and str(year) in title:
				title = title.replace(str(year), "")
			title = title.replace("  ", " ").replace(")", "").replace("(", "")
			try:
				print(str(count) + " - " + title + " " + year)
				rottenFilmData = query_film(title, year)
			except UnicodeEncodeError:
				pass
		#rottenFilmData.extend(query_reviews(rottenFilmData[]))
		# add in Wikipedia URL for joining on to other data sources later. Also add on the levenstein distance of how similar the titles are
		#rottenFilmData.extend((wikiFilmData[], titleSimilarity)
		#write_film_data(rottenFilmData)

# TODO: have one for querying films and another for reviews. figure out what is the same between them.
# returns (id, title, year, critics_consensus, critics_rating, critics_score, audience_rating, audience_score)
def query_film(title, year=None):
	yearQuery = '+' + str(year) if year else ""
	titlePlus = title.replace(" ", "+")
	baseUrl = 'http://api.rottentomatoes.com/api/public/v1.0/movies.json'
	payload = {'apikey': getKey(), 'q': titlePlus + yearQuery, 'page_limit': 1}
	try:
		response = requests.get(baseUrl, params=payload)
		print("\tresponse -> " + response.text)
	except requests.exceptions.RequestException:
		print('Exception: Bad Request for ' + title + ' -> ' + response.url)
	sys.exit(0)

# return (numberOfQuotes, quote1|quote2|quote3, date1|date2|date3)
def query_reviews(id):
	print()

# write all rotten tomatoes data plus wikipedia URL and similarity score between titles.
# input (Wikipedia URL, id, title, year, critics_consensus)
def write_film_data(filmData, outputFileName):
	print()

def getKey():
	keyFile = open('rotten_key', encoding="utf8")
	return keyFile.readline()

if __name__=="__main__":

	inputFile = '../data-collection/data/film_data_part_2.csv'
	filmIndex = download_film_reviews(inputFile)