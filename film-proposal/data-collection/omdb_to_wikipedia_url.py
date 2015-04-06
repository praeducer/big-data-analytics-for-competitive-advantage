# description: takes in a list of movie titles and outputs a list of wikipedia URLs.
# input: The Open Movie Database's Database Dump. e.g. https://github.com/praeducer/big-data-analytics-for-competitive-advantage/blob/master/film-proposal/data-collection/data/omdb/test/omdbMovies_tiny_sample.txt
# file output: a .csv e.g. https://github.com/praeducer/big-data-analytics-for-competitive-advantage/blob/master/film-proposal/data-collection/data/wikipedia_urls.csv
# cmd line output: e.g. https://github.com/praeducer/big-data-analytics-for-competitive-advantage/blob/master/film-proposal/data-collection/data/cmd_output.txt
# author: Paul Prae
# since: 3/3/2015
# tested with Python 3.3 on CentOS 7 and Windows 8.1
# TODO: FIX RECURSIVE MADNESS
# TODO: Unit Test all strange cases. Will help this make more sense to others too.
# TODO: Rethink recursion for readability. 
# TODO: Way too many inputs to these functions. Simplify.
# TODO: This script needs to figure out if its OO or functional.

import sys
import csv
import operator
import codecs
import wikipedia
# TODO: Consider https://pypi.python.org/pypi/python-Levenshtein/ instead/as well for optimization of fuzz
import difflib
from fuzzywuzzy import fuzz

# returns a tuple of a url and its quality score.
# TODO: Make it explicitly separate to search a query directly versus its best match.
def bestURLSearch(queries, title):
	bestURLs = {}
	# get first query
	query = next (iter (queries.keys()))
	# Use recursion instead of for loop since queries changes over time.
	while query:
		printQuery(query, 'Searching best match: ')
		searchResults = wikipedia.search(query)
		if searchResults:
			bestURL, queries = findBestURL(query, queries, searchResults, title)
			if bestURL:
				bestURLs[bestURL[0]] = bestURL[1]
		# get next query. returns false if we are done.
		query = getNextQuery(queries)
	if bestURLs:
		bestURL = max(bestURLs.items(), key=operator.itemgetter(1))[0]
		return (bestURL, bestURLs[bestURL])
	return ()

def getNextQuery(queries):
	for query, beenQueried in queries.items():
		# If there are queries left to be queried.
		if not beenQueried:
			return query
	# If we make it to here, no more left.
	return False

# returns ((url, score), queries)
def findBestURL(query, queries, options, title):
	bestMatch = difflib.get_close_matches(query, options, 1)
	if bestMatch:
		# Make sure we have not already processed bestMatch before setting it to zero.
		if not bestMatch[0] in queries.keys():
			# Add best match to query list
			queries[bestMatch[0]] = 0
		# Because the match was recommended this guarantees a result.
		return findPageURL(bestMatch[0], queries, title)
	# 1 means true, it has been queried
	elif queries[query]:
		for option in options:
			print('\toption: ' + option)
			if 'film)' in option:
				return findPageURL(option, queries, title)
	else:
		print("\t! - No good match from search results. Using raw query.")
		# No guarantee we will find anything.
		return findPageURL(query, queries, title)
	return ((), queries)

# query param: (query, <0 or 1 depending if searched yet or not)
# returns ((url, score), queries)
def findPageURL(query, queries, title):
	# Do not find a page for a query if its been searched for already. Prevents redundant recursion.
	# 0 means it has not been queried. 
	if not queries[query]:
		printQuery(query, 'Finding page for: ')
		# mark as searched since we actually tried to find a page with it.
		queries[query] = 1
		try:
			page = wikipedia.page(query)
			if page:
				# first query is always the title we are looking for
				pageScore = scorePage( title, page)
				return ((page.url, pageScore), queries)
		except wikipedia.exceptions.PageError:
			pass
		except wikipedia.exceptions.DisambiguationError as e:
			print("\t! - DisambiguationError: Searching through other options.")
			return findBestURL(query, queries, e.options, title)
	return ((), queries)

def isTitleSimilarToPage(title, page, targetRatio):
	estimateTitleIsInSummary = fuzz.partial_ratio(title, page.summary)
	estimateTitleIsSimilar = fuzz.ratio(title, page.title)
	if estimateTitleIsInSummary > targetRatio or estimateTitleIsSimilar > targetRatio:
		return True
	else:
		print("\t! - This Wikipedia's page's title, " + str(estimateTitleIsSimilar) + ", and summary, " + str(estimateTitleIsInSummary) + ", were not similar to OMDB title.")
		return False

# Just return the highest score. This function can simply score a given page.
# TODO: if the title of the page has the exact title we are searching for plus (film) then give it a bonus.
# TODO: if the title of the page has the year we are looking for, provide another bonus.
def scorePage(title, page):
	return max( fuzz.partial_ratio(title, page.summary), fuzz.ratio(title, page.title))

def printQuery(query, message):
	try:
		print('\t' + message + query)
	except UnicodeEncodeError:
		print('\tquery: <UnicodeEncodeError during print. Search is fine.>')

if __name__=="__main__":
	outputFilename = './data/omdb/test/omdb_movies_wikipedia_urls_tiny_sample.csv'
	filmDataWriter = csv.writer(open(outputFilename,'w', encoding="utf8", newline=''), delimiter='\t')
	inputFilename = './data/omdb/test/omdbMovies_tiny_sample.txt'
	filmDataReader = csv.reader(open(inputFilename, encoding="utf8"),delimiter='\t')
	filmDataReader.__next__()
	urls = []
	lineCount = 0

	for line in filmDataReader:
		lineCount += 1
		print(' ~ ' + str(lineCount) + ' ~ ')
		title = line[2].strip('\n\r')
		titleFilm = title + ' (film)'
		queries = {title: 0, titleFilm: 0}
		# Start with two queries: one with (film) and one without. Run both and see which fuzzy score is better.
		# Highest scoring page found is the one we use the URL from. Save URL and score. N/A only if it was impossible to find any page at all.
		url = bestURLSearch(queries, title)
		if not url:
			print("\t! - No URL found")
			url = ('N/A', 0)
		print('\tresult-> ' + url[0] + ", " + str(url[1]))
		line.append(url)
		filmDataWriter.writerow(line)
