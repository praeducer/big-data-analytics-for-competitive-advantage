# description: Web mines urls for all films on wikipedia.
# output: .csv
# author: Paul Prae
# since: 3/7/2015
# tested with Python 3.3 on CentOS 7

import sys
from bs4 import BeautifulSoup
import urllib
import wikipedia

def parseFilmIndex(startURL):
	listOfFilmsURLs = [];
	listOfFilmsURLs.append(startURL);
	listOfFilmsSoup = BeautifulSoup(urllib.request.urlopen(startURL));
	filmIndexTable = listOfFilmsSoup.find('table', { 'class' : 'wikitable'});
	filmIndexTableRows = filmIndexTable.findAll('tr');
	for filmIndexTableRow in filmIndexTableRows:
		filmIndexTableCols = filmIndexTableRow.findAll('td');
		for filmIndexTableCol in filmIndexTableCols:
			filmIndexTableColATag = filmIndexTableCol.find('a');
			if filmIndexTableColATag:
				filmIndexHref = filmIndexTableCol.find('a').get('href'); 
				if listOfFilmsPath in filmIndexHref:
					listOfFilmsURLs.append(wikipediaRoot + filmIndexHref);
	return listOfFilmsURLs;

def parseAllFilmPages(listOfFilmsURLs):
	# indexed by wikipedia URL to prevent duplicates
	filmDataByURL = {};

	for listOfFilmsURL in listOfFilmsURLs:
		listOfFilmsSoup = BeautifulSoup(urllib.request.urlopen(listOfFilmsURL));
		listOfFilmsITags = listOfFilmsSoup.findAll('i');
		for listOfFilmsITag in listOfFilmsITags:
			if listOfFilmsITag.a:
				filmData = parseITag(listOfFilmsITag);
				filmDataByURL[filmData['url']] = filmData;
	return filmDataByURL;

# PullData we need out of the <i> tag in the soup object. return list with url, title, and date.
def parseITag(iTag):
	listOfFilmsITag = iTag;
	filmTitle = listOfFilmsITag.a.get('title');
	filmTitle = filmTitle.replace(',','').replace('\'','').replace('"','');
	filmYear = '';
	iTagParentContents = listOfFilmsITag.parent.contents;
	if len(iTagParentContents) > 1:
		filmYear = iTagParentContents[1];
		# Make sure it is just the year (no letters or special chars)
		filmYear = ''.join(filter(lambda char: char.isdigit(), filmYear));
	if not filmYear and len(iTagParentContents) > 2:
		filmYear = iTagParentContents[2].contents[0];
		filmYear = ''.join(filter(lambda char: char.isdigit(), filmYear));
#	elif not filmYear:
#		iTagSibling = listOfFilmsITag.next_sibling
#		print(filmTitle);
#		if iTagSibling:
#			filmYear = iTagSibling.contents[0];
#			filmYear = ''.join(filter(lambda char: char.isdigit(), filmYear));
#			print(filmYear);
	if not filmYear:
		filmYear = 'null';
	filmURL = wikipediaRoot + listOfFilmsITag.a.get('href');
	filmURL = filmURL.replace(',','');
	filmData = {'url' : filmURL, 'title' : filmTitle, 'year' : filmYear};
	return filmData;

if __name__=="__main__":

	filename = './data/film_urls.csv'
	outputFile = open(filename,'w');
	outputFile.write('url,title,year\n');

	wikipediaRoot = 'http://en.wikipedia.org';
	listOfFilmsPath = '/wiki/List_of_films:';
	startListOfFilmsHref = listOfFilmsPath + '_numbers';
	startListOfFilmsURL = wikipediaRoot + startListOfFilmsHref;
	listOfFilmsURLs = parseFilmIndex(startListOfFilmsURL);
	filmDataByURL = parseAllFilmPages(listOfFilmsURLs);

	# Had to add this extra for loop and a dict because there were duplicate links
	for filmURL, filmData in filmDataByURL.items():
		filmTitle = filmData['title'];
		filmYear = filmData['year'];
		outputFile.write( filmURL + ',' + '\'' + filmTitle + '\'' + ',' + filmYear + '\n');

	outputFile.close();


