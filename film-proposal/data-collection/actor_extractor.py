# author: Paul Prae
# since: 2/21/2015

from bs4 import BeautifulSoup
import urllib
import wikipedia

wikipediaRoot = 'http://en.wikipedia.org';
actorsAwardPage = wikipediaRoot + '/wiki/Screen_Actors_Guild_Award';
actorsAwardSoup = BeautifulSoup(urllib.urlopen(actorsAwardPage));

winnersForYearsHeader = actorsAwardSoup.find('span', { 'id' : 'List_of_nominees_and_winners'}).parent;
winnersForYears = winnersForYearsHeader.find_next_sibling('ul');
winnersForYearsATags = winnersForYears.find_all('a');
winnersForYearsURLs = [];
for item in winnersForYearsATags:
	if item.has_attr('href'):
		winnersForYearsURLs.append(wikipediaRoot + item['href']);

for winnersForAYearPage in winnersForYearsURLs:

	winnersForAYearSoup = BeautifulSoup(urllib.urlopen(winnersForAYearPage));
	winnersForAYearTitle = winnersForAYearSoup.title.contents[0];
	winnersForAYearTitle = winnersForAYearTitle.replace(' - Wikipedia, the free encyclopedia','');	

	filmWinnersForAYearTable = winnersForAYearSoup.find('table',{ 'class' : 'wikitable'});
	if filmWinnersForAYearTable is not None:
		filmWinnersForAYearRows = filmWinnersForAYearTable.find_all('tr');

		leadActorsColumns = filmWinnersForAYearRows[1].find_all('td');
		leadMaleActorATag = leadActorsColumns[0].find_next('a');
		leadFemaleActorATag = leadActorsColumns[1].find_next('a');

		supportActorsColumns = filmWinnersForAYearRows[3].find_all('td');
		supportMaleActorATag = supportActorsColumns[0].find_next('a');
		supportFemaleActorATag = supportActorsColumns[1].find_next('a');
	else:	
		leadMaleActorHeader = winnersForAYearSoup.find('span', { 'id' : 'Outstanding_Performance_by_a_Male_Actor_in_a_Leading_Role'});
		leadFemaleActorHeader = winnersForAYearSoup.find('span', { 'id' : 'Outstanding_Performance_by_a_Female_Actor_in_a_Leading_Role'});
		supportMaleActorHeader = winnersForAYearSoup.find('span', { 'id' : 'Outstanding_Performance_by_a_Male_Actor_in_a_Supporting_Role'});
		supportFemaleActorHeader = winnersForAYearSoup.find('span', { 'id' : 'Outstanding_Performance_by_a_Female_Actor_in_a_Supporting_Role'});
		leadMaleActorATag = leadMaleActorHeader.find_next('b').find_next('a');
		leadFemaleActorATag = leadFemaleActorHeader.find_next('b').find_next('a');
		supportMaleActorATag = supportMaleActorHeader.find_next('b').find_next('a');
		supportFemaleActorATag = supportFemaleActorHeader.find_next('b').find_next('a');

	leadMaleActor = leadMaleActorATag['title'];
	leadMaleActorURL = wikipediaRoot + leadMaleActorATag['href'];
	print(leadMaleActor + ',' + leadMaleActorURL + ',male,lead,' + winnersForAYearTitle);
	
	leadFemaleActor = leadFemaleActorATag['title'];
	leadFemaleActorURL = wikipediaRoot + leadFemaleActorATag['href'];
	print(leadFemaleActor + ',' + leadFemaleActorURL + ',female,lead,' + winnersForAYearTitle);

	supportMaleActor = supportMaleActorATag['title'];
	supportMaleActorURL = wikipediaRoot + supportMaleActorATag['href'];
	print(supportMaleActor + ',' + supportMaleActorURL + ',male,support,' + winnersForAYearTitle);

	supportFemaleActor = supportFemaleActorATag['title'];
	supportFemaleActorURL = wikipediaRoot + supportFemaleActorATag['href'];
	print(supportFemaleActor + ',' + supportFemaleActorURL + ',female,support,' + winnersForAYearTitle);

