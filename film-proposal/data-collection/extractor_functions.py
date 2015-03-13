# description: Accepts a film's URL and outputs the Director, Production Company, Starring Actors, and Budget from Wikipedia
# author: Daniel Joensen
# since: 03/08/2015
# tested with Python 3.4.2 on Windows 7 Ultimate 64 bit

import sys
from bs4 import BeautifulSoup
import urllib
import wikipedia
from datetime import datetime

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
					actorName = row.text.replace(',','').replace('\'','').replace('"','').replace(' (page does not exist)','').replace(' (actor)','').replace('\u0107','c');
					actorURL = 'null'
					actorTuple = {'name': actorName, 'url': actorURL};
					actorData.append(actorTuple);
				else:
					for tag in actorNameATags:
						if tag['href'][0] == "/":			
							actorName = tag['title'].replace(',','').replace('\'','').replace('"','').replace(' (page does not exist)','').replace(' (actor)','').replace('\u0107','c');
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

	budgetData = [];

	try:
		summaryTableRows = summaryTable.find_all('tr');

		for row in summaryTableRows:
			if 'Budget' in row.text:
				filmBudget = row.text;
				filmBudget = filmBudget.strip();
				filmBudget = filmBudget.replace('\n','');
				decimalFind = filmBudget.find('.');
				poundFind = filmBudget.find('£');
				if poundFind == -1:
					if decimalFind == -1:
						if 'million' in filmBudget:
							filmBudget = filmBudget.split('$')[1].split('[')[0].replace('million','').strip();
							filmBudget = filmBudget + ',000,000';
							budgetData.append(filmBudget);
						elif 'thousand' in filmBudget:
							filmBudget = filmBudget.split('$')[1].split('[')[0].replace('thousand','').strip();
							filmBudget = filmBudget + ',000';
							budgetData.append(filmBudget);
						else:
							filmBudget = filmBudget.split('$')[1].split('[')[0].strip();
							budgetData.append(filmBudget);
					else:
						if 'million' in filmBudget:
							filmBudget = filmBudget.split('$')[1].split('[')[0].replace('million','').replace('.',',').strip();
							filmBudget = filmBudget + '00,000';
							budgetData.append(filmBudget);
						elif 'thousand' in filmBudget:
							filmBudget = filmBudget.split('$')[1].split('[')[0].replace('thousand','').replace('.',',').strip();
							filmBudget = filmBudget + '00';
							budgetData.append(filmBudget);
						else:
							filmBudget = filmBudget.split('$')[1].split('[')[0].replace('.',',').strip();
							budgetData.append(filmBudget);
	except AttributeError:
		budgetData.append("null");

	return budgetData;


def revenue_extractor(filmPageSoup):
	summaryTable = filmPageSoup.find('table',{ 'class' : 'infobox vevent'});

	revenueData = [];

	try:
		summaryTableRows = summaryTable.find_all('tr');

		for row in summaryTableRows:
			if 'Box' in row.text:
				filmRevenue = row.text;
				filmRevenue = filmRevenue.strip();
				filmRevenue = filmRevenue.replace('\n','');
				poundFind = filmRevenue.find('£');
				#purposefully left the if statement for pound find open so that it is passed over if pounds are found, converting pounds to dollars will be a challenge.  may look at this later.
				if poundFind == -1:
					filmRevenue = filmRevenue.split('$')[1].split('[')[0].replace('.',',').strip();
					revenueData.append(filmRevenue);
	except AttributeError:
		revenueData.append("null");

	return revenueData;

def release_date_extractor(filmPageSoup):
	summaryTable = filmPageSoup.find('table',{ 'class' : 'infobox vevent'});

	try:
		summaryTableRows = summaryTable.find_all('tr');
		for row in summaryTableRows:
			if 'Release' in row.text:
				dateRow = summaryTable.find('span',{ 'class' : 'bday dtstart published updated'});
				releaseDate = dateRow.text;
				releaseDate = releaseDate.strip();
				releaseDate = releaseDate.replace('\n','');

	except AttributeError:
		releaseDate = ("null");

#Still need to handle films that list multiple dates, commonly for different countries

	return releaseDate;

"""
URL's with Errors, fix later!

'http://en.wikipedia.org/wiki/Harry_Potter_and_the_Philosopher%27s_Stone_(film)'

Revenue function errors:
'http://en.wikipedia.org/wiki/Who%27s_Minding_the_Store%3F'

"""

filmURLs = [
'http://en.wikipedia.org/wiki/Talladega_Nights:_The_Ballad_of_Ricky_Bobby',
'http://en.wikipedia.org/wiki/Gokulamlo_Seetha',
'http://en.wikipedia.org/wiki/Grain_in_Ear',
'http://en.wikipedia.org/wiki/Scarlet_Sails_(film)',
'http://en.wikipedia.org/wiki/A_Question_of_Taste',
'http://en.wikipedia.org/wiki/Uniform_(film)',
'http://en.wikipedia.org/wiki/City_Slickers',
'http://en.wikipedia.org/wiki/Die_Sehnsucht_der_Veronika_Voss',
'http://en.wikipedia.org/wiki/Lenny_(film)',
'http://en.wikipedia.org/wiki/The_White_Sheik',
'http://en.wikipedia.org/wiki/Doom_(film)',
'http://en.wikipedia.org/wiki/It_Happened_in_Brooklyn',
'http://en.wikipedia.org/wiki/Dead_or_Alive_(film)',
'http://en.wikipedia.org/wiki/Batman:_New_Times',
'http://en.wikipedia.org/wiki/Quel_maledetto_treno_blindato',
'http://en.wikipedia.org/wiki/Teenage_Mutant_Ninja_Turtles_III',
'http://en.wikipedia.org/wiki/Desert_Fury',
'http://en.wikipedia.org/wiki/Farewell_My_Lovely_(1975_film)',
'http://en.wikipedia.org/wiki/Light_Sleeper',
'http://en.wikipedia.org/wiki/The_Awakening_(2011_film)',
'http://en.wikipedia.org/wiki/Duck_and_Cover_(film)',
'http://en.wikipedia.org/wiki/I_Wanna_Hold_Your_Hand_(film)',
'http://en.wikipedia.org/wiki/Legend_(1985_film)',
'http://en.wikipedia.org/wiki/Enchanted_(film)',
'http://en.wikipedia.org/wiki/Clean_and_Sober',
'http://en.wikipedia.org/wiki/A_Summer_Place_(film)',
'http://en.wikipedia.org/wiki/Whoopee!_(film)',
'http://en.wikipedia.org/wiki/I_Eat_Your_Skin'

]

for filmURL in filmURLs:

	filmPageSoup = BeautifulSoup(urllib.request.urlopen(filmURL));
	directorData = director_extractor(filmPageSoup);
	budgetData = budget_extractor(filmPageSoup);
	distributionCompanyData = distribution_company_extractor(filmPageSoup);
	actorData = actor_extractor(filmPageSoup);
	revenueData = revenue_extractor(filmPageSoup);
	releaseDate = release_date_extractor(filmPageSoup);
	print('Release Date: ');
	print(releaseDate);