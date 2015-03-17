## readme
This file describes the core source files that are necessary for collecting the data we need to analyze. It will list the scripts in the order they should be ran, since the output of a script may be necessary for the input of the next. Each section will contain a description of the script, how to run the script, the input requirements, and what to expect for output. We will start by listing the project's dependencies. 

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
+ Unless otherwise noted, all scripts can be ran by typing 'python <name-of-file.py>'.
+ Some scripts will require an input file. Unless noted below, assume input is hard coded.
+ Output will typically be placed where the scripts is ran or into a './data/' directory. Please create this directory ahead of time.
+ Some scripts will also output the state of the script to the terminal but this is for logging only.

### Step One: Extract the Films URLs
##### film_url_extractor.py
This script will extract film titles, film Wikipedia URLs, and film release year (because year happened to be easy to collect during this process) from the 'List of Films' article on Wikipedia. This list is organized by year and is also organized alphabetically. We found alphabetically to be a more straightforward approach.

###### Input
You do not need to provide any input via the command line. Since this file is custom built for a specific article, its input is hard coded. The file starts web mining at http://en.wikipedia.org/wiki/List_of_films:_numbers. From there it first mines the other pages it needs to mine for data such as http://en.wikipedia.org/wiki/List_of_films:_A, http://en.wikipedia.org/wiki/List_of_films:_B, http://en.wikipedia.org/wiki/List_of_films:_C, etc. The function that creates this index of lists of films is called 'parseFilmIndex(startURL)'. These end up being the input to the function that extracts the data, 'parseAllFilmPages(listOfFilmsURLs)'. Most of the data ends up being inside an item element which is parsed with 'parseITag(iTag)'.

###### Output
It will write a .csv file to './data/film_urls.csv' with the columns 'url,title,year'. e.g.
`
url,title,year
http://en.wikipedia.org/wiki/Lifeforce_(film),'Lifeforce (film)',1985
http://en.wikipedia.org/wiki/Pat_and_Mike,'Pat and Mike',1952
http://en.wikipedia.org/wiki/The_Tales_of_Hoffmann_(film),'The Tales of Hoffmann (film)',1951
http://en.wikipedia.org/wiki/All_or_Nothing_(film),'All or Nothing (film)',2002
http://en.wikipedia.org/wiki/Malli_(film),'Malli (film)',1998
`

### Step Two: Download the Films
##### download_films.py
This script stores the HTML from a web page locally given a list of URLs of each page to download.

###### Input
This script simply takes the output file from 'film_url_extractor.py' and downloads the content from every URL in the first column. This technically could work on an arbitrary new line separated list of URLs.

###### Output
For each URL provided, there will be a '<page-name>.html' file stored in './data/films/'. This file will contain the source code found at the given URL.

### Step Three: Parse the Film Files
##### film_data_extractor.py
This is the script that does the primary data extraction. This script will parse all of the HTML files stored in './data/films/'.

###### Input
This film will process every file located in './data/films/'. 

### Collection of Notable Contributors

#### Notable Directors
##### director_extractor.py

#### Notable Distributors
##### producer_extractor.py

#### Notable Actors
##### actor_extractor.py
