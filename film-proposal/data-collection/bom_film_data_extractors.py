# description: Pulls various pieces of data from Box office mojo
# authors: Daniel Joensen
# since: 4/3/2015
# tested with Python 3.4.2 on Windows 7 Ultimate 64 bit
import urllib
import os
import sys
import re
import wikipedia
import csv
from bs4 import BeautifulSoup

#TODO: Finish integrating the urls from the excel input file
#TODO: Organize and test final data output
#TODO: Replace dollar signs and commas in dollar outputs
#TODO: Reformat date field to convert release date into MM/DD/YYYY, or worst case just extract the year.

movie_ID = 'godzilla2012.htm';
base_URL = 'http://www.boxofficemojo.com/movies';
movie_URL = ('%s/?id=%s' % (base_URL,movie_ID));
movie_soup = BeautifulSoup(urllib.request.urlopen(movie_URL));


def find_movie_name(movie_soup):
	table_list = movie_soup.find_all('table');
	target_table = table_list[2];
	table_rows = target_table.find_all('tr');
	target_row = table_rows[0];
	target_columns = target_row.find_all('td', {'align':'center'});
	target_column = target_columns[1];
	target_column = target_column.find('b')
	movie_title = target_column.text;
	return movie_title;

def find_domestic_total(movie_soup):
	revenue_table = movie_soup.find('div', {'class':'mp_box_content'});
	revenue_table_rows = revenue_table.find_all('tr');
	domestic_total = 'null';
	for row in revenue_table_rows:
		if 'Domestic' in row.text:
			domestic_total = row.text;
			domestic_total = domestic_total.split()[1];
	return domestic_total;

def find_foreign_total(movie_soup):
	revenue_table = movie_soup.find('div', {'class':'mp_box_content'});
	revenue_table_rows = revenue_table.find_all('tr');
	foreign_total = 'null';
	for row in revenue_table_rows:
		if 'Foreign' in row.text:
			foreign_total = row.text;
			foreign_total = foreign_total.split()[2];
	return foreign_total;

def find_global_total(movie_soup):
	revenue_table = movie_soup.find('div', {'class':'mp_box_content'});
	revenue_table_rows = revenue_table.find_all('tr');
	global_total = 'null';
	for row in revenue_table_rows:
		if 'Worldwide' in row.text:
			global_total = row.text;
			global_total = global_total.split()[2];
		else:
			global_total = 'null';
	return global_total;

def find_opening_weekend_total(movie_soup):
	revenue_table = movie_soup.find_all('div', {'class':'mp_box_content'});
	target_table = revenue_table[1];
	target_table_rows = target_table.find_all('tr');
	opening_weekend_total = 'null';
	for row in target_table_rows:
		list_item = row.text;
		if 'Weekend' in row.text:
			if 'Limited' in row.text:
				pass
			else:
				final_row = row.text.split();
				for item in final_row:
					if '$' in item:
						opening_weekend_total = item;
	return opening_weekend_total;

def find_number_of_theaters(movie_soup):
	try:
		revenue_table = movie_soup.find_all('div', {'class':'mp_box_content'});
		target_table = revenue_table[1];
		target_table_columns = target_table.find_all('td');
		column_list = [];
		for column in target_table_columns:
			list_item = column.text;
			list_item = list_item.split();
			column_list.append(list_item);
	#	print(column_list[len(column_list)-1]);
		number_of_theaters = column_list[2];
		number_of_theaters = number_of_theaters[2];
	except IndexError:
		number_of_theaters = 'null';
	return number_of_theaters;

def find_mpaa_rating(movie_soup):
	center_table = movie_soup.findChildren('center')[0];
	center_table_data = center_table.findChildren('tr');#[5];
	#center_table_data = center_table_data[len(center_table_data)-2];
	for row in center_table_data:
		if 'MPAA' in row.text:
			center_table_data = row.find('b');
			center_table_data = center_table_data.text;
#	center_table_data = center_table_data.find('b');
#	center_table_data = center_table_data.text
	return center_table_data;

def find_release_date(movie_soup):
	center_table = movie_soup.findChildren('center')[0];
	center_table_data = center_table.findChildren('tr');
	for row in center_table_data:
		if 'Distributor' in row.text:
			if 'Release' in row.text:
				release_date = row.find_all('b');
				release_date = release_date[1].text;
		else:
			if 'Release' in row.text:
				release_date = row.find('b');
				release_date = release_date.text;
	return release_date;

domestic_total = find_domestic_total(movie_soup);
foreign_total = find_foreign_total(movie_soup);
global_total = find_global_total(movie_soup);
opening_weekend_total = find_opening_weekend_total(movie_soup);
number_of_theaters = find_number_of_theaters(movie_soup);
mpaa_rating = find_mpaa_rating(movie_soup);
movie_name = find_movie_name(movie_soup);
release_date = find_release_date(movie_soup);

"""
filename = './data/bom_film_urls.csv';
bom_film_urls = [];
film_url_reader = csv.reader(open(filename));
for row in film_url_reader:
	bom_film_urls.append(row);

for item in bom_film_urls:
	print (item);

"""

print("Film Title: ");
print(movie_name);

print("Release Date: ");
print(release_date);

print("Domestic total: ");
print(domestic_total);

print("Foreign total: ");
print(foreign_total);

print("Global total: ");
print(global_total);

print("Opening Weekend Total: ");
print(opening_weekend_total);

print("Number of Theaters: ");
print(number_of_theaters);

print("MPAA Rating: ");
print(mpaa_rating);
