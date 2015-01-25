# Get and display all links from a web page

# Import resources
import urllib.request
import csv
import os
from bs4 import BeautifulSoup

# Identify URL
url="http://www.quora.com/Where-can-I-find-large-datasets-open-to-the-public"

# Open and read the URL
connection = urllib.request.urlopen(url)
html = connection.read()

# Scan the page
soupresults = BeautifulSoup(html)

# Start the search
links = soupresults.find_all('a')

# Create a writer so we can save a csv
currentDir = os.path.dirname(__file__)
with os.open(currentDir, os.O_WRONLY) as csv_file:
	writer = csv.writer(csv_file, delimiter=',')
	# Loop start
	for tag in links:
	    # Make sure this is a link
	    link = tag.get('href',None)
	    # If it found anything, print it
	    if link != None:
	        # Filter out relative links and anchor tags
	        if len(link) > 0 and link[0] != '/' and link[0] != '#':
	            writer.writerow(link)