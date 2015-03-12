# description: Accepts a film's URL and outputs the Director from Wikipedia
# author: Daniel Joensen
# since: 3/08/2015
# tested with Python 3.4.2 on windows 7 Ultimate 64 bit

import sys
from bs4 import BeautifulSoup
import urllib
import wikipedia

filmURLs = [
'http://en.wikipedia.org/wiki/Dutch_(film)',
'http://en.wikipedia.org/wiki/Robots_(2005_film)',
'http://en.wikipedia.org/wiki/Deep_Rising',
'http://en.wikipedia.org/wiki/Rob_Roy_(1995_film)',
'http://en.wikipedia.org/wiki/I_Robot_(film)',
'http://en.wikipedia.org/wiki/Charlie%27s_Angels_(film)',
'http://en.wikipedia.org/wiki/The_More_the_Merrier',
'http://en.wikipedia.org/wiki/Stroker_Ace',
'http://en.wikipedia.org/wiki/All_or_Nothing_(film)',
'http://en.wikipedia.org/wiki/Highway_61_(film)',
'http://en.wikipedia.org/wiki/The_Reckoning_(2003_film)',
'http://en.wikipedia.org/wiki/Gleaming_the_Cube'
]


wikipediaRoot = 'http://en.wikipedia.org';

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
					if not directorNameATags:
						directorName = row.text.replace(',','').replace('\'','').replace('"','').replace('\u014d','o');
						directorName = directorName.replace('\n','').replace('Directed by','');
						directorURL = 'null'
						directorTuple = {'name': directorName, 'url': directorURL};
						directorNames.append(directorTuple);
					else:
						for tag in directorNameATags:
							if tag['href'][0] == "/":			
								directorName = tag['title'].replace(',','').replace('\'','').replace('"','').replace('\u014d','o');
								directorURL = wikipediaRoot + tag['href'].replace(',','').replace('\'','').replace('"','');
								directorTuple = {'name': directorName, 'url': directorURL};
								directorNames.append(directorTuple);
		except (AttributeError, UnicodeEncodeError) as e:
			directorNames.append("null");

		return directorNames;


	def actor_extractor(filmURL):
		filmPageSoup = BeautifulSoup(urllib.request.urlopen(filmURL));
		summaryTable = filmPageSoup.find('table',{ 'class' : 'infobox vevent'});
		
		actorNames = [];

		try:
			summaryTableRows = summaryTable.find_all('tr');

			for row in summaryTableRows:
				if 'Starring' in row.text:
					actorNameATags = row.find_all('a');
					for tag in actorNameATags:
						if tag['href'][0] == "/":			
							actorName = tag['title'].replace(',','').replace('\'','').replace('"','');
							actorURL = wikipediaRoot + tag['href'].replace(',','').replace('\'','').replace('"','');
							actorTuple = {'name': actorName, 'url': actorURL};
							actorNames.append(actorTuple);
		except AttributeError:
			actorNames.append("null");

		return actorNames;

	def distribution_company_extractor(filmURL):
		filmPageSoup = BeautifulSoup(urllib.request.urlopen(filmURL));
		summaryTable = filmPageSoup.find('table',{ 'class' : 'infobox vevent'});
		
		companyNames = [];

		try:
			summaryTableRows = summaryTable.find_all('tr');

			for row in summaryTableRows:
				if 'Distributed' in row.text:
					companyNameATags = row.find_all('a');
					if not companyNameATags:
						companyName = row.text.replace(',','').replace('\'','').replace('"','');
						companyName = companyName.replace('\n','').replace('Distributed by','');
						companyURL = 'null';
						companyTuple = {'name': companyName, 'url': companyURL};
						companyNames.append(companyTuple);
					else:
						for tag in companyNameATags:
							if tag['href'][0] == "/":			
								companyName = tag['title'].replace(',','').replace('\'','').replace('"','');
								companyURL = wikipediaRoot + tag['href'].replace(',','').replace('\'','').replace('"','');
								companyTuple = {'name': companyName, 'url': companyURL};
								companyNames.append(companyTuple);
		except AttributeError:
			companyNames.append("null");

		return companyNames;

	def budget_extractor(filmURL):
		filmPageSoup = BeautifulSoup(urllib.request.urlopen(filmURL));
		summaryTable = filmPageSoup.find('table',{ 'class' : 'infobox vevent'});
		summaryTableRows = summaryTable.find_all('tr');

		filmBudgets = [];

		for row in summaryTableRows:
			if 'Budget' in row.text:
				filmBudget = row.text;
				filmBudget = filmBudget.strip();
				filmBudget = filmBudget.replace('\n','');
				decimalFind = filmBudget.find('.');
				if decimalFind == -1:
					if 'million' in filmBudget:
						filmBudget = filmBudget.split('$')[1].split('[')[0].replace('million','').strip();
						filmBudget = filmBudget + ',000,000';
						filmBudgets.append(filmBudget);
					elif 'thousand' in filmBudget:
						filmBudget = filmBudget.split('$')[1].split('[')[0].replace('thousand','').strip();
						filmBudget = filmBudget + ',000';
						filmBudgets.append(filmBudget);
					else:
						filmBudget = filmBudget.split('$')[1].split('[')[0].strip();
						filmBudgets.append(filmBudget);
				else:
					if 'million' in filmBudget:
						filmBudget = filmBudget.split('$')[1].split('[')[0].replace('million','').replace('.',',').strip();
						filmBudget = filmBudget + '00,000';
						filmBudgets.append(filmBudget);
					elif 'thousand' in filmBudget:
						filmBudget = filmBudget.split('$')[1].split('[')[0].replace('thousand','').replace('.',',').strip();
						filmBudget = filmBudget + '00';
						filmBudgets.append(filmBudget);
					else:
						filmBudget = filmBudget.split('$')[1].split('[')[0].replace('.',',').strip();
						filmBudgets.append(filmBudget);
		return filmBudgets;

#	filmBudgets = budget_extractor(filmURL);
#	print(filmBudgets);
	

	actorNames = actor_extractor(filmURL);
	for actorName in actorNames:
		print(actorName);
