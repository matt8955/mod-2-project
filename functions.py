import sqlite3
import castle as c 
from datetime import datetime
import requests
import json
from matplotlib import pyplot
import seaborn as sns
from PIL import Image
import numpy as np


conn = sqlite3.connect('database.sqlite')

def fetched_query(query):
    '''creates takes in a query (str) then makes a cursor
        and executes a query'''
    c = conn.cursor()
    return c.execute(query).fetchall()

def all_teams(season):
    foo = fetched_query(f"select distinct(HomeTeam) from Matches where season='{season}'")
    return [team[0] for team in foo]

class team():
    def __init__(self, team_name, season):
        self.team = team_name
        self.season = season
        
    def get_unique_dates(self):
        '''returns a list of unique match days in a given season '''
        query = fetched_query(f"select distinct date from matches where season='{self.season}'")
        return [date[0] for date in query]

    def total_wins(self):
        '''takes in name of team  and season and spits out number of wins
           in a season '''
        away_wins = fetched_query("select count(season) from matches" 
                                  f" where (season = {self.season} and ftr = 'A' and AwayTeam = '{self.team}')")
        home_wins = fetched_query("select count(season) from matches" 
                                  f" where (season = {self.season} and ftr = 'H' and HomeTeam = '{self.team}')")
        return away_wins[0][0] + home_wins[0][0]

    def total_goals(self):
        '''given a team and season returns the total number of goals given
            team scored'''
        away_goals = fetched_query(f"select sum(FTAG) from matches where (season = {self.season} and AwayTeam = '{self.team}')")
        home_goals = fetched_query(f"select sum(FTHG) from matches where (season = {self.season} and HomeTeam = '{self.team}')")
        return away_goals[0][0] + home_goals[0][0]

    def get_matches(self):
        '''given a team and a season returns the date for each match'''
        return fetched_query(f"SELECT date, HomeTeam, AwayTeam, FTR from Matches where season='{self.season}' and (HomeTeam ='{self.team}' or AwayTeam='{self.team}')")


    def get_result(self, match):
        if self.team == match[1] and match[3] == 'H' or self.team == match[2] and match[3] == 'A':
            return 'win'
        elif self.team == match[2] and match[3] == 'H' or self.team == match[1] and match[3] == 'A':
            return 'loss'
        else:
            return 'draw'

    def get_barplot(self):
        '''creates a barplot of teams win losses and draws and converts it into
        a list of pixels'''
        matches = self.get_matches()
        results = []
        for match in matches:
            results.append(self.get_result(match))
        ax = sns.countplot(results)
        ax.figure.savefig('figure.png', dpi=30)
        img = Image.open('figure.png')
        img.load()
        data = np.asarray(img)
        return data.tolist()
    
    def win_percent_rain(self):
        '''takes in team name and returns their win percentage if it is raining'''
        with open('rain_dict.json', 'r') as q:
            rain = json.load(q)
        matches = self.get_matches() #get matches
        matches = [match for match in matches if rain[match[0]] == True] #keep only rainy days
        results = []
        for match in matches: 
            results.append(self.get_result(match))
        win_percent = results.count('win')/ len(results)
        return win_percent



class weather_helper():
    def __init__(self, latitude, longitude):
        self.url = 'https://api.darksky.net/forecast'
        self.key = c.api_key
        self.lat = latitude
        self.long = longitude
    
    def is_rain(self,dates):
        '''saves a dict of dates as keys and bools as value if it rained on the given date'''
        rain_dict = {}
        for date in dates:
            #format dates
            d = date.split('-')
            time = datetime(int(d[0]),int(d[1]),int(d[2]))
            time = time.timestamp()
            time = str(int(time))
            page = requests.get(f'{self.url}/{self.key}/{self.lat},{self.long},{self.time}')
            p = json.loads(page.text)
            if p['daily']['data'][0]['precipIntensity'] == 0:
                rain_dict[date] = False
            else:
                rain_dict[date] = True
        with open('rain_dict.json', 'w') as q:
            json.dump(q)
    