# coding: utf-8
import pandas as pd
import numpy as np
import pickle as pk
# import matplotlib.pyplot as plt
import sys
from NBA_GET_GAMES import *
from NBA_GET_TEAMS import *

def rank_by_improvement(year):
    data_path = '../data/'
    try:
        games_df = pd.read_csv(data_path + 'Games_' + str(year) + '.csv')
    except IOError:
        print 'Games for str(year) ' + str(year) + ' not exist, fetching data...'
        Get_All_Games(year)
        games_df = pd.read_csv(data_path + 'Games_' + str(year) + '.csv')

    try:
        teams = pk.load(open(data_path + 'name_pref.pickle'))
    except IOError:
        Get_All_Teams()
        teams = pk.load(open(data_path + 'name_pref.pickle'))

    improv_Dict = {}
    for name, pref in teams:
        improv_Dict[name] = {'W':0, 'Pos':[]}

    improv_df = pd.DataFrame(improv_Dict).T

    for idx, row in games_df.iterrows():
        home_team = row['home_team']
        visit_team = row['visit_team']
        home_score = int(row['home_score'].split()[0]) # possible 'OT'
        visit_score = int(row['visit_score'].split()[0]) 
        if home_score > visit_score:
            improv_df.ix[home_team]['W'] += 1
        else:
            improv_df.ix[visit_team]['W'] += 1
        cur_rank = improv_df['W'].rank(method='min', ascending=False)
        i = 0
        for pos in improv_df['Pos'].values:
            pos.append(cur_rank[i])
            i += 1

    team_name = []
    improvement = []
    for idx, row in improv_df.iterrows():
        team_name.append(idx)
        pos = row['Pos']
        worstPosInd = np.argmax(pos)
    #     later_pos = pos[worstPosInd:]
    #     bestPosInd = np.argmin(later_pos)
    #     improvement.append(pos[worstPosInd] - later_pos[bestPosInd])
        improvement.append(pos[worstPosInd] - pos[-1])

    team_improv = pd.Series(improvement, index=team_name)

    sorted_improv = team_improv.sort_values(ascending=False)
    print 'Output teams ranked by improvement to csv file...'
    pd.Series(data = sorted_improv.index.values).to_csv(data_path + 'Rank_Improve_' + str(year) +'.csv')
    # name = 'San Antonio Spurs'
    # data = improv_df.ix[name]['Pos']
    # plt.plot(np.array(worriers))
    # plt.xlim(0, len(data))
    # plt.title(name + ' ' + 'Rank Changes')
    # plt.show()

if __name__ == '__main__':
    year = int(sys.argv[1])
    rank_by_improvement(year)




