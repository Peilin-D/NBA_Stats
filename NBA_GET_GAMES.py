# coding: utf-8
import urllib
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, date
import sys
import pickle as pk
from NBA_GET_TEAM import *

def Get_All_Games(year):

    # see if the data already exists
    try:
        games_df = pd.read_csv('Games_' + str(year) + '.csv')
        print 'Data already exists'
        return
    except IOError:
        pass

    # get the teams
    try:
        city_name_Dict = pk.load(open('city_name.pickle'))
        name_pref_Tuples = pk.load(open('name_pref.pickle'))
    except IOError:
        Get_All_Teams()
        city_name_Dict = pk.load(open('city_name.pickle'))
        name_pref_Tuples = pk.load(open('name_pref.pickle'))

    # for regular season
    BASE_URL = 'http://espn.go.com/nba/team/schedule/_/name/%s/year/%s/seasontype/2'

    if year < 2002:
        raise ValueError('Cannot access data before 2002')
    if year >= int(date.today().year):
        raise ValueError('Data not available yet')

    home_team = []
    visit_team = []
    home_score = []
    visit_score = []
    dates = []
    match_id = []

    for team, pref in name_pref_Tuples:
        url = BASE_URL % (pref, str(year + 1))
        next_year = year
        html = urllib.urlopen(url).read()
        soup = BeautifulSoup(html, 'lxml')
        tables = soup.find_all('tr')[1:]
        for table in tables:
            if table['class'][0] == 'colhead':
                if table.td.text == 'JANUARY':
                    next_year = year + 1
                continue
            try:
                info = table.find_all('td')
                _d = datetime.strptime(str(next_year) + ', ' + info[0].text, '%Y, %a, %b %d')
                _home = True if info[1].find(class_ = 'game-status').text == 'vs' else False
                try:
                    _other_team = city_name_Dict[info[1].find(class_ = 'team-name').a.text]
                except Exception:
                    if info[1].find(class_ = 'team-name').a.text == 'NY Knicks':
                        _other_team = 'New York Knicks'
                    else:
                        _other_team = info[1].find(class_ = 'team-name').a.text
                    pass
                
                _score = info[2].find(class_ = 'score').a.text.split('-')
                _won = True if info[2].li.span.text == 'W' else False
                _id = info[2].a['href'].split('/')[-1]
                
                home_team.append(team if _home else _other_team)
                visit_team.append(_other_team if _home else team)
                dates.append(_d)
                match_id.append(_id)
                
                
                if _home:
                    if _won:
                        home_score.append(_score[0])
                        visit_score.append(_score[1])
                    else:
                        home_score.append(_score[1])
                        visit_score.append(_score[0])
                else:
                    if _won:
                        home_score.append(_score[1])
                        visit_score.append(_score[0])
                    else:
                        home_score.append(_score[0])
                        visit_score.append(_score[1])
            except Exception as e:
                print e
                pass


    game_data = {'date':dates, 
                 'match_id':match_id, 
                 'home_team':home_team, 
                 'visit_team':visit_team, 
                 'home_score':home_score, 
                 'visit_score':visit_score}

    games_df = pd.DataFrame(game_data, columns = ['match_id', 'date', 'home_team', 'visit_team', 'home_score', 'visit_score']).drop_duplicates('match_id')

    games_df2 = pd.DataFrame(data = games_df.values, index = range(len(games_df.index)), columns = ['match_id', 'date', 'home_team', 'visit_team', 'home_score', 'visit_score'])

    games_df2 = games_df2.sort_values('date')
    print 'Output all games csv file...'
    games_df2.to_csv('Games_' + str(year) + '.csv', index=False)


if __name__ == '__main__':
    year = int(sys.argv[1])
    Get_All_Games(year)

