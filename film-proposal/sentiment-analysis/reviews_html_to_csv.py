# description: Pull film and review data from html files stored locally.
# authors: Paul Prae, Daniel Joensen
# since: 3/08/2015
# note: tested with Python 3.3 on CentOS 7 and Windows 8 (64 bit)
# data provided by: Bo Pang and Lillian Lee from their 2004 Sentiment Analysis research at Cornell. http://www.cs.cornell.edu/people/pabo/movie-review-data/
# data set: Polarity dataset (Pool of 27886 unprocessed html files). http://www.cs.cornell.edu/people/pabo/movie-review-data/polarity_html.zip
# TODO: Figure out regex for year
# TODO: Pull out review text

import os
import re
import sys
from bs4 import BeautifulSoup
import csv
import ntpath

def mapper(fullFilmFilePath):
	try:
		filmPage = open(fullFilmFilePath, encoding="utf8")
	except IsADirectoryError:
		return None
	try:
		filmPageSoup = BeautifulSoup(filmPage.read())
	# TODO: Handle or prevent this for real. We lose a sizable subset of the reviews because of this.
	# TODO: Try ascii encoding.
	except UnicodeDecodeError:
		print("\tUnicodeDecodeError!")
		return None
	filmFileName = ntpath.basename(fullFilmFilePath)
	filmFileID = os.path.splitext(filmFileName)[0]

	titleTagContents = filmPageSoup.find('h1').find('a').string # alternate: filmPageSoup.title.string
	# year = ''.join(filter(lambda char: char.isdigit(), titleTagContents)); # won't work for title with digits
	inParenRegex = re.compile('(?<=\().+?(?=\))') # wut: ('\(([^\)]+)\)')
	year = inParenRegex.match(titleTagContents)
	if year:
		year = year.group()
	title = titleTagContents.split('(', 1)[0]
	title = title.replace(',','').replace('\'','').replace('"','').rstrip()

	return [filmFileID, title, year]#, review]

def loop_local(inputDirectory, outputFile):
	filmWriter = csv.writer(open(outputFile, 'w', newline='', encoding="utf8"))
	filmWriter.writerow(['id', 'title', 'release year', 'review'])

	filmFiles = os.listdir(inputDirectory)
	count = 0

	for filmFileName in filmFiles:
		count += 1
		print(str(count) + ' - ' + filmFileName)
		fullFilmFilePath = inputDirectory + filmFileName
		filmRow = mapper(fullFilmFilePath)
		if filmRow:
			filmWriter.writerow(filmRow)
			print(filmRow)
		sys.exit(0)


if __name__=="__main__":

	inputDirectory = './data/movie/'
	outputFile = './data/film_review_data.csv'

	loop_local(inputDirectory, outputFile)
