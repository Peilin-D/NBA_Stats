#NBA Data Analysis

### 1. NBA_GET_TEAMS.py
Get all the team names from ESPN and store them in two files, the city_name.pickle and name_pref.pickle.
city_name.pickle is a dict with (city, team_name) pairs  
name_pref.pickle is a list of (team_name, team_name_prefix) tuples  
**Usage:** `python NBA_GET_TEAMS.py`

### 2. NBA_GET_GAMES.py
Get all the game results of the user input year (the year where the *regular* season begins).  
The result would be stored as .csv file.
The data is stored as:

| match_id  | date       | home_team      | visit_team         | home_score | visit_score |
|-----------|------------|----------------|--------------------|------------|-------------|
| 400827892 | 2015-10-28 | Boston Celtics | Philadelphia 76ers | 112        | 95          |
| 400827911 | 2015-10-30 | Boston Celtics | Toronto Raptors    | 103        | 113         |
**Usage:** `python NBA_GET_GAMES.py [year]`

### 3. NBA_SORT_BY_WINS.py
Rank the teams by their performance.  
Teams are sorted first by their number of wins (most significant), then by their number of visit wins, then by their average score per contest they played.  
Running this script would automatically run NBA_GET_TEAMS.py and NBA_GET_GAMES.py if the files are not there.  
**Usage:** `python NBA_SORT_BY_WINS.py [year]`

### 4. NBA_SORT_BY_IMPROV.py
Rank the teams by the improvement of their performance.
Running this script would automatically run NBA_GET_TEAMS.py and NBA_GET_GAMES.py if the files are not there.  
**Usage:** `python NBA_SORT_BY_IMPROV.py [year]`
