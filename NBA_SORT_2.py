# coding: utf-8
import pandas as pd
import numpy as np
import pickle as pk
import matplotlib.pyplot as plt

games_df = pd.read_csv('Games.csv')

teams = pk.load(open('name_pref.pickle'))
improv_Dict = {}
for name, pref in teams:
    improv_Dict[name] = {'W':0, 'Pos':[]}

improv_df = pd.DataFrame(improv_Dict).T

date_df = games_df.sort_values('date')

for idx, row in date_df.iterrows():
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
pd.Series(data = sorted_improv.index.values).to_csv('Rank_Improve.csv')
# name = 'San Antonio Spurs'
# data = improv_df.ix[name]['Pos']
# plt.plot(np.array(worriers))
# plt.xlim(0, len(data))
# plt.title(name + ' ' + 'Rank Changes')
# plt.show()




