import urllib
from bs4 import BeautifulSoup
import pandas as pd

# get the teams
BASE_URL = 'http://espn.go.com/nba/team/schedule/_/name/%s/year/%s/seasontype/2'
url = BASE_URL % ('bos', '2016')
html = urllib.urlopen(url).read()
soup = BeautifulSoup(html)
print soup.prettify()