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
# custom
import wiki_feature_extractors

def tuples_to_column_value(notableData):
	pipesAndTuples = "";
	for notableTuple in notableData:
		notableName = notableTuple['name'];
		notableURL = notableTuple['url'];
		pipesAndTuples += notableName + ';' + notableURL + '|';
	# Removing last pipe
	finalValue = pipesAndTuples[:-1]
	if not finalValue:
		finalValue = 'null';
	return finalValue;

def list_to_column_value(dataList):
	columnValue = "";
	for item in dataList:
		columnValue += item + '|';
	columnValue = columnValue[:-1];
	if not columnValue:
		columnValue = 'null';
	return columnValue;

def build_film_index():
	filmIndex = {};
	filmDataFilename = './data/film_urls.csv';
	filmDataReader = csv.reader(open(filmDataFilename, encoding="utf8"));
	filmDataReader.__next__();
	count = 0;
	for filmData in filmDataReader:
		count += 1;
		filmIndex[filmData[0]] = {'title': filmData[1], 'year': filmData[2]};
	return filmIndex;

if __name__=="__main__":

	filmWriter = csv.writer(open('./data/test_film_data.csv', 'w'));
	filmIndex = build_film_index();
	filmWriter.writerow(['title', 'url', 'release date', 'release year', 'budget', 'revenue', 'director', 'actor', 'distributor', 'genre']);
	relativeFilmFilePath = './data/films/test/';
	filmFiles = os.listdir(relativeFilmFilePath);
	count = 0;
	for filmFileName in filmFiles:
		count += 1;
		print(str(count) + ' - ' + filmFileName);
		fullFilmFilePath = relativeFilmFilePath + filmFileName;
		try:
			filmPage = open(fullFilmFilePath, encoding="utf8");
		except IsADirectoryError:
			pass;
		filmPageSoup = BeautifulSoup(filmPage.read());

		filmURLName = os.path.splitext(filmFileName)[0];
		filmURL = 'http://en.wikipedia.org/wiki/' + filmURLName;
		
		filmDate = wiki_feature_extractors.find_release_date(filmPageSoup);

		budgetValue = wiki_feature_extractors.find_budget(filmPageSoup);
		if not budgetValue:
			budgetValue = 'null';
		budgetValue = budgetValue.replace(',','');

		revenueValue = wiki_feature_extractors.find_revenue(filmPageSoup);

		directorData = wiki_feature_extractors.find_director(filmPageSoup);
		directorValue = tuples_to_column_value(directorData);

		actorData = wiki_feature_extractors.find_actor(filmPageSoup);
		actorValue = tuples_to_column_value(actorData);

		distributionData = wiki_feature_extractors.find_distribution_company(filmPageSoup);
		distributionValue = tuples_to_column_value(distributionData);

		genreData = wiki_feature_extractors.find_genre(filmPageSoup);
		genreValue = list_to_column_value(genreData);

		try:
			filmData = filmIndex.get(filmURL);
			if filmData:
				filmTitle = filmData.get('title');
				if not filmTitle:
					filmTitle = filmFileName;
				filmYear = filmData.get('year');
				if not filmYear:
					filmYear = 'null';
			else:
				filmTitle = 'null';
				filmYear = 'null';
			filmWriter.writerow([filmTitle, filmURL, filmDate, filmYear, budgetValue, revenueValue, directorValue, actorValue, distributionValue, genreValue]);
		except KeyError:
			pass;
