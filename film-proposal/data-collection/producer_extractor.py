# description: Web mines producers from Wikipedia and returns the results as an excel CSV file.
# output: .csv
# original author: Paul Prae
# modifications by: Daniel Joensen
# since: 3/02/2015
# tested with Python 3.4.2 on windows 7 Ultimate 64 bit

import sys
from bs4 import BeautifulSoup
import urllib
import wikipedia

#creates and opens the CSV file, as well as creates the column names.
filename = 'producers_list.csv'
outputFile = open(filename,'w');
outputFile.write('company,url\n');

#constructs the wikipedia URL and soup.
wikipediaRoot = 'http://en.wikipedia.org';
producersPage = wikipediaRoot + '/wiki/List_of_film_production_companies';
producersSoup = BeautifulSoup(urllib.request.urlopen(producersPage));

#identifies the relevent table, and breaks out each row.
producersTable = producersSoup.find('table',{ 'class' : 'wikitable sortable'});
producersTableRows = producersTable.find_all('tr');

for rows in producersTableRows:	
	#loops through the rows in the table, pulls out the "a" tags, constructs the name and URL, and then writes each to the excel file.
	producerNameATag = rows.find_next('a'); 
	producerName = producerNameATag['title'].replace('\'', '').replace(',', '').replace('.', '');
	producerURL = wikipediaRoot + producerNameATag['href'].replace(',', '');
	outputFile.write('\'' + producerName + '\'' + ',' + producerURL + '\'' + '\n');

outputFile.close();
