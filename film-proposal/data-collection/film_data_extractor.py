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
		directorTuple = {'name': 'null', 'url': 'null'};
		directorData.append(directorTuple);

	return directorData;

def actor_extractor(filmPageSoup):

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
		companyTuple = {'name': 'null', 'url': 'null'};
		distributionCompanyData.append(companyTuple);

	return distributionCompanyData;

# TODO: Still need to handle films that list multiple dates, commonly for different countries
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

	return releaseDate;

def list_to_column_value(notableData):
	pipesAndTuples = "";
	
	for notableTuple in notableData:
		notableName = notableTuple['name'];
		notableURL = notableTuple['url'];
		pipesAndTuples += notableName + ';' + notableURL + '|';
	# Removing last pipe
	return pipesAndTuples[:-1];

def build_film_index():
	filmIndex = {};
	filmDataFilename = './data/film_urls.csv';
	filmDataReader = csv.reader(open(filmDataFilename));
	filmDataReader.__next__();
	count = 0;
	for filmData in filmDataReader:
		count += 1;
		filmIndex[filmData[0]] = {'title': filmData[1], 'year': filmData[2]};
	return filmIndex;

if __name__=="__main__":

	filmWriter = csv.writer(open('./data/film_data.csv', 'w'));
	filmIndex = build_film_index();
	filmWriter.writerow(['title', 'url', 'release date', 'release year', 'director', 'actor', 'distributor']);
	relativeFilmFilePath = './data/films/test/';
	filmFiles = os.listdir(relativeFilmFilePath);
	for filmFileName in filmFiles:
		print(filmFileName);
		fullFilmFilePath = relativeFilmFilePath + filmFileName;
		try:
			filmPage = open(fullFilmFilePath);
		except IsADirectoryError:
			pass;
		filmPageSoup = BeautifulSoup(filmPage.read());

		filmURLName = os.path.splitext(filmFileName)[0];
		filmURL = 'http://en.wikipedia.org/wiki/' + filmURLName;
		releaseDate = release_date_extractor(filmPageSoup);
		directorData = director_extractor(filmPageSoup);
		directorValue = list_to_column_value(directorData);
		actorData = actor_extractor(filmPageSoup);
		actorValue = list_to_column_value(actorData);
		distributionData = distribution_company_extractor(filmPageSoup);
		distributionValue = list_to_column_value(distributionData);

		try:
			filmWriter.writerow([filmIndex[filmURL]['title'], filmURL, releaseDate, filmIndex[filmURL]['year'], directorValue, actorValue, distributionValue]);
		except KeyError:
			pass;
