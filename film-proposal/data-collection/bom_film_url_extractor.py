# description: Parses the primary and secondary alphabetical index pages on Box Office Mojo in order to construct a complete list of individual film urls.
# authors: Daniel Joensen
# since: 4/09/2015
# tested with Python 3.4.2 on Windows 7 Ultimate 64 bit

import urllib
import os
import sys
import re
import wikipedia
from bs4 import BeautifulSoup

initial_url = 'http://www.boxofficemojo.com/movies/';
index_base_url = 'http://www.boxofficemojo.com';

def parse_alphabetical_index(initial_url):
	index_url_list = [];
	initial_url_soup = BeautifulSoup(urllib.request.urlopen(initial_url));
	all_tables = initial_url_soup.find_all('table');
	index_table	= all_tables[1];
	index_table_rows = index_table.find_all('tr');
	target_row = index_table_rows[1];
	target_columns = target_row.find_all('td');
	for column in target_columns:
		index_url = column.find('a').get('href');
		final_index_url = initial_url + index_url;
		index_url_list.append(final_index_url);
	return index_url_list;

def parse_index_pages(index_url_list):
	secondary_index_list = [];
	index_url_base = 'http://www.boxofficemojo.com';
	for item in index_url_list:
		secondary_index_list.append(item);
		primary_index_soup = BeautifulSoup(urllib.request.urlopen(item));
		target_table = primary_index_soup.find('div',{'class':'alpha-nav-holder'});
		target_table_tags = target_table.find_all('a');
		for tag in target_table_tags:
			secondary_index_url = tag.get('href');
			secondary_index_url = index_url_base + secondary_index_url;
			secondary_index_list.append(secondary_index_url);
	return secondary_index_list;

def build_film_page_list(secondary_index_list):
	film_url_list = [];

	for item in secondary_index_list:
		secondary_index_soup = BeautifulSoup(urllib.request.urlopen(item));
		page_urls = secondary_index_soup.find_all('a');
		for url in page_urls:
			url = url.get('href');
			url_split = url.split('=');
			if url_split[0] == '/movies/?id':
				if url == '/movies/?id=fast7.htm':
					pass
				else:
					url = url.replace(',','');
					film_url_list.append(url);
	film_url_list.append('/movies/?id=fast7.htm'); #adding back in fast7 manually, it was getting picked up on every movie page
	return film_url_list;

if __name__=="__main__":

	filename = './data/bom_film_urls.csv'
	outputFile = open(filename,'w');
	outputFile.write('url\n');

	index_url_list = parse_alphabetical_index(initial_url);
	secondary_index_list = parse_index_pages(index_url_list);
	film_url_list = build_film_page_list(secondary_index_list);

	for film_url in film_url_list:
		final_url = index_base_url + film_url;
		outputFile.write( final_url + '\n');

	outputFile.close();