# description: Accepts a film's URL and outputs the Director, Production Company, Starring Actors, and Budget from Wikipedia
# author: Daniel Joensen
# since: 03/08/2015
# tested with Python 3.4.2 on Windows 7 Ultimate 64 bit

import sys
from bs4 import BeautifulSoup
import urllib
import wikipedia

wikipediaRoot = 'http://en.wikipedia.org';

def director_extractor(filmPageSoup):
	summaryTable = filmPageSoup.find('table',{ 'class' : 'infobox vevent'});	
	directorData = [];

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
					directorData.append(directorTuple);
				else:
					for tag in directorNameATags:
						if tag['href'][0] == "/":			
							directorName = tag['title'].replace(',','').replace('\'','').replace('"','').replace('\u014d','o');
							directorURL = wikipediaRoot + tag['href'].replace(',','').replace('\'','').replace('"','');
							directorTuple = {'name': directorName, 'url': directorURL};
							directorData.append(directorTuple);
	except AttributeError:
		directorData.append("null");

	return directorData;


def actor_extractor(filmPageSoup):
	summaryTable = filmPageSoup.find('table',{ 'class' : 'infobox vevent'});	
	actorData = [];

	try:
		summaryTableRows = summaryTable.find_all('tr');

		for row in summaryTableRows:
			if 'Starring' in row.text:
				actorNameATags = row.find_all('a');
				if not actorNameATags:
					actorName = row.text.replace(',','').replace('\'','').replace('"','').replace(' (page does not exist)','').replace(' (actor)','');
					actorURL = 'null'
					actorTuple = {'name': actorName, 'url': actorURL};
					actorData.append(actorTuple);
				else:
					for tag in actorNameATags:
						if tag['href'][0] == "/":			
							actorName = tag['title'].replace(',','').replace('\'','').replace('"','').replace(' (page does not exist)','').replace(' (actor)','');
							actorURL = wikipediaRoot + tag['href'].replace(',','').replace('\'','').replace('"','');
							actorTuple = {'name': actorName, 'url': actorURL};
							actorData.append(actorTuple);
	except AttributeError:
		actorData.append("null");

	return actorData;

def distribution_company_extractor(filmPageSoup):
	summaryTable = filmPageSoup.find('table',{ 'class' : 'infobox vevent'});	
	distributionCompanyData = [];

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
					distributionCompanyData.append(companyTuple);
				else:
					for tag in companyNameATags:
						if tag['href'][0] == "/":			
							companyName = tag['title'].replace(',','').replace('\'','').replace('"','');
							companyURL = wikipediaRoot + tag['href'].replace(',','').replace('\'','').replace('"','');
							companyTuple = {'name': companyName, 'url': companyURL};
							distributionCompanyData.append(companyTuple);
	except AttributeError:
		distributionCompanyData.append("null");

	return distributionCompanyData;

def budget_extractor(filmPageSoup):
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

filmURLs = [
'http://en.wikipedia.org/wiki/Dutch_(film)',
'http://en.wikipedia.org/wiki/Robots_(2005_film)',
'http://en.wikipedia.org/wiki/Deep_Rising',
'http://en.wikipedia.org/wiki/Rob_Roy_(1995_film)'
]

for filmURL in filmURLs:
	filmPageSoup = BeautifulSoup(urllib.request.urlopen(filmURL));
	directorData = director_extractor(filmPageSoup);
	filmBudgets = budget_extractor(filmPageSoup);
	distributionCompanyData = distribution_company_extractor(filmPageSoup);
	actorData = actor_extractor(filmPageSoup);
	for directorTuple in directorData:
		print('Director: ');
		print(directorTuple);
	for filmBudget in filmBudgets:
		print('Budget: ');
		print(filmBudget);
	for companyTuple in distributionCompanyData:
		print('Production Company: ');
		print(companyTuple);
	for actorTuple in actorData:
		print('Actor: ');
		print(actorTuple);