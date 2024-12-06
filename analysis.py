import pandas as pd
from config import config

class Analysis:
    def __init__(self):
        self.offensive_data = self.get_offensive_stats()
        self.defensive_data = self.get_defensive_stats()
        self.st_data = self.get_special_teams_stats()
    
    def get_offensive_stats(self):
        offensive_stats = config['offense_stat_list']
        data = {}
        for stat in offensive_stats:
            data[stat] = pd.read_csv(f'{config['team_outputs']}/offense/offense_{stat}_output.csv')
           
        return data
    
    def get_defensive_stats(self):
        defensive_stats = config['defense_stat_list']
        data = {}
        for stat in defensive_stats:
            data[stat] = pd.read_csv(f'{config['team_outputs']}/defense/defense_{stat}_output.csv')
        return data
    def get_special_teams_stats(self):
        st_stats = config['special_teams_stat_list']
        data = {}
        for stat in st_stats:
            data[stat] = pd.read_csv(f'{config['team_outputs']}/special_teams/special_teams_{stat}_output.csv')
        return data