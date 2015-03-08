# description: Accepts a film's URL and outputs the Director from Wikipedia
# author: Daniel Joensen
# since: 3/0/2015
# tested with Python 3.4.2 on windows 7 Ultimate 64 bit

import sys
from bs4 import BeautifulSoup
import urllib
import wikipedia

filmURLs = [
'http://en.wikipedia.org/wiki/Planes_(film)'
]

for filmURL in filmURLs:
	def director_extractor(filmURL):
		filmPageSoup = BeautifulSoup(urllib.request.urlopen(filmURL));
		summaryTable = filmPageSoup.find('table',{ 'class' : 'infobox vevent'});
		summaryTableRows = summaryTable.find_all('tr');

		directorNames = [];

		for row in summaryTableRows:
			if 'Directed' in row.text:
				directorNameATags = row.find_all('a');
				#print(directorNameATags);
				for tag in directorNameATags:
					directorName = tag['title'];
					directorNames.append(directorName);

		return directorNames;

	directorNames = director_extractor(filmURL);
	print(directorNames);
