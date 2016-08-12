# coding: utf-8

import urllib
from bs4 import BeautifulSoup
import pandas as pd
import pickle as pk


def Get_All_Teams():
    # get the teams
    url = 'http://espn.go.com/nba/teams'
    html = urllib.urlopen(url).read()
    soup = BeautifulSoup(html, 'lxml')
    # print (soup.prettify())
    tables = soup.find_all('ul', class_ = 'medium-logos')

    tables[0].find_all('li')[0].h5.a

    name_pref_Tuples = []
    city_name_Dict = {}
    for table in tables:
        lis = table.find_all('li')
        for li in lis:
            info = li.h5.a
            team_url = info['href']
            team_name = info.text
            pref = team_url.split('/')[-2]
            city_name = ' '.join(info.text.split()[:-1])
            if team_name == 'Portland Trail Blazers':
                city_name = 'Portland'
            city_name_Dict[city_name] = team_name
            name_pref_Tuples.append((team_name, pref))

    print 'output two files: city_name.pickle and name_pref.pickle'
    print 'city_name.pickle is a dict with (city, team_name) pairs'
    print 'name_pref.pickle is a list of (team_name, team_name_prefix) tuples'
    pk.dump(city_name_Dict, open('city_name.pickle', 'wb'))
    pk.dump(name_pref_Tuples, open('name_pref.pickle', 'wb'))

if __name__ == '__main__':
    Get_All_Teams()

