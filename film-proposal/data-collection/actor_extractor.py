from bs4 import BeautifulSoup
import urllib
import wikipedia

actorsAwardPage = "http://en.wikipedia.org/wiki/Screen_Actors_Guild_Award";
actorsAwardSoup = BeautifulSoup(urllib.urlopen(actorsAwardPage));
listOfWinnersHeader = actorsAwardSoup.find(id="List_of_nominees_and_winners").parent;
listOfWinners = listOfWinnersHeader.find_next_sibling("ul");
print(listOfWinners);

