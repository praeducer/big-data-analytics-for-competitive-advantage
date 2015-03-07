# description: Web mines urls for all films on wikipedia.
# output: .csv
# author: Paul Prae
# since: 3/7/2015
# tested with Python 3.3 on CentOS 7

import sys
from bs4 import BeautifulSoup
import urllib
import wikipedia

filename = './data/film_urls.csv'
outputFile = open(filename,'w');
outputFile.write('title,year,url,source\n');

wikipediaRoot = 'http://en.wikipedia.org';
listOfFilmsPath = '/wiki/List_of_films:';
# start here
currentListOfFilmsHref = listOfFilmsPath + '_numbers';
listOfFilmsURLs = [];
listOfFilmsURLs.append(wikipediaRoot + currentListOfFilmsHref);
listOfFilmsSoup = BeautifulSoup(urllib.request.urlopen(listOfFilmsURLs[0]));

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

# indexed by wikipedia URL to prevent duplicates
filmDataByURL = {};

for listOfFilmsURL in listOfFilmsURLs:
	listOfFilmsSoup = BeautifulSoup(urllib.request.urlopen(listOfFilmsURL));
	listOfFilmsITags = listOfFilmsSoup.findAll('i');
	for listOfFilmsITag in listOfFilmsITags:
		if listOfFilmsITag.a:
			filmTitle = listOfFilmsITag.a.get('title');
			iTagContents = listOfFilmsITag.parent.contents;
			if len(iTagContents) > 1:
				filmYear = listOfFilmsITag.parent.contents[1];
				filmYear = filmYear.replace(' ', '').replace('(','').replace(')','');
			else:
				filmYear = 'null';
			filmURL = wikipediaRoot + listOfFilmsITag.a.get('href');
			filmData = [{'title' : filmTitle}, {'year' : filmYear}, {'source' : listOfFilmsURL}];
			filmDataByURL[filmURL] = filmData;
	
		break;

# outputFile.write('\'' + filmTitle + '\'' + ',' + filmYear + ',' + filmUrl + ',' + currentListOfFilmsIndex + '\n');

outputFile.close();

