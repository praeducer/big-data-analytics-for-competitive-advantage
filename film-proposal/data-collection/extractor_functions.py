# description: Accepts a film's URL and outputs the Director from Wikipedia
# author: Daniel Joensen
# since: 3/08/2015
# tested with Python 3.4.2 on windows 7 Ultimate 64 bit

import sys
from bs4 import BeautifulSoup
import urllib
import wikipedia

filmURLs = [
'http://en.wikipedia.org/wiki/(500)_Days_of_Summer',
'http://en.wikipedia.org/wiki/3_Godfathers',
'http://en.wikipedia.org/wiki/A_Chinese_Ghost_Story',
'http://en.wikipedia.org/wiki/A_Love_Song_for_Bobby_Long',
'http://en.wikipedia.org/wiki/A_Simple_Noodle_Story',
'http://en.wikipedia.org/wiki/Aag_Aur_Chingari',
'http://en.wikipedia.org/wiki/Adada',
'http://en.wikipedia.org/wiki/Air_Force_(film)',
'http://en.wikipedia.org/wiki/All_About_Anna',
'http://en.wikipedia.org/wiki/America_Screams',
'http://en.wikipedia.org/wiki/Anacondas:_The_Hunt_for_the_Blood_Orchid',
'http://en.wikipedia.org/wiki/Anonymous_Rex_(film)',
'http://en.wikipedia.org/wiki/Armed_and_Innocent',
'http://en.wikipedia.org/wiki/Atragon',
'http://en.wikipedia.org/wiki/Baby_the_Rain_Must_Fall',
'http://en.wikipedia.org/wiki/Barbie:_Mermaidia',
'http://en.wikipedia.org/wiki/Beautiful_Girls_(film)',
'http://en.wikipedia.org/wiki/Best_in_Show_(film)',
'http://en.wikipedia.org/wiki/Billy_Jack',
'http://en.wikipedia.org/wiki/Blind_Date_(1987_film)',
'http://en.wikipedia.org/wiki/Bogus_(film)',
'http://en.wikipedia.org/wiki/Breakfast_at_Tiffany%27s_(film)',
'http://en.wikipedia.org/wiki/Buffalo_%2766',
'http://en.wikipedia.org/wiki/Cahill_U.S._Marshal',
'http://en.wikipedia.org/wiki/Carnival_in_Flanders_(film)',
'http://en.wikipedia.org/wiki/Century_Hotel',
'http://en.wikipedia.org/wiki/Children_of_Heaven',
'http://en.wikipedia.org/wiki/City_of_God_(2002_film)',
'http://en.wikipedia.org/wiki/Colorful_(film)',
'http://en.wikipedia.org/wiki/Coraline_(film)',
'http://en.wikipedia.org/wiki/Cronos_(film)',
'http://en.wikipedia.org/wiki/Dalagang_Ilocana',
'http://en.wikipedia.org/wiki/Day_Watch_(film)',
'http://en.wikipedia.org/wiki/December_Heat',
'http://en.wikipedia.org/wiki/Devil_Fish_(film)',
'http://en.wikipedia.org/wiki/Divorce_Italian_Style',
'http://en.wikipedia.org/wiki/Dosti:_Friends_Forever',
'http://en.wikipedia.org/wiki/Dream_(2008_film)',
'http://en.wikipedia.org/wiki/East_Palace_West_Palace',
'http://en.wikipedia.org/wiki/Elephant_Boy_(film)',
'http://en.wikipedia.org/wiki/Er_Dong',
'http://en.wikipedia.org/wiki/Ex_Fighting',
'http://en.wikipedia.org/wiki/Farewell_to_the_King',
'http://en.wikipedia.org/wiki/Final_Fantasy_VII_Advent_Children',
'http://en.wikipedia.org/wiki/Flipped_(film)',
'http://en.wikipedia.org/wiki/Four_for_Venice',
'http://en.wikipedia.org/wiki/From_Beyond_(film)',
'http://en.wikipedia.org/wiki/Gangs_of_New_York',
'http://en.wikipedia.org/wiki/Ghost_Town_(film)',
'http://en.wikipedia.org/wiki/Gog_(film)',
'http://en.wikipedia.org/wiki/Gravity_(film)',
'http://en.wikipedia.org/wiki/Hababam_sinifi',
'http://en.wikipedia.org/wiki/Hard_Eight_(film)',
'http://en.wikipedia.org/wiki/Heartless_(2009_film)',
'http://en.wikipedia.org/wiki/Hey_Ram',
'http://en.wikipedia.org/wiki/Hollywood_Canteen_(1944_film)',
'http://en.wikipedia.org/wiki/House_by_the_River',
'http://en.wikipedia.org/wiki/Hurlyburly_(film)',
'http://en.wikipedia.org/wiki/I_Remember_Mama',
'http://en.wikipedia.org/wiki/Illusive_Tracks',
'http://en.wikipedia.org/wiki/Indecent_Proposal',
'http://en.wikipedia.org/wiki/Iron_Man_(2008_film)',
'http://en.wikipedia.org/wiki/Jack-Jack_Attack',
'http://en.wikipedia.org/wiki/Jobs_(film)',
'http://en.wikipedia.org/wiki/Ju-on_2',
'http://en.wikipedia.org/wiki/Kerd_ma_lui',
'http://en.wikipedia.org/wiki/Kiss_of_the_Dragon',
'http://en.wikipedia.org/wiki/La_belle_noiseuse',
'http://en.wikipedia.org/wiki/Lantana_(film)',
'http://en.wikipedia.org/wiki/Learning_to_Lie',
'http://en.wikipedia.org/wiki/Ley%27s_Line',
'http://en.wikipedia.org/wiki/Little_Man_(2006_film)',
'http://en.wikipedia.org/wiki/Lord_Jim_(1965_film)',
'http://en.wikipedia.org/wiki/Lovin%27_Molly',
'http://en.wikipedia.org/wiki/Maestro_(manga)',
'http://en.wikipedia.org/wiki/Manic_(film)',
'http://en.wikipedia.org/wiki/Max_(2002_film)',
'http://en.wikipedia.org/wiki/Merlin_(film)',
'http://en.wikipedia.org/wiki/Miracle_in_Lane_2',
'http://en.wikipedia.org/wiki/Monsieur_Klein',
'http://en.wikipedia.org/wiki/Mr._Blandings_Builds_His_Dream_House',
'http://en.wikipedia.org/wiki/Mutant_Aliens',
'http://en.wikipedia.org/wiki/My_Side_of_the_Mountain_(film)',
'http://en.wikipedia.org/wiki/National_Treasure_(film)',
'http://en.wikipedia.org/wiki/Nim%27s_Island',
'http://en.wikipedia.org/wiki/Nowhere_in_Africa',
'http://en.wikipedia.org/wiki/On_Borrowed_Time',
'http://en.wikipedia.org/wiki/One_Two_Three',
'http://en.wikipedia.org/wiki/Outlander_(film)',
'http://en.wikipedia.org/wiki/Paris_Is_Burning_(film)',
'http://en.wikipedia.org/wiki/Permanent_Record_(film)',
'http://en.wikipedia.org/wiki/Place_des_Cordeliers_%C3%A0_Lyon',
'http://en.wikipedia.org/wiki/Pornostar_(film)',
'http://en.wikipedia.org/wiki/Pulp_Fiction',
'http://en.wikipedia.org/wiki/Quigley_Down_Under',
'http://en.wikipedia.org/wiki/Ready_to_Rumble',
'http://en.wikipedia.org/wiki/Resurrecting_the_Champ',
'http://en.wikipedia.org/wiki/Road_Rage_(film)',
'http://en.wikipedia.org/wiki/Roswell_(1994_film)',
'http://en.wikipedia.org/wiki/Sally_(1929_film)'
]

wikipediaRoot = 'http://en.wikipedia.org';

for filmURL in filmURLs:
	def director_extractor(filmURL):
		filmPageSoup = BeautifulSoup(urllib.request.urlopen(filmURL));
		summaryTable = filmPageSoup.find('table',{ 'class' : 'infobox vevent'});
		
		directorNames = [];

		try:
			summaryTableRows = summaryTable.find_all('tr');

			for row in summaryTableRows:
				if 'Directed' in row.text:
					directorNameATags = row.find_all('a');
					for tag in directorNameATags:
						if tag['href'][0] == "/":			
							directorName = tag['title'].replace(',','').replace('\'','').replace('"','');
							directorURL = wikipediaRoot + tag['href'].replace(',','').replace('\'','').replace('"','');
							directorTuple = {'name': directorName, 'url': directorURL};
							directorNames.append(directorTuple);
		except AttributeError:
			directorNames.append("null");

		return directorNames;


	def actor_extractor(filmURL):
		filmPageSoup = BeautifulSoup(urllib.request.urlopen(filmURL));
		summaryTable = filmPageSoup.find('table',{ 'class' : 'infobox vevent'});
		
		actorNames = [];

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
							actorNames.append(actorTuple);
		except AttributeError:
			actorNames.append("null");

		return actorNames;

	actorNames = actor_extractor(filmURL);
	for actorName in actorNames:
		print(actorName);
