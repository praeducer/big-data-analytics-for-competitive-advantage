# description: Pull important data from Wikipedia film pages stored locally.
# authors: Paul Prae, Daniel Joensen
# since: 3/08/2015
# tested with Python 3.3 on CentOS 7

import os
import sys
import re
from bs4 import BeautifulSoup
import wikipedia
import csv

wikipediaRoot = 'http://en.wikipedia.org';

def find_budget(filmPageSoup):
	summaryTable = filmPageSoup.find('table',{ 'class' : 'infobox vevent'});

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
							filmBudget = filmBudget.split('$')[1].split('[')[0].replace('million','').replace(' ','').strip();
							filmBudget = filmBudget + ',000,000';
							openingIndex = filmBudget.find('(');
							closingIndex = filmBudget.find(')');
							filmBudget = filmBudget[0:openingIndex] + '' + filmBudget[closingIndex:(len(filmBudget))];
							filmBudget = filmBudget.replace(' ','').replace(')','');
							return filmBudget;
						elif 'thousand' in filmBudget:
							filmBudget = filmBudget.split('$')[1].split('[')[0].replace('thousand','').strip();
							filmBudget = filmBudget + ',000';
							openingIndex = filmBudget.find('(');
							closingIndex = filmBudget.find(')');
							filmBudget = filmBudget[0:openingIndex] + '' + filmBudget[closingIndex:(len(filmBudget))];
							filmBudget = filmBudget.replace(' ','').replace(')','');
							return filmBudget;
						else:
							filmBudget = filmBudget.split('$')[1].split('[')[0].strip();
							openingIndex = filmBudget.find('(');
							closingIndex = filmBudget.find(')');
							filmBudget = filmBudget[0:openingIndex] + '' + filmBudget[closingIndex:(len(filmBudget))];
							filmBudget = filmBudget.replace(' ','').replace(')','');
							return filmBudget;
					else:
						if 'million' in filmBudget:
							filmBudget = filmBudget.split('$')[1].split('[')[0].replace('million','').replace('.',',').strip();
							filmBudget = filmBudget + '00,000';
							openingIndex = filmBudget.find('(');
							closingIndex = filmBudget.find(')');
							filmBudget = filmBudget[0:openingIndex] + '' + filmBudget[closingIndex:(len(filmBudget))];
							filmBudget = filmBudget.replace(' ','').replace(')','');
							return filmBudget;
						elif 'thousand' in filmBudget:
							filmBudget = filmBudget.split('$')[1].split('[')[0].replace('thousand','').replace('.',',').strip();
							filmBudget = filmBudget + '00';
							openingIndex = filmBudget.find('(');
							closingIndex = filmBudget.find(')');
							filmBudget = filmBudget[0:openingIndex] + '' + filmBudget[closingIndex:(len(filmBudget))];
							filmBudget = filmBudget.replace(' ','').replace(')','');
							return filmBudget;
						else:
							filmBudget = filmBudget.split('$')[1].split('[')[0].replace('.',',').strip();
							openingIndex = filmBudget.find('(');
							closingIndex = filmBudget.find(')');
							filmBudget = filmBudget[0:openingIndex] + '' + filmBudget[closingIndex:(len(filmBudget))];
							filmBudget = filmBudget.replace(' ','').replace(')','');
							return filmBudget;
	except (AttributeError, IndexError):
		filmBudget = "null";
		return filmBudget;


def find_revenue(filmPageSoup):
	summaryTable = filmPageSoup.find('table',{ 'class' : 'infobox vevent'});

	revenueData = "";

	try:
		summaryTableRows = summaryTable.find_all('tr');

		for row in summaryTableRows:
			if 'Box' in row.text:
				filmRevenue = row.text;
				filmRevenue = filmRevenue.strip();
				filmRevenue = filmRevenue.replace('\n','');
				poundFind = filmRevenue.find('£');
				# TODO: purposefully left the if statement for pound find open so that it is passed over if pounds are found, converting pounds to dollars will be a challenge.  may look at this later.
				if poundFind == -1:
					revenueData = filmRevenue.split('$')[1].split('[')[0].replace('.',',').strip();
	except (AttributeError,IndexError):
		revenueData = "null";

	return revenueData.replace(',','');

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
				for tag in actorNameATags:
					if tag['href'][0] == "/":			
						actorName = tag['title'].replace(',','').replace('\'','').replace('"','');
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

	except AttributeError:
		releaseDate = ("null");

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
		'Science Fiction',
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
		'Romantic Comedy',
		'Epic',
		'Sports',
		'Parody',
		'Cult',
		'Spy',
		'Concert',
		'Vampires',
		'Children',
		'Adventure',
		'Sci-fi'
	]

	filmParagraphs = filmPageSoup.find_all('p');
	if filmParagraphs:
		targetParagraph = filmParagraphs[0];
		paragraphText = targetParagraph.text.lower();
		paragraphText = paragraphText.replace('-',' ');
		wordList = paragraphText.split('.');
		targetSentance = wordList[0];
		targetWords = targetSentance.split(' ');

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
