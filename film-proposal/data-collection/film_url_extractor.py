# description: Web mines actors that won an outstanding performance award from the screen actors guild.
# output: .csv
# author: Paul Prae
# since: 2/21/2015
# tested with Python 3.3 on CentOS 7

import sys
from bs4 import BeautifulSoup
import urllib
import wikipedia

filename = './data/film_urls.csv'
outputFile = open(filename,'w');
outputFile.write('title,year,url,group\n');

wikipediaRoot = 'http://en.wikipedia.org/wiki/';
listOfFilmsPrefix = wikipediaRoot + 'List_of_films:';
# start here
currentListOfFilmsIndex = '_numbers';
currentListOfFilmsURL = listOfFilmsPrefix + currentListOfFilmsIndex;
listOfFilmsSoup = BeautifulSoup(urllib.request.urlopen(currentListOfFilmsURL));

filmIndexTable = listOfFilmsSoup.find('table', { 'class' : 'wikitable'});

print(filmIndexTable);	

# outputFile.write('\'' + filmTitle + '\'' + ',' + filmYear + ',' + filmUrl + ',' + currentListOfFilmsIndex + '\n');

outputFile.close();

