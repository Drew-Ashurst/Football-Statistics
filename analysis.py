import pandas as pd
from config import config

class Analysis:
    def __init__(self):
        self.offensive_data = self.create_team_stats_dfs('offense')
        self.defensive_data = self.create_team_stats_dfs('defense')
        self.st_data = self.create_team_stats_dfs('special_teams')

    def create_team_stats_dfs(self, side):
        stats = config[f'{side}_stat_list']
        data = {}
        for stat in stats:
            data[stat] = pd.read_csv(f'{config['team_outputs']}/{side}/{side}_{stat}_output.csv')

        return data
    
    def get_max_stat(self, df, stat):
        print(df[stat].idxmax())
        return df.loc[df[stat].idxmax()]
    
    def team_order_stat(self, df, stat):
        return df.sort_values(by=[stat])
    
