# description: Pull data from Box office mojo
# authors: Daniel Joensen
# since: 4/3/2015
# tested with Python 3.4.2 on Windows 7 Ultimate 64 bit
import urllib
import os
import sys
import re
import wikipedia
from bs4 import BeautifulSoup

#TODO: build function to extract list of movie titles/movie_ids from Alphabetical index
#TODO: finish opening weekend revenue function
#TODO: build number of theaters function

movie_ID = 'avatar.htm';
base_URL = 'http://www.boxofficemojo.com/movies';
movie_URL = ('%s/?id=%s' % (base_URL,movie_ID));
movie_soup = BeautifulSoup(urllib.request.urlopen(movie_URL));
#.encode('utf-8','ignore');

def find_domestic_total(movie_soup):
	revenue_table = movie_soup.find('div', {'class':'mp_box_content'});
	revenue_table_rows = revenue_table.find_all('tr');
	for row in revenue_table_rows:
		if 'Domestic' in row.text:
			domestic_total = row.text;
			domestic_total = domestic_total.split()[1];
	return domestic_total

def find_foreign_total(movie_soup):
	revenue_table = movie_soup.find('div', {'class':'mp_box_content'});
	revenue_table_rows = revenue_table.find_all('tr');
	for row in revenue_table_rows:
		if 'Foreign' in row.text:
			foreign_total = row.text;
			foreign_total = foreign_total.split()[2];
	return foreign_total

def find_global_total(movie_soup):
	revenue_table = movie_soup.find('div', {'class':'mp_box_content'});
	revenue_table_rows = revenue_table.find_all('tr');
	for row in revenue_table_rows:
		if 'Worldwide' in row.text:
			global_total = row.text;
			global_total = global_total.split()[2];
	return global_total


#def find_opening_weekend_total(movie_soup):
revenue_table = movie_soup.find_all('div', {'class':'mp_box_content'});
for table in revenue_table:
	table = str(table).encode('utf-8','ignore');
	print(table);
#	revenue_table_rows = revenue_table.find_all('tr');
#	for row in revenue_table_rows:
#		row = str(row).encode('utf-8','ignore');
#		print(row);


#	for column in revenue_table_columns:
#		if 'Opening' and 'Weekend' in column.text:
#			opening_weekend_total = column.text;
#			opening_weekend_total = opening_weekend_total.split()[0];
#	return opening_weekend_total


domestic_total = find_domestic_total(movie_soup);
foreign_total = find_foreign_total(movie_soup);
global_total = find_global_total(movie_soup);
#opening_weekend_total = find_opening_weekend_total(movie_soup);

"""
print("Domestic total: ");
print(domestic_total);

print("Foreign total: ");
print(foreign_total);

print("Global total: ");
print(global_total);



print("Opening Weekend Total: ");
print(opening_weekend_total);
"""