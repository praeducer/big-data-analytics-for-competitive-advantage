# description: Accepts a film's URL and outputs the Director from Wikipedia
# author: Daniel Joensen
# since: 3/08/2015
# tested with Python 3.4.2 on windows 7 Ultimate 64 bit

import sys
from bs4 import BeautifulSoup
import urllib
import wikipedia

filmURLs = [
'http://en.wikipedia.org/wiki/Lovin%27_Molly',
'http://en.wikipedia.org/wiki/Maestro_(manga)',
'http://en.wikipedia.org/wiki/Manic_(film)',
'http://en.wikipedia.org/wiki/Max_(2002_film)',
'http://en.wikipedia.org/wiki/Merlin_(film)'
]

for filmURL in filmURLs:
	def director_extractor(filmURL):
		filmPageSoup = BeautifulSoup(urllib.request.urlopen(filmURL));
		summaryTable = filmPageSoup.find('table',{ 'class' : 'infobox vevent'});
		
		directorNames = [];

		try:
			summaryTableRows = summaryTable.find_all('tr');

			for row in summaryTableRows:
				if 'Directed' in row.text:
					directorNameATags = row.find_all('a');
					for tag in directorNameATags:
						if tag['href'][0] == "/":			
							directorName = tag['title'].replace(',','').replace('\'','').replace('"','');
							directorURL = tag['href'].replace(',','').replace('\'','').replace('"','');
							directorTuple = {'name': directorName, 'url': directorURL};
							directorNames.append(directorTuple);
		except AttributeError:
			directorNames.append("null");

		return directorNames;

	directorNames = director_extractor(filmURL);
	print(directorNames);
