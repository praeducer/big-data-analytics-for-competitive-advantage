# description: takes in a list of search terms and outputs a list of wikipedia URLs. Currently focuses on films.
# input: must pass in a new line separated input file as a command line argument.
# output: .csv
# author: Paul Prae
# since: 3/3/2015
# tested with Python 3.3 on CentOS 7

import sys
import fileinput
import wikipedia

outputFilename = 'wikipedia_urls.csv';
outputFile = open(outputFilename,'w');
terms = [];
urls = [];

for line in fileinput.input():
	terms.append(line);

for term in terms:
	query = term.strip('\n\r') + ' (film)';
	print('query: ' + query);
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
				url = None;
	except wikipedia.exceptions.PageError:
		url = None;
	outputFile.write('%s\n' % url);

outputFile.close();

