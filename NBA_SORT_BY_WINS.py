# coding: utf-8
import pandas as pd
import pickle as pk
import sys
from NBA_GET_GAMES import *
from NBA_GET_TEAMS import *

def rank_by_wins(year):

    try:
        games_df = pd.read_csv('Games_' + str(year) + '.csv')
    except IOError:
        print 'Games for year' + str(year) + 'not exist, fetching data...'
        Get_All_Games(year)
        games_df = pd.read_csv('Games_' + str(year) + '.csv')

    try:
        name_pref_Tuples = pk.load(open('name_pref.pickle'))
    except IOError:
        Get_All_Teams()
        name_pref_Tuples = pk.load(open('name_pref.pickle'))

    Team_Stat = {}
    for team, pref in name_pref_Tuples:
        Team_Stat[team] = {'home_win':0, 'visit_win':0, 'W':0, 'home_lose':0, 'visit_lose':0,\
                           'L':0, 'Avg_Score':0, 'Total_Score':0, 'Num_Contests':0}


    for idx, row in games_df.iterrows():
        home = row['home_team']
        visit = row['visit_team']
        h_score = int(row['home_score'].split()[0]) # possible 'OT'
        v_score = int(row['visit_score'].split()[0])
        Team_Stat[home]['Total_Score'] += h_score
        Team_Stat[visit]['Total_Score'] += v_score
        Team_Stat[home]['Num_Contests'] += 1
        Team_Stat[visit]['Num_Contests'] += 1
        if h_score > v_score:
            Team_Stat[home]['home_win'] += 1
            Team_Stat[home]['W'] += 1
            Team_Stat[visit]['visit_lose'] += 1
            Team_Stat[visit]['L'] += 1
        else:
            Team_Stat[visit]['visit_win'] += 1
            Team_Stat[visit]['W'] += 1
            Team_Stat[home]['home_lose'] += 1
            Team_Stat[home]['L'] += 1

    for t in Team_Stat:
        Team_Stat[t]['Avg_Score'] = Team_Stat[t]['Total_Score'] / Team_Stat[t]['Num_Contests']
    
    stat_df = pd.DataFrame(Team_Stat).T

    sorted_df = stat_df.sort_values(['W', 'visit_win', 'Avg_Score'], ascending=[False, False, False])
    sorted_df = sorted_df.drop(['Total_Score', 'L', 'home_lose', 'home_win', 'visit_lose', 'Num_Contests'], axis=1)
    sorted_df = sorted_df.reindex(columns=['W', 'visit_win', 'Avg_Score'])

    print 'Output team rank csv file...'
    sorted_df.to_csv('Team_Rank_' + str(year) + '.csv')

if __name__ == '__main__':
    year = int(sys.argv[1])
    rank_by_wins(year)


