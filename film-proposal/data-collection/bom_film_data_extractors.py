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
from datetime import datetime
from bs4 import BeautifulSoup

#TODO: Finish integrating the urls from the excel input file

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
	try:
		revenue_table = movie_soup.find('div', {'class':'mp_box_content'});
		revenue_table_rows = revenue_table.find_all('tr');
		domestic_total = 'null';
		for row in revenue_table_rows:
			if 'Domestic' in row.text:
				domestic_total = row.text;
				domestic_total = domestic_total.split()[1];
				domestic_total = domestic_total.replace('$','').replace(',','');
	except IndexError:
		domestic_total = 'null';
	return domestic_total;

def find_foreign_total(movie_soup):
	try:
		revenue_table = movie_soup.find('div', {'class':'mp_box_content'});
		revenue_table_rows = revenue_table.find_all('tr');
		foreign_total = 'null';
		for row in revenue_table_rows:
			if 'Foreign' in row.text:
				foreign_total = row.text;
				foreign_total = foreign_total.split()[2];
				foreign_total = foreign_total.replace('$','').replace(',','');
	except IndexError:
		domestic_total = 'null';
	return foreign_total;

def find_global_total(movie_soup):
	try:
		revenue_table = movie_soup.find('div', {'class':'mp_box_content'});
		revenue_table_rows = revenue_table.find_all('tr');
		global_total = 'null';
		for row in revenue_table_rows:
			if 'Worldwide' in row.text:
				global_total = row.text;
				global_total = global_total.split()[2];
				global_total = global_total.replace('$','').replace(',','');
	except IndexError:
		domestic_total = 'null';
	return global_total;

def find_opening_weekend_total(movie_soup):
	try:
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
							opening_weekend_total = item
							opening_weekend_total = opening_weekend_total.replace('$','').replace(',','');
	except IndexError:
		opening_weekend_total = 'null';
	return opening_weekend_total;

def find_number_of_theaters(movie_soup):
	try:	
		revenue_table = movie_soup.find_all('div', {'class':'mp_box_content'});
		target_table = revenue_table[1];
		target_table_rows = target_table.find_all('tr');
		number_of_theaters = 'null';
		if len(target_table_rows) == 0:
			number_of_theaters = 'null';
		else:
			for row in target_table_rows:
				if 'Widest' in row.text:
					row_list = row.text.split();
					number_of_theaters = row_list[2];
					number_of_theaters = number_of_theaters.replace(',','');
	except IndexError:
		number_of_theaters = 'null';
	return number_of_theaters;

def find_mpaa_rating(movie_soup):
	center_table = movie_soup.findChildren('center')[0];
	center_table_data = center_table.findChildren('tr');#[5];
	#center_table_data = center_table_data[len(center_table_data)-2];
	for row in center_table_data:
		if 'MPAA' in row.text:
			mpaa_rating = row.find('b');
			mpaa_rating = mpaa_rating.text;
	return mpaa_rating;

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

	try:
		release_date = datetime.strptime(release_date, "%B %d, %Y");
		release_date = datetime.strftime(release_date, "%m/%d/%Y");
	except ValueError:
		release_date = release_date;

	return release_date;

def find_run_time(movie_soup):
	try:
		center_table = movie_soup.findChildren('center')[0];
		center_table_data = center_table.findChildren('tr');
		for row in center_table_data:
			if 'Genre' in row.text:
				if 'Runtime' in row.text:
					run_time = row.find_all('b');
					run_time = run_time[1].text;
			else:
				if 'Runtime' in row.text:
					run_time = row.find('b');
					run_time = run_time.text;
		if run_time == 'N/A':
			pass
		else:
			run_time = run_time.replace('hrs.','').replace('min.','');
			run_time = run_time.split();
			run_time = (int(run_time[0])*60) + (int(run_time[1]));
			run_time = str(run_time);
	except IndexError:
		run_time = 'null';

	return run_time;

film_url_list = [
'http://www.boxofficemojo.com/movies/?id=feast.htm',
'http://www.boxofficemojo.com/movies/?id=findingnemo.htm',
'http://www.boxofficemojo.com/movies/?id=fleshandblood.htm',
'http://www.boxofficemojo.com/movies/?id=forthemoment.htm',
'http://www.boxofficemojo.com/movies/?id=fraude.htm',
'http://www.boxofficemojo.com/movies/?id=front.htm',
'http://www.boxofficemojo.com/movies/?id=garden09.htm',
'http://www.boxofficemojo.com/movies/?id=ghosttown.htm',
'http://www.boxofficemojo.com/movies/?id=glenorglenda53.htm',
'http://www.boxofficemojo.com/movies/?id=gonegirl.htm',
'http://www.boxofficemojo.com/movies/?id=graduate.htm',
'http://www.boxofficemojo.com/movies/?id=greetingsfromtimbuckley.htm',
'http://www.boxofficemojo.com/movies/?id=haikutunnel.htm',
'http://www.boxofficemojo.com/movies/?id=happytimes.htm',
'http://www.boxofficemojo.com/movies/?id=hayride2.htm',
'http://www.boxofficemojo.com/movies/?id=hellbound.htm',
'http://www.boxofficemojo.com/movies/?id=highheelsandlowlifes.htm',
'http://www.boxofficemojo.com/movies/?id=hollywoodland.htm',
'http://www.boxofficemojo.com/movies/?id=hotspot.htm',
'http://www.boxofficemojo.com/movies/?id=surviveaplague.htm',
'http://www.boxofficemojo.com/movies/?id=icouldneverbeyourwoman.htm',
'http://www.boxofficemojo.com/movies/?id=icemancometh.htm',
'http://www.boxofficemojo.com/movies/?id=inmyfathersden.htm',
'http://www.boxofficemojo.com/movies/?id=inlandempire.htm',
'http://www.boxofficemojo.com/movies/?id=invisiblewoman.htm',
'http://www.boxofficemojo.com/movies/?id=oneshot.htm',
'http://www.boxofficemojo.com/movies/?id=jewinthelotus.htm',
'http://www.boxofficemojo.com/movies/?id=ghosttown.htm',
'http://www.boxofficemojo.com/movies/?id=glenorglenda53.htm',
'http://www.boxofficemojo.com/movies/?id=gonegirl.htm',
'http://www.boxofficemojo.com/movies/?id=graduate.htm',
'http://www.boxofficemojo.com/movies/?id=greetingsfromtimbuckley.htm',
'http://www.boxofficemojo.com/movies/?id=haikutunnel.htm',
'http://www.boxofficemojo.com/movies/?id=happytimes.htm',
'http://www.boxofficemojo.com/movies/?id=hayride2.htm',
'http://www.boxofficemojo.com/movies/?id=hellbound.htm',
'http://www.boxofficemojo.com/movies/?id=highheelsandlowlifes.htm',
'http://www.boxofficemojo.com/movies/?id=hollywoodland.htm',
'http://www.boxofficemojo.com/movies/?id=hotspot.htm',
'http://www.boxofficemojo.com/movies/?id=surviveaplague.htm',
'http://www.boxofficemojo.com/movies/?id=icouldneverbeyourwoman.htm',
'http://www.boxofficemojo.com/movies/?id=icemancometh.htm',
'http://www.boxofficemojo.com/movies/?id=inmyfathersden.htm',
'http://www.boxofficemojo.com/movies/?id=inlandempire.htm',
'http://www.boxofficemojo.com/movies/?id=invisiblewoman.htm',
'http://www.boxofficemojo.com/movies/?id=oneshot.htm',
'http://www.boxofficemojo.com/movies/?id=jewinthelotus.htm'
]

"""

#NOTE: Left in for testing purposes.

for film_url in film_url_list:
	movie_soup = BeautifulSoup(urllib.request.urlopen(film_url));	
	movie_name = find_movie_name(movie_soup);
	run_time = find_run_time(movie_soup);
	release_date = find_release_date(movie_soup);
	mpaa_rating = find_mpaa_rating(movie_soup);	
	opening_weekend_total = find_opening_weekend_total(movie_soup);
	number_of_theaters = find_number_of_theaters(movie_soup);
	domestic_total = find_domestic_total(movie_soup);
	foreign_total = find_foreign_total(movie_soup);
	global_total = find_global_total(movie_soup);

	print("Movie Name: ");
	print(movie_name);

	print("Number of Theaters:");
	print(number_of_theaters);

#	print("Release Date:");
#	print(release_date);
"""

"""
filename = './data/bom_film_urls.csv';
bom_film_urls = [];
film_url_reader = csv.reader(open(filename));
for row in film_url_reader:
	film_urls.append(row);

for item in film_urls:
	print (item);
"""

if __name__=="__main__":

	filename = './data/bom_film_data.csv'
	outputFile = open(filename,'w');
	outputFile.write('Movie name, URL, Release Date, MPAA Rating, Run Time,  Opening Weekend Total, Number of Theaters, Domestic Total Sales, Foreign Total Sales, Global Total Sales\n');

	for film_url in film_url_list:
		movie_soup = BeautifulSoup(urllib.request.urlopen(film_url));	
		movie_name = find_movie_name(movie_soup);
		release_date = find_release_date(movie_soup);
		mpaa_rating = find_mpaa_rating(movie_soup);	
		run_time = find_run_time(movie_soup);
		opening_weekend_total = find_opening_weekend_total(movie_soup);
		number_of_theaters = find_number_of_theaters(movie_soup);
		domestic_total = find_domestic_total(movie_soup);
		foreign_total = find_foreign_total(movie_soup);
		global_total = find_global_total(movie_soup);

		outputFile.write( movie_name + ',' + film_url + ',' + release_date + ',' + mpaa_rating + ',' + run_time + ',' + opening_weekend_total + ',' + number_of_theaters + ',' + domestic_total + ',' + foreign_total + ',' + global_total + '\n');

	outputFile.close();
