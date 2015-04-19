# description: Pull film and review data from html files stored locally.
# authors: Paul Prae, Daniel Joensen
# since: 3/08/2015
# note: tested with Python 3.3 on CentOS 7 and Windows 8 (64 bit)
# data provided by: Bo Pang and Lillian Lee from their 2004 Sentiment Analysis research at Cornell. http://www.cs.cornell.edu/people/pabo/movie-review-data/
# data set: Polarity dataset (Pool of 27886 unprocessed html files). http://www.cs.cornell.edu/people/pabo/movie-review-data/polarity_html.zip
# Note: There can be multiple reviews for each film
# TODO: Consider extracting out meta data. e.g.:
'''
<PRE>==========
X-RAMR-ID: 29870
X-Language: en
X-RT-ReviewID: 256672
X-RT-TitleID: 1110296
X-RT-SourceID: 595
X-RT-AuthorID: 1146</PRE>
'''

import os
import re
import sys
from bs4 import BeautifulSoup
import csv
import ntpath
import string

# TODO: break into find_year, find_title, find_review etc.
def mapper(fullFilmFilePath):
	try:
		filmPage = open(fullFilmFilePath, encoding="utf8")
	except IsADirectoryError:
		return None

	filmFileName = ntpath.basename(fullFilmFilePath)
	filmFileParts = os.path.splitext(filmFileName)
	filmFileID = filmFileParts[0]
	filmExtension = filmFileParts[1]

	if filmExtension != '.html':
		return None

	try:
		filmPageSoup = BeautifulSoup(filmPage.read())
	# TODO: Handle or prevent this for real. We lose a sizable subset of the reviews because of this.
	# TODO: Try ascii encoding.
	except UnicodeDecodeError:
		print("\tUnicodeDecodeError!")
		return None

	if not filmPageSoup:
		return None

	titleTagContents = None
	filmPageH1Tag = filmPageSoup.find('h1')
	if filmPageH1Tag:
		filmPageATag = filmPageH1Tag.find('a')
		if filmPageATag:
			titleTagContents = filmPageATag.string # alternate: filmPageSoup.title.string
	if not titleTagContents and filmPageSoup.title:
		titleTagContents = filmPageSoup.title.string

	year = None
	title = None
	if titleTagContents:
		# matches any four digit sequence (year) in parentheses
		inParenRegex = re.compile('\([0-9][0-9][0-9][0-9]\)')
		year = re.search(inParenRegex, titleTagContents)
		if year:
			year = year.group()
			# digits only
			year = ''.join(filter(lambda char: char.isdigit(), year))
		title = titleTagContents.split('(', 1)[0]
		title = title.replace(',','').replace('\'','').replace('"','').rstrip()

	filmPagePTags = filmPageSoup.findAll('p')
	review = ""
	totalPTagsLeft = len(filmPagePTags)
	# Concat the strings from every P tags except the last two which 
	for pTag in filmPagePTags:
		if pTag.string:
			review += pTag.string
			review += " "
			totalPTagsLeft -= 1
		# last two appear to be unnecessary meta data
		if totalPTagsLeft < 3:
			break

	# matches only alphanumeric chars
	alphaNumRegex = re.compile('[\W]+')
	review = alphaNumRegex.sub(' ', review)
	review = review.replace('  ',' ').rstrip().lstrip()

	if not filmFileID:
		filmFileID = 'null'
	if not title:
		title = 'null'
	if not year:
		year = 'null'
	if not review:
		review = 'null'

	return [filmFileID, title, year, review]

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

if __name__=="__main__":

	inputDirectory = './data/movie/'
	outputFile = './data/film_review_data.csv'

	loop_local(inputDirectory, outputFile)
