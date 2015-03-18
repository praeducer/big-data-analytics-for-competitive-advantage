# Readme
This section describes the core source files that are necessary for collecting the data we need to analyze. It will list the scripts in the order they should be ran, since the output of a script may be necessary for the input of the next. Each section will contain a description of the script, how to run the script, the input requirements, and what to expect for output. We will start by listing the project's dependencies. 

### Environment Configuration
#### Python Libraries
These scripts use fairly common Python 3 libraries. They were tested on Linux (CentOS 7) and Windows systems running Python 3.3 or later. Before running any script, make sure your environment is setup with the correct version of Python and all of the following dependencies.

Primary libraries used:
+ BeautifulSoup - Beautiful Soup is a Python library for pulling data out of HTML and XML files. It works with your favorite parser to provide idiomatic ways of navigating, searching, and modifying the parse tree. http://www.crummy.com/software/BeautifulSoup/bs4/doc/ 
+ Wikipedia Python API - Wikipedia is a Python library that makes it easy to access and parse data from Wikipedia. You can search Wikipedia, get article summaries, get data like links and images from a page, and more. Wikipedia wraps the MediaWiki API (https://www.mediawiki.org/wiki/API:Main_page). https://pypi.python.org/pypi/wikipedia/
+ urllib - urllib is a package that collects several modules for working with URLs. It can open, read, and parse them. https://docs.python.org/3/library/urllib.html
+ requests - Requests takes all of the work out of Python HTTP/1.1 — making your integration with web services seamless. Requests is ready for today’s web. http://docs.python-requests.org/en/latest/

We also used some more general use libraries such as 'sys', 'os', 'fileinput', 'csv', 'datetime', and 're'.

#### Directory Structure
All scripts should be ran from the same location. This location should have a directory created called 'data' where some of the output will be stored.

### General Notes
+ Unless otherwise noted, all scripts can be ran by typing 'python name-of-file.py'.
+ Some scripts will require an input file. Unless noted below, assume input is hard coded.
+ Output will typically be placed where the script is ran or into a './data/' directory. Please create this directory ahead of time.
+ Some scripts will also output the state of the script to the terminal but this is for logging only.
+ When pulling any entity from Wikipedia, we also grab the URL that represents that entity. This is perfect for uniquely identifying an entity such as a film or an actor. These URLs can then be used to join different data sets.

### Step One: Extract the Films URLs
##### film_url_extractor.py
This script will extract film titles, film Wikipedia URLs, and film release year (because year happened to be easy to collect during this process) from the 'List of Films' article on Wikipedia. This list is organized by year and is also organized alphabetically. We found alphabetically to be a more straightforward approach to mine.

###### Input
You do not need to provide any input via the command line. Since this file is custom built for a specific article, its input is hard coded. The file starts web mining at http://en.wikipedia.org/wiki/List_of_films:_numbers. From there it first mines the other pages it needs to mine for data such as http://en.wikipedia.org/wiki/List_of_films:_A, http://en.wikipedia.org/wiki/List_of_films:_B, http://en.wikipedia.org/wiki/List_of_films:_C, etc. The function that creates this index of lists of films is called 'parseFilmIndex(startURL)'. These end up being the input to the function that extracts the data, 'parseAllFilmPages(listOfFilmsURLs)'. Most of the data ends up being inside an item element which is parsed with 'parseITag(iTag)'.

###### Output
It will write a .csv file to './data/film_urls.csv' with the columns 'url,title,year'. e.g.

url,title,year

http://en.wikipedia.org/wiki/Lifeforce_(film), 'Lifeforce (film)',1985

http://en.wikipedia.org/wiki/Pat_and_Mike, 'Pat and Mike',1952

http://en.wikipedia.org/wiki/The_Tales_of_Hoffmann_(film), 'The Tales of Hoffmann (film)',1951

http://en.wikipedia.org/wiki/All_or_Nothing_(film), 'All or Nothing (film)',2002

http://en.wikipedia.org/wiki/Malli_(film), 'Malli (film)',1998


### Step Two: Download the Films
##### download_films.py
Given a list of URLs for pages to download, this script stores the HTML from these pages locally.

###### Input
This script simply takes the output file, './data/film_urls.csv', from 'film_url_extractor.py' and downloads the content from every URL in the first column. This technically could work on an arbitrary new line separated list of URLs from any source.

###### Output
For each URL provided, there will be a 'page-name.html' file stored in './data/films/'. This file will contain the source code found at the given URL.


### Step Three: Parse the Film Files
##### film_data_extractor.py
This is the script that does the primary data extraction. This script will parse all of the HTML files stored in './data/films/'. It turns each file into an HTML Beautiful Soup object and passes this object into a series of functions. Each function parses the page and returns a specific piece of data. All of this data for all of the films is placed in a single .csv file.

###### Input
This script will process every file located in './data/films/'. It grabs every file in the given directory and processes it when possible. It assumes they are Wikipedia film pages downloaded directly from the web. It will only need the body of the pages.

###### Output
It will create a .csv file where each row represents a film. Each row will have the following columns:

'title', 'url', 'release date', 'release year', 'budget', 'revenue', 'director', 'actor', 'distributor', 'genre'.

Each of these will typically be the direct output from one of the several extractor functions defined in the file e.g. 'actor_extractor(filmPageSoup)' or 'budget_extractor(filmPageSoup)'. If the data is not found, 'null' is returned.

If the column contains a list, it will be pipe, '|', separated. e.g.  'genre':

`
fantasy|action|comedy
`

If there are multiple value inside the pipe separated values, they will be separated with a semi-colon. e.g. 'actor':

`
Jim Carrey;http://en.wikipedia.org/wiki/Jim_Carrey|Peter Riegert;http://en.wikipedia.org/wiki/Peter_Riegert|Peter Greene;http://en.wikipedia.org/wiki/Peter_Greene|Amy Yasbeck;http://en.wikipedia.org/wiki/Amy_Yasbeck|Richard Jeni;http://en.wikipedia.org/wiki/Richard_Jeni|Cameron Diaz;http://en.wikipedia.org/wiki/Cameron_Diaz
`

Here are a few example rows:

`'Fullmetal Alchemist the Movie: Conqueror of Shamballa',http://en.wikipedia.org/wiki/Fullmetal_Alchemist_the_Movie:_Conqueror_of_Shamballa,2005-07-23,2005,null,null,Seiji Mizushima;http://en.wikipedia.org/wiki/Seiji_Mizushima,Romi Park;http://en.wikipedia.org/wiki/Romi_Park|Rie Kugimiya;http://en.wikipedia.org/wiki/Rie_Kugimiya|Megumi Toyoguchi;http://en.wikipedia.org/wiki/Megumi_Toyoguchi|Tōru Ōkawa;http://en.wikipedia.org/wiki/T%C5%8Dru_%C5%8Ckawa|Kenji Utsumi;http://en.wikipedia.org/wiki/Kenji_Utsumi|Michiko Neya;http://en.wikipedia.org/wiki/Michiko_Neya|Keiji Fujiwara;http://en.wikipedia.org/wiki/Keiji_Fujiwara|Kotono Mitsuishi;http://en.wikipedia.org/wiki/Kotono_Mitsuishi|Masashi Ebara;http://en.wikipedia.org/wiki/Masashi_Ebara|Unshō Ishizuka;http://en.wikipedia.org/wiki/Unsh%C5%8D_Ishizuka|Hidekatsu Shibata;http://en.wikipedia.org/wiki/Hidekatsu_Shibata|Miyoko Asō;http://en.wikipedia.org/wiki/Miyoko_As%C5%8D|Masane Tsukayama;http://en.wikipedia.org/wiki/Masane_Tsukayama|Shun Oguri;http://en.wikipedia.org/wiki/Shun_Oguri|Miyuu Sawai;http://en.wikipedia.org/wiki/Miyuu_Sawai,Shochiku;http://en.wikipedia.org/wiki/Shochiku,animated`
***
`'The Mask (film)',http://en.wikipedia.org/wiki/The_Mask_(film),1994-07-29,1994,23000000,3516 million,Chuck Russell;http://en.wikipedia.org/wiki/Chuck_Russell,Jim Carrey;http://en.wikipedia.org/wiki/Jim_Carrey|Peter Riegert;http://en.wikipedia.org/wiki/Peter_Riegert|Peter Greene;http://en.wikipedia.org/wiki/Peter_Greene|Amy Yasbeck;http://en.wikipedia.org/wiki/Amy_Yasbeck|Richard Jeni;http://en.wikipedia.org/wiki/Richard_Jeni|Cameron Diaz;http://en.wikipedia.org/wiki/Cameron_Diaz,New Line Productions;http://en.wikipedia.org/wiki/New_Line_Productions,fantasy|action|comedy`
***
`'Clueless (film)',http://en.wikipedia.org/wiki/Clueless_(film),1995-07-19,1995,20000000,56631572,Amy Heckerling;http://en.wikipedia.org/wiki/Amy_Heckerling,Alicia Silverstone;http://en.wikipedia.org/wiki/Alicia_Silverstone|Stacey Dash;http://en.wikipedia.org/wiki/Stacey_Dash|Brittany Murphy;http://en.wikipedia.org/wiki/Brittany_Murphy|Paul Rudd;http://en.wikipedia.org/wiki/Paul_Rudd|Donald Faison;http://en.wikipedia.org/wiki/Donald_Faison|Breckin Meyer;http://en.wikipedia.org/wiki/Breckin_Meyer|Dan Hedaya;http://en.wikipedia.org/wiki/Dan_Hedaya,Paramount Pictures;http://en.wikipedia.org/wiki/Paramount_Pictures,comedy`


### Collection of Notable Contributors
#### Notable Actors
##### actor_extractor.py
This script mines all of the actors that won the Screen Actors Guild Award.

###### Input
It only needs the root page, http://en.wikipedia.org/wiki/Screen_Actors_Guild_Award, to start with. This is hard coded in the script. From there it is able to pull all of the pages that represent each year the awards were held (e.g. http://en.wikipedia.org/wiki/1st_Screen_Actors_Guild_Awards and http://en.wikipedia.org/wiki/21st_Screen_Actors_Guild_Awards). On those specific award ceremony pages, we gain access to the actual actors who won that year.

###### Output
From each instance of an awards ceremony, the script grabs all male and female actors that received awards for an outstanding performance (e.g. "Outstanding Performance by a Male Actor in a Supporting Role" or "Outstanding Performance by a Female Actor in a Leading Role").

For each actor it is able to pull out the following information:
'name,url,gender,role,event'

Here are a few example rows from 'notable_actors.csv':

`
'Tom Hanks',http://en.wikipedia.org/wiki/Tom_Hanks,male,lead,'1st Screen Actors Guild Awards'
'Jodie Foster',http://en.wikipedia.org/wiki/Jodie_Foster,female,lead,'1st Screen Actors Guild Awards'
'Martin Landau',http://en.wikipedia.org/wiki/Martin_Landau,male,support,'1st Screen Actors Guild Awards'
`

#### Notable Directors
##### director_extractor.py
This script grabs all notable directors as listed on Wikipedia. It uses a similar technique as in the actor extractor.

###### Input
It takes in the page and list found at http://en.wikipedia.org/wiki/Film_director#Notable_individuals. This is hard coded in the script.

###### Output
It extracts each director's name and their Wikipedia URL. They are each placed in a final .csv file titled, 'directors_list.csv'.

#### Notable Distributors
##### producer_extractor.py
This script simply extracts a list of film filmmaking, film distribution companies from Wikipedia. It uses a similar technique as in the director extractor.

###### Input
It pulls the name and Wikipedia URLs of the production companies from the 'Notable production companies' section at http://en.wikipedia.org/wiki/List_of_film_production_companies.

###### Output
It pulls the names and URLs of each entity as with the other extractor scripts.

Here are a few example rows from 'producers_list.csv':

`
'Columbia Pictures',http://en.wikipedia.org/wiki/Columbia_Pictures'
'TriStar Pictures',http://en.wikipedia.org/wiki/TriStar_Pictures'
'Sony Pictures Classics',http://en.wikipedia.org/wiki/Sony_Pictures_Classics'
`

### Lessons learned while web mining Wikipedia:
+ The Wikipedia Python API library is not magical. Paul hardly used it at all when pulling notable actors for example. We mostly did standard web mining with Beautiful Soup.
+ Wikipedia pages that are supposed to have the same exact type of content can be formatted completely different. This forces your code to handle several variations. Each film page could be of a different variety. e.g. Like on several others, formatting on this page http://en.wikipedia.org/wiki/6th_Screen_Actors_Guild_Awards is different from this page http://en.wikipedia.org/wiki/21st_Screen_Actors_Guild_Awards. Our code had to take a different approach for each to extract the actors.
+ If any of the HTML we are targeting changes, our code will break. When targeting content, we needed to be as specific as possible and rely on as few elements and attributes as possible.
+ Sometimes copying and pasting is faster than writing a script but will not be as reproducible. One particular task we tackled, pulling notable actors, was a great learning and portfolio building experience but too tedious for the end result.
