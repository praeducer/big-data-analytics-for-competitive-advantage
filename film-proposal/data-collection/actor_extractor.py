# TODO:
#	Handle special cases for html formatting on some of the pages. e.g.:
#		http://en.wikipedia.org/wiki/18th_Screen_Actors_Guild_Awards
#		http://en.wikipedia.org/wiki/17th_Screen_Actors_Guild_Awards
#	Add in a column for which award ceremony it was, e.g. '17th Screen Actors Guild Awards'. Should just be the title of the wikipedia page. Wikipedia library can do this easy.

from bs4 import BeautifulSoup
import urllib
import wikipedia

wikipediaRoot = 'http://en.wikipedia.org';
actorsAwardPage = wikipediaRoot + '/wiki/Screen_Actors_Guild_Award';
actorsAwardSoup = BeautifulSoup(urllib.urlopen(actorsAwardPage));

winnersForYearsHeader = actorsAwardSoup.find(id='List_of_nominees_and_winners').parent;
winnersForYears = winnersForYearsHeader.find_next_sibling('ul');
winnersForYearsATags = winnersForYears.find_all('a');
winnersForYearsURLs = [];
for item in winnersForYearsATags:
	if item.has_attr('href'):
		winnersForYearsURLs.append(wikipediaRoot + item['href']);

for winnersForAYearPage in winnersForYearsURLs:
	winnersForAYearSoup = BeautifulSoup(urllib.urlopen(winnersForAYearPage));
	filmWinnersForAYearHeader = winnersForAYearSoup.find(id='Film').parent;
	filmWinnersForAYearTable = filmWinnersForAYearHeader.find_next_sibling('table');
	filmWinnersForAYearRows = filmWinnersForAYearTable.find_all('tr');

	leadActorsColumns = filmWinnersForAYearRows[1].find_all('td');
	leadMaleActorATag = leadActorsColumns[0].find_all('a')[0];
	leadMaleActor = leadMaleActorATag['title'];
	leadMaleActorURL = wikipediaRoot + leadMaleActorATag['href'];
	print(leadMaleActor + ',' + leadMaleActorURL + ',male,lead');
	leadFemaleActorATag = leadActorsColumns[1].find_all('a')[0];
	leadFemaleActor = leadFemaleActorATag['title'];
	leadFemaleActorURL = wikipediaRoot + leadFemaleActorATag['href'];
	print(leadFemaleActor + ',' + leadFemaleActorURL + ',female,lead');

	supportActorsColumns = filmWinnersForAYearRows[3].find_all('td');
	supportMaleActorATag = supportActorsColumns[0].find_all('a')[0];
	supportMaleActor = supportMaleActorATag['title'];
	supportMaleActorURL = wikipediaRoot + supportMaleActorATag['href'];
	print(supportMaleActor + ',' + supportMaleActorURL + ',male,support');
	supportFemaleActorATag = supportActorsColumns[1].find_all('a')[0];
	supportFemaleActor = supportFemaleActorATag['title'];
	supportFemaleActorURL = wikipediaRoot + supportFemaleActorATag['href'];
	print(supportFemaleActor + ',' + supportFemaleActorURL + ',female,support');

