# Get and display all links from a web page

#Import resources
import urllib.request
from bs4 import BeautifulSoup

#Identify URL
url="http://www.quora.com/Where-can-I-find-large-datasets-open-to-the-public"

#Open and read the URL
connection = urllib.request.urlopen(url)
html = connection.read()

#Scan the page
soupresults = BeautifulSoup(html)

#Start the search
links = soupresults.find_all('a')

#Loop start
for tag in links:
    #Make sure this is a link
    link = tag.get('href',None)

    #If it found anything, print it
    if link != None:
        #an optional a filter for short stuff that shouldn't be included
        if len(link) > 2:
            print (link)