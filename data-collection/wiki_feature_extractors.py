# description: Pull features from Wikipedia pages. Intended for film pages so far.
# authors: Daniel Joensen (primary contributor), Paul Prae (cleaning crew)
# note: During refactoring, much of this code was copied over by Paul from a file Daniel wrote.
# since: 3/08/2015
# tested with Python 3.3 on CentOS 7

import os
import sys
import re
from bs4 import BeautifulSoup
import wikipedia
import urllib
import csv

wikipediaRoot = 'http://en.wikipedia.org';

def dollar_cleaner(dollarField):

	try:
		dollarField = dollarField.split('$')[1].split('[')[0].strip();
		openingIndex = dollarField.find('(');
		closingIndex = dollarField.find(')');
		dollarField = dollarField[0:openingIndex] + '' + dollarField[closingIndex:(len(dollarField))];
		dollarField = dollarField.replace(' ','').replace(')','').replace('to','');
		poundFind = dollarField.find('£');

		if poundFind == -1:
			if 'billion' in dollarField:
				dollarField = dollarField.replace('billion','');
				if dollarField.find('.') == -1:
					dollarField = int(dollarField) * 1000000000;
				else:
					itemList = dollarField.split('.');
					dollarField = dollarField.replace('.','');
					if len(itemList[1]) == 1:
						dollarField = int(dollarField) * 100000000;
					elif len(itemList[1]) == 2:
						dollarField = int(dollarField) * 10000000;
					else:
						dollarField = int(dollarField) * 1000000;
			elif 'million' in dollarField:
				dollarField = dollarField.replace('million','');
				if dollarField.find('.') == -1:
					dollarField = int(dollarField) * 1000000;
				else:
					itemList = dollarField.split('.');
					dollarField = dollarField.replace('.','');
					if len(itemList[1]) == 1:
						dollarField = int(dollarField) * 100000;
					elif len(itemList[1]) == 2:
						dollarField = int(dollarField) * 10000;
					else:
						dollarField = int(dollarField) * 1000;
			elif 'thousand' in dollarField:
				dollarField = replace('thousand','');
				if dollarField.find('.') == -1:
					dollarField = int(dollarField) * 1000;
				else:
					itemList = dollarField.split('.');
					dollarField = dollarField.replace('.','');
					if len(itemList[1]) == 1:
						dollarField = int(dollarField) * 100;
					elif len(itemList[1]) == 2:
						dollarField = int(dollarField) * 10;
					else:
						dollarField = int(dollarField) * 1;
			else:
				dollarField = dollarField;
	
	except (AttributeError, IndexError, ValueError):
		dollarField = "null";

	return dollarField;

def find_budget(filmPageSoup):
	summaryTable = filmPageSoup.find('table',{ 'class' : 'infobox vevent'});
	filmBudget = '';
	try:
		summaryTableRows = summaryTable.find_all('tr');

		for row in summaryTableRows:
			if 'Budget' in row.text:
				dollarField = row.text;
				filmBudget = dollar_cleaner(dollarField);
				filmBudget = str(filmBudget);

	except (AttributeError, IndexError):
		filmBudget = 'null';

	if not filmBudget:
		filmBudget = 'null';

	return filmBudget.replace(',','');


def find_revenue(filmPageSoup):
	summaryTable = filmPageSoup.find('table',{ 'class' : 'infobox vevent'});
	filmRevenue = "";

	try:
		summaryTableRows = summaryTable.find_all('tr');

		for row in summaryTableRows:
			if 'Box' in row.text:
				dollarField = row.text;
				filmRevenue	= dollar_cleaner(dollarField);
				filmRevenue = str(filmRevenue);

	except (AttributeError,IndexError):
		filmRevenue = 'null';

	if not filmRevenue:
		filmRevenue = 'null'; 

	return filmRevenue.replace(',','');

def find_director(filmPageSoup):
	summaryTable = filmPageSoup.find('table',{ 'class' : 'infobox vevent'});	
	directorData = [];

	try:
		summaryTableRows = summaryTable.find_all('tr');

		for row in summaryTableRows:
			if 'Directed' in row.text:
				directorNameATags = row.find_all('a');
				if not directorNameATags:
					directorName = row.text.replace(',','').replace('\'','').replace('"','').replace('\u014d','o');
					directorName = directorName.replace('Directed by','').split('\n');
					for director in directorName:
						directorURL = 'null'
						if director == '':
							pass
						else:
							directorTuple = {'name': director, 'url': directorURL};
							directorData.append(directorTuple);
				else:
					for tag in directorNameATags:
						if tag['href'][0] == "/":			
							directorName = tag['title'].replace(',','').replace('\'','').replace('"','').replace('\u014d','o');
							directorURL = wikipediaRoot + tag['href'].replace(',','').replace('\'','').replace('"','');
							directorTuple = {'name': directorName, 'url': directorURL};
							directorData.append(directorTuple);
	except AttributeError:
		directorTuple = {'name': 'null', 'url': 'null'};
		directorData.append(directorTuple);

	return directorData;

def find_actor(filmPageSoup):

	summaryTable = filmPageSoup.find('table',{ 'class' : 'infobox vevent'});
	actorData = [];

	try:
		summaryTableRows = summaryTable.find_all('tr');
		for row in summaryTableRows:
			if 'Starring' in row.text:
				actorNameATags = row.find_all('a');
				if not actorNameATags:
					actorName = row.text.replace(',','').replace('\'','').replace('"','').replace('\u014d','o').replace('\u016b','u');
					actorName = actorName.replace('Starring','').replace('(page does not exist)','').split('\n');
					for actor in actorName:
						actorURL = 'null'
						if actor == '':
							pass
						else:
							actorTuple = {'name': actor, 'url': actorURL};
							actorData.append(actorTuple);
				else:
					for tag in actorNameATags:
						if tag['href'][0] == "/":			
							actorName = tag['title'].replace(',','').replace('\'','').replace('"','').replace('(page does not exist)','').replace('\u014d','o').replace('\u016b','u');
							actorURL = wikipediaRoot + tag['href'].replace(',','').replace('\'','').replace('"','');
							actorTuple = {'name': actorName, 'url': actorURL};
							actorData.append(actorTuple);
	except AttributeError:
		actorTuple = {'name': 'null', 'url': 'null'};
		actorData.append(actorTuple);

	return actorData;

def find_distribution_company(filmPageSoup):
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
		companyTuple = {'name': 'null', 'url': 'null'};
		distributionCompanyData.append(companyTuple);

	return distributionCompanyData;

# TODO: Still need to handle films that list multiple dates, commonly for different countries
def find_release_date(filmPageSoup):
	summaryTable = filmPageSoup.find('table',{ 'class' : 'infobox vevent'});
	releaseDate = "";
	try:
		summaryTableRows = summaryTable.find_all('tr');
		for row in summaryTableRows:
			if 'Release' in row.text:
				dateRow = summaryTable.find('span',{ 'class' : 'bday dtstart published updated'});
				releaseDate = dateRow.text;
				releaseDate = releaseDate.strip();
				releaseDate = releaseDate.replace('\n','');

#TODO: Add parsedatetime library, pass in release date and check output, WTF

	except AttributeError:
		releaseDate = 'null';
	if not releaseDate:
		releaseDate = 'null';

	return releaseDate;

def find_genre(filmPageSoup):
	genreList = [];
	# Main list of film Genres scrubbed programatically from Wikipedia, supplemented by list found at http://www.imdb.com/genre/
	filmGenres = [
		'Romance',
		'Short',
		'Action',
		'Comedy',
		'Drama',
		'Horror',
		'Mystery',
#		'Science Fiction',
		'Silent',
		'Crime',
		'Fantasy',
		'Caper',
		'Slasher',
		'Teen',
		'Biographical',
		'Independent',
		'Animated',
		'Erotic',
		'Documentary',
		'War',
		'Thriller',
		'Musical',
		'Heist',
		'Exploitation',
#		'Romantic Comedy',
#		'Epic',
		'Sports',
		'Parody',
		'Cult',
		'Spy',
		'Concert',
		'Vampires',
		'Children',
		'Adventure',
		'Sci-fi',
        'Science',
		'Fiction',
		'Romantic',
		'Superhero'
	]

	filmParagraphs = filmPageSoup.find_all('p');
	if filmParagraphs:
		targetParagraph = filmParagraphs[0];
		paragraphText = targetParagraph.text.lower();
		paragraphText = paragraphText.replace('-',' ');
		wordList = paragraphText.split('.');
		targetSentence = wordList[0];
		targetWords = targetSentence.split(' ');
		
		try:
			for word in targetWords:
				for genre in filmGenres:
					genre = genre.lower();
					if word == genre:
						genreList.append(word);
		except IndexError:
			genreList.append("null");
	else:
			genreList.append("null");

	return genreList;



""" Code for testing only

filmURLs = [
'http://en.wikipedia.org/wiki/Cannonball_Run_(film)',
'http://en.wikipedia.org/wiki/Cannonball_Run_II',
'http://en.wikipedia.org/wiki/Can%27t_Buy_Me_Love_(film)',
'http://en.wikipedia.org/wiki/Can%27t_Hardly_Wait',
'http://en.wikipedia.org/wiki/Can%27t_Stop_the_Music',
'http://en.wikipedia.org/wiki/Cape_Nostalgia',
'http://en.wikipedia.org/wiki/Capitalism:_A_Love_Story',
'http://en.wikipedia.org/wiki/Capone_(film)',
'http://en.wikipedia.org/wiki/Capote_(film)',
'http://en.wikipedia.org/wiki/Capricorn_One'
]

for filmURL in filmURLs:
	
	filmPageSoup = BeautifulSoup(urllib.request.urlopen(filmURL));
#	filmBudget = find_budget(filmPageSoup);
#	filmRevenue = find_revenue(filmPageSoup);
#	directorData = find_director(filmPageSoup);
#	distributionCompanyData = find_distribution_company(filmPageSoup);
#	actorData = find_actor(filmPageSoup);
#	releaseDate = find_release_date(filmPageSoup);
	genreList = find_genre(filmPageSoup);

#	for directorTuple in directorData:
#		print("Directed by: ");
#		print(directorTuple);

#	for actorTuple in actorData:
#		print("Starring: ");
#		print(actorTuple); 

	#for genre in genreList:
	#	print("Genre: ");
	#	print(genre);
	print("Genre: ");
	print(genreList);

#	print("Film Budget: ");
#	print(filmBudget);

#	print("Film Revenue: ");
#	print(filmRevenue);
"""
