# description: takes in a list of movie titles and outputs a list of wikipedia URLs.
# input: The Open Movie Database's Database Dump. e.g. https://github.com/praeducer/big-data-analytics-for-competitive-advantage/blob/master/film-proposal/data-collection/data/omdb/test/omdbMovies_tiny_sample.txt
# file output: a .csv e.g. https://github.com/praeducer/big-data-analytics-for-competitive-advantage/blob/master/film-proposal/data-collection/data/wikipedia_urls.csv
# cmd line output: e.g. https://github.com/praeducer/big-data-analytics-for-competitive-advantage/blob/master/film-proposal/data-collection/data/cmd_output.txt
# author: Paul Prae
# since: 3/3/2015
# tested with Python 3.3 on CentOS 7 and Windows 8.1

import sys
import wikipedia
import csv
import codecs

outputFilename = './data/omdb/test/omdb_movies_wikipedia_urls_tiny_sample.csv';
filmDataWriter = csv.writer(open(outputFilename,'w', encoding="utf8", newline=''), delimiter='\t');
inputFilename = './data/omdb/test/omdbMovies_tiny_sample.txt';
filmDataReader = csv.reader(open(inputFilename, encoding="utf8"),delimiter='\t');
filmDataReader.__next__();
urls = [];
count = 0;

for line in filmDataReader:
	count += 1;
	title = line[2];
	query = title.strip('\n\r') + ' (film)';
	try:
		print(str(count) + ' - ' + 'query: ' + query);
	except UnicodeEncodeError:
		print(str(count) + ' - ' + 'query: <UnicodeEncodeError during print. Search is fine.>');
	try:
		# Note: This can sometimes auto-suggest or redirect to odd pages.
		# TODO: Handle case when page "does not exist" and the first result is automatically given
		page = wikipedia.page(query);
		url = page.url;
		print('\tresult-> ' + url);
	except wikipedia.exceptions.DisambiguationError as e:
		for option in e.options:
			print('\toption: ' + option);
			if 'film)' in option:
				# TODO: This problem may happen recursively...
				page = wikipedia.page(option);
				url = page.url
				print('\t\tresult-> ' + url);
				break;
			else:
				url = 'N/A';
	except wikipedia.exceptions.PageError:
		url = 'N/A';
	if not url:
		url = 'N/A';
	line.append(url);
	filmDataWriter.writerow(line);
