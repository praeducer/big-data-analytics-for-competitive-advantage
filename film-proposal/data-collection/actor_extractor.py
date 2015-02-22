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

winnersForAYearPage = winnersForYearsURLs[0];
winnersForAYearSoup = BeautifulSoup(urllib.urlopen(winnersForAYearPage));
filmWinnersForAYearHeader = winnersForAYearSoup.find(id='Film').parent;
filmWinnersForAYearTable = filmWinnersForAYearHeader.find_next_sibling('table');filmWinnersForAYearRows = filmWinnersForAYearTable.find_all('tr');
leadActorsColumns = filmWinnersForAYearRows[1].find_all('td');
leadMaleActorATag = leadActorsColumns[0].find_all('a')[0];
leadMaleActor = leadMaleActorATag['title'];
leadMaleActorURL = wikipediaRoot + leadMaleActorATag['href'];
print(leadMaleActor);
print(leadMaleActorURL);

