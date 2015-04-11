# description: takes in a list of movie titles and outputs a list of wikipedia URLs and a confidence level.
# input: The Open Movie Database's Database Dump. e.g. https://github.com/praeducer/big-data-analytics-for-competitive-advantage/blob/master/film-proposal/data-collection/data/omdb/test/omdbMovies_tiny_sample.txt
# file output: a .csv e.g. https://github.com/praeducer/big-data-analytics-for-competitive-advantage/blob/master/film-proposal/data-collection/data/omdb/test/omdb_movies_wikipedia_urls_tiny_sample.csv
# cmd line output: e.g. https://github.com/praeducer/big-data-analytics-for-competitive-advantage/blob/master/film-proposal/data-collection/data/omdb/test/omdb_to_url_cmd_output.txt
# author: Paul Prae
# since: 3/3/2015
# tested with Python 3.3 on CentOS 7 and Windows 8.1
# Note: May want to comment out prints when running on Hadoop.
# TODO: Unit Test all strange cases. Will help this make more sense to others too.
# TODO: Optimize this. It can be slow over many records.
#	'Using slow pure-python SequenceMatcher. Install python-Levenshtein to remove this warning'
# TODO: Make confidence level more scientific. Basically, use solid reasoning behind bonuses.
# TODO: Abstract this away so it can be used to find articles about any topic given any kind of row by column input.

import sys
import csv
import operator
import codecs
import wikipedia
# TODO: Consider https://pypi.python.org/pypi/python-Levenshtein/ instead/as well for optimization of fuzz
import difflib
from fuzzywuzzy import fuzz

# returns a tuple of a url and its quality score.
def bestURLSearch(title, year):
	bestURLs = []
	queries = []

	# Start with two queries: one with (film) and one without. Run both and see which fuzzy score is better.
	titleWithFilm = title + ' (film)'
	# get wikipedia's best guess for both. appends (url, score). if nothing was found ('N/A', 0)
	bestURLs.append(findPageURL(title, title, year))
	queries.append(title)
	bestURLs.append(findPageURL(titleWithFilm, title, year))
	queries.append(titleWithFilm)

	# Lazy optimization
	# After some testing, this means about a perfect match.
	# We at least want 100 (exact title match in summary or page title) + the word 'film' and the film's release year in the summary bonuses, all divided by total possible points.
	desiredScore = 0.875
	currentBestURL, currentBestScore = max(bestURLs, key=operator.itemgetter(1))
	if currentBestScore >= desiredScore:
		return (currentBestURL, round(currentBestScore, 2))

	# get best options from a search with each
	titleBestOption = findBestOption(title, title)
	titleWithFilmBestOption = findBestOption(titleWithFilm, title)

	# search best options if they are not the same as queries we already searched for
	if titleBestOption and titleBestOption not in queries:
		bestURLs.append(findPageURL(titleBestOption, title, year))
		queries.append(titleBestOption)
	if titleWithFilmBestOption and titleWithFilmBestOption not in queries:
		bestURLs.append(findPageURL(titleWithFilmBestOption, title, year))
		queries.append(titleWithFilmBestOption)

	# there are some cases where the option has a film version
	if titleBestOption and 'film' not in titleBestOption:
		titleBestOptionWithFilm = titleBestOption + ' (film)'
		if titleBestOptionWithFilm not in queries:
			bestURLs.append(findPageURL(titleBestOptionWithFilm, title, year))
			#queries.append(titleBestOption)

	url, score = max(bestURLs, key=operator.itemgetter(1))
	return (url, round(score, 2))

# returns the best query to search
def findBestOption(query, title):
	searchResults = wikipedia.search(query)
	if searchResults:
		bestMatch = difflib.get_close_matches(title, searchResults, 1)
		if bestMatch:
			return bestMatch[0]
		else:
			# do our best
			for option in searchResults:
				if 'film' in option or title in option:
					return option
			# TODO: Does this ever return anything different than findPageURL?
			# if we found nothing at all similar in the options, trust wikipedia search and return the first result.
			return searchResults[0]
	return None

# returns (url, score)
def findPageURL(query, title, year):
	safePrint('\tFinding page for: ' + query)
	try:
		page = wikipedia.page(query)
		if page:
			pageScore = scorePage(page, title, year)
			# we made it! we at least have one to work with.
			return (page.url, pageScore)
	except wikipedia.exceptions.PageError:
		# nothing good will come of this. wikipedia thought nothing at all like this exists.
		pass
	except wikipedia.exceptions.DisambiguationError as e:
		# this would provide a list of options to search through (i.e. 'e.options') but our findBestOption function will find those.
		pass
	return ('N/A', 0)

# Just return the highest score. This function can simply score a given page.
# TODO: Find a way to make the bonus scores less arbitrary.
# TODO: Make confidence more scientific. 
def scorePage(page, title, year):
	defaultBonus = 10
	bonuses = []
	bonusToScore = {'filmInTitle': defaultBonus, 'filmInSummary': 20, 'yearInTitle': defaultBonus, 'yearInSummary': 20}
	pageScore = 0
	pageScore = max( fuzz.partial_ratio(title, page.summary), fuzz.ratio(title, page.title))

	if 'film' in page.title:
		bonuses.append('filmInTitle')
		pageScore += bonusToScore['filmInTitle']

	if 'film' in page.summary:
		bonuses.append('filmInSummary')
		pageScore += bonusToScore['filmInSummary']

	if str(year) in page.title:
		bonuses.append('yearInTitle')
		pageScore += bonusToScore['yearInTitle']

	if str(year) in page.summary:
		bonuses.append('yearInSummary')
		pageScore += bonusToScore['yearInSummary']

	pageConfidence = pageScore / (100 + sum(bonusToScore.values()))

	safePrint('\t\tPage Title-> ' + page.title)
	print('\t\tPage Bonus-> ' + ','.join(bonuses))
	safePrint('\t\tConfidence-> ' + str(pageConfidence))
	return pageConfidence

# not currently used but could be useful
def isTitleSimilarToPage(title, page, targetRatio):
	estimateTitleIsInSummary = fuzz.partial_ratio(title, page.summary)
	estimateTitleIsSimilar = fuzz.ratio(title, page.title)
	if estimateTitleIsInSummary > targetRatio or estimateTitleIsSimilar > targetRatio:
		return True
	else:
		print("\t! - This Wikipedia's page's title, " + str(estimateTitleIsSimilar) + ", and summary, " + str(estimateTitleIsInSummary) + ", were not similar to OMDB title.")
		return False

# a little redundant but handles that exception at least (happens on Windows)
def safePrint(message):
	try:
		print(message)
	except UnicodeEncodeError:
		print('\tsafePrint: <UnicodeEncodeError during print. Search is fine.>')

def mapper(line):
	title = line[2].strip('\n\r')
	year = line[3]
	# Highest scoring page found is the one we use the URL from. Save URL and score. N/A only if it was impossible to find any page at all.
	url = bestURLSearch(title, year)
	if not url:
		print("\t! - No URL found")
		url = ('N/A', 0)
	print('\tresult-> ' + url[0] + ", " + str(url[1]))
	line.extend(url)
	return line

if __name__=="__main__":
	outputFilename = './data/omdb/test/omdb_movies_wikipedia_urls_tiny_sample_map_test.csv'
	filmDataWriter = csv.writer(open(outputFilename,'w', encoding="utf8", newline=''), delimiter='\t')
	inputFilename = './data/omdb/test/omdbMovies_tiny_sample.txt'
	filmDataReader = csv.reader(open(inputFilename, encoding="utf8"),delimiter='\t')
	filmDataReader.__next__()
	urls = []
	lineCount = 0

	for line in filmDataReader:
		lineCount += 1
		print(' ~ ' + str(lineCount) + ' ~ ')
		extendedLine = mapper(line)
		filmDataWriter.writerow(extendedLine)
