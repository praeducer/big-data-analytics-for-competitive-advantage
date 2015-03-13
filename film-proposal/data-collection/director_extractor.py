# description: Web mines a list of notable directors from Wikipedia and returns the results as an excel CSV file.
# output: .csv
# author: Daniel Joensen
# since: 3/12/2015
# tested with Python 3.4.2 on windows 7 Ultimate 64 bit

import sys
from bs4 import BeautifulSoup
import urllib
import wikipedia

#reates and opens the CSV file, as well as creates the column names.
filename = 'directors_list.csv'
outputFile = open(filename,'w');
outputFile.write('director name,url\n');

#constructs the wikipedia URL and soup.
wikipediaRoot = 'http://en.wikipedia.org';
directorPage = wikipediaRoot + '/wiki/Film_director';
directorSoup = BeautifulSoup(urllib.request.urlopen(directorPage));

#identifies the relevent table, and breaks out each row.
directorList = directorSoup.find('div',{ 'class' : 'div-col columns column-count column-count-2'});
directorListItems = directorList.find_all('li');


for item in directorListItems:	
	directorNameATag = item.find_next('a');
	directorName = directorNameATag['title'].replace('\'', '').replace(',', '').replace('.', '').replace('\u015b','s').replace('\u014d','s').replace('\u0159','r');
	directorURL = wikipediaRoot + directorNameATag['href'].replace(',', '');
	outputFile.write('\'' + directorName + '\'' + ',' + directorURL + '\'' + '\n');

outputFile.close();
