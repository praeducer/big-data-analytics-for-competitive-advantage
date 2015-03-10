# description: Accepts a film's URL and outputs the Director from Wikipedia
# author: Daniel Joensen
# since: 3/0/2015
# tested with Python 3.4.2 on windows 7 Ultimate 64 bit

import sys
from bs4 import BeautifulSoup
import urllib
import wikipedia

filmURL = 'http://en.wikipedia.org/wiki/Avatar_(2009_film)'

def budget_extractor(filmURL):
	filmPageSoup = BeautifulSoup(urllib.request.urlopen(filmURL));
	summaryTable = filmPageSoup.find('table',{ 'class' : 'infobox vevent'});
	summaryTableRows = summaryTable.find_all('tr');

	for row in summaryTableRows:
		if 'Budget' in row.text:
			budgetText = row.text;
			budgetText = budgetText.strip();
			budgetText = budgetText.replace('\n','');
			if 'million' in budgetText:
				budgetText = budgetText.split('$')[1].split('[')[0].replace('million','').strip();
				budgetText = budgetText + ',000,000';
#			elif '$' in budgetText:
#				budgetText = budgetText.split('$')[-1].split('[')[0].replace(',','');
			return budgetText;

filmBudget = budget_extractor(filmURL);
print(filmBudget);