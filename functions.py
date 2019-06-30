import sqlite3
conn = sqlite3.connect('database.sqlite')

def fetched_query(query):
    '''creates takes in a query (str) then makes a cursor
        and executes a query'''
    c = conn.cursor()
    return c.execute(query).fetchall()

def team_list():
    '''returns a list of all teams in the database'''
    teams = []
    for row in fetched_query('select teamname from  unique_teams'):
        teams.append(row[0])
    return teams

def total_wins(team, season):
    '''takes in name of team  and season and spits out number of wins
       in a season '''
    
    away_wins = fetched_query("select count(season) from matches" 
                              f" where (season = {season} and ftr = 'A' and AwayTeam = '{team}')")
    home_wins = fetched_query("select count(season) from matches" 
                              f" where (season = {season} and ftr = 'H' and HomeTeam = '{team}')")
    return away_wins[0][0] + home_wins[0][0]

def all_teams(season):
    teams = team_list()
    foo = []
    for team in teams:
        try:
            foo.append([team, total_wins(team, season)])
        except:
            pass
    return [x[0] for x in foo if x[1] != 0]


def total_goals(team, season):
    '''given a team and season returns the total number of goals given
        team scored'''
    away_goals = fetched_query(f"select sum(FTAG) from matches where (season = {season} and AwayTeam = '{team}')")
    home_goals = fetched_query(f"select sum(FTHG) from matches where (season = {season} and HomeTeam = '{team}')")
    return away_goals[0][0] + home_goals[0][0]

def get_matches(team, season):
    '''given a team and a season returns the date for each match'''
    pass

def get_result(matchid):
    pass
def is_rain(date):
    pass