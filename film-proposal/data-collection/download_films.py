# description: Given a list of URLs for pages to download, this script stores the HTML from these pages locally.
# output: .csv
# author: Paul Prae
# since: 3/8/2015
# tested with Python 3.3 on CentOS 7

import sys
import csv
import requests
import random
import time

trackingFile = open('C:/Users/Public/dev/film_page_storage/progress_tracking.csv','w');
filmDataFilename = 'C:/Users/Public/dev/bom_film_urls.csv';
filmDataReader = csv.reader(open(filmDataFilename, encoding="utf8"));
filmDataReader.__next__();
count = 0;
for filmData in filmDataReader:
	count += 1;
#	pause = time.sleep(15 + 15*random.random())
	url = filmData[0];
	urlPieces = url.split('=');
	pageName = urlPieces[len(urlPieces) - 1];
	pageFile = open('C:/Users/Public/dev/film_page_storage/' + pageName, 'w');
	try:
		response = requests.get(url);
		response = str(response).encode('ascii','ignore');
		response = response.decode('ascii','ignore').strip();
		print(str(count) + '. Writing ' + pageName);
		pageFile.write(response);
		trackingFile.write(url + '\n');
	except requests.exceptions.RequestException:
		print('Exception: Bad Request for ' + pageName + ' -> ' + url);
		pageFile.close();
trackingFile.close();

"""
#Wikipedia webpage extractor function
filmDataFilename = './data/test_film_urls.csv';
filmDataReader = csv.reader(open(filmDataFilename, encoding="utf8"));
filmDataReader.__next__();
count = 0;
for filmData in filmDataReader:
	count += 1;
	url = filmData[0];
	urlPieces = url.split('/');
	pageName = urlPieces[len(urlPieces) - 1];
	pageFile = open('./data/films/' + pageName + '.html', 'w');
	try:
		response = requests.get(url);
		print(str(count) + '. Writing ' + pageName);
		pageFile.write(response.text);
	except requests.exceptions.RequestException:
		print('Exception: Bad Request for ' + pageName + ' -> ' + url);
	pageFile.close();
"""