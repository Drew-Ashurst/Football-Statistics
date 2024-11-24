from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import config
import pandas as pd
from bs4 import BeautifulSoup
import time


class Data:
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('headless')
        chrome_options.add_argument('window-size=1920x1080')
        chrome_options.add_argument("disable-gpu")
        chrome_options.add_experimental_option("prefs", {"profile.default_content_setting_values.cookies": 2})
        
        with open('teams.txt', 'r') as f:
            self.teams = [i.strip() for i in f.readlines()]
        
        self.driver = webdriver.Chrome(chrome_options)
        self.get_rosters()
        
    
    def get_next_page(self, df, xpath):
        try:
            self.driver.find_element(By.XPATH, xpath).click()
            df = pd.concat([df, pd.DataFrame(pd.read_html(self.driver.current_url)[0])])
            return df, True
        except Exception as e:
            print(e)
            return df, False
    
    def get_player_team(self, row):
        try:
            return self.rosters.loc[self.rosters['Player'] == row['Player'], ['Team']].values[0][0]
        except:
            return None

    def get_indv_data(self):
        keys = config['indv_urls']
        for url_key in keys.keys():
            url = keys[url_key]
            self.driver.get(url)
            indv_df = pd.read_html(url)[0]  
            while True:
                
                indv_df, state = self.get_next_page(indv_df, '/html/body/div[3]/main/section[3]/div/div/div/footer/div/div/a')
                if not state:
                    break
                
            indv_df['Team'] = indv_df.apply(self.get_player_team, axis=1)
            cols = list(indv_df)
            cols.insert(1, cols.pop(cols.index('Team')))
            indv_df = indv_df.loc[:, cols]
            indv_df.to_csv(f'{config['individual_outputs']}/{url_key}_output.csv', index=False)
    
    def get_rosters(self):

        roster_df = pd.DataFrame()

        for team in self.teams:
            name = '-'.join(team.lower().split())
            temp_df = pd.DataFrame(pd.read_html(f'https://www.nfl.com/teams/{name}/roster')[0]['Player'])
            temp_df['Team'] = team
            roster_df = pd.concat([roster_df, temp_df])
            roster_df.to_csv(config['roster'], index=False)

        self.rosters = pd.read_csv(config['roster'])
    
    def get_team_stats(self):
        offensive_urls = {i: f'https://www.nfl.com/stats/team-stats/offense/{i}/2024/reg/all' for i in config['offense_stat_list']}
        defensive_urls = {i: f'https://www.nfl.com/stats/team-stats/defense/{i}/2024/reg/all' for i in config['defense_stat_list']}
        st_urls = {i: f'https://www.nfl.com/stats/team-stats/special-teams/{i}/2024/reg/all' for i in config['special_teams_stat_list']}
        dicts = [(offensive_urls, 'offense'), (defensive_urls, 'defense'), (st_urls, 'special_teams')]
        for dict in dicts:
            side = dict[1]
            for url_key in dict[0].keys():
                url = dict[0][url_key]
                self.driver.get(url)
                team_df = pd.read_html(url)[0]  
                while True:
                    team_df, state = self.get_next_page(team_df, '/html/body/div[3]/main/section[3]/div/div/div/footer/div/div/a')
                    if not state:
                        break
                
                team_df.to_csv(f'{config['team_outputs']}/{side}/{side}_{url_key}_output.csv', index=False)
    
    def get_game_outcomes(self, current_week):
        outcomes_df = pd.DataFrame()
        
        chrome_options2 = webdriver.ChromeOptions()
        chrome_options2.add_argument('headless')
        chrome_options2.add_argument('window-size=1920x1080')
        chrome_options2.add_argument("disable-gpu")
        chrome_options2.add_experimental_option("prefs", {"profile.default_content_setting_values.cookies": 1})
        
        outcome_driver = webdriver.Chrome(chrome_options2)
        for week in range(1, current_week + 1):
            print(week)
            data = []
        
            url= f"https://www.nfl.com/scores/2024/reg{week}"
            outcome_driver.get(url)
            
            time.sleep(5)
            content = outcome_driver.page_source.encode('utf-8').strip()
            soup = BeautifulSoup(content,"html.parser")

            team_list = soup.find_all('div', {'class': ['css-text-146c3p1 r-color-1khnkhu r-fontFamily-1fdbu1n r-fontSize-ubezar']})
            scores = soup.find_all('div', {'class': ['css-text-146c3p1 r-fontFamily-1ujtvat r-fontSize-ubezar r-marginLeft-1jkjb r-textAlign-q4m81j r-width-lrsllp r-color-zyhucb', 'css-text-146c3p1 r-fontFamily-1ujtvat r-fontSize-ubezar r-marginLeft-1jkjb r-textAlign-q4m81j r-width-lrsllp r-color-1khnkhu']})

            team_list = [i.text for i in team_list]
            for i in range(len(team_list)):
                for x in self.teams:
                    if team_list[i] in x:
                        team_list[i] = x
                        
            scores = [int(i.text) for i in scores]
            matchups = [[team_list[i], team_list[i+1]] for i in range(0, len(team_list), 2)]
            matchup_scores = [[scores[i], scores[i+1]] for i in range(0, len(scores), 2)]
            
            for i in range(len(matchups)):
                data.append({'Team': matchups[i][0],
                            'Week': f'Week {week}',
                            'Outcome': 'Win' if matchup_scores[i][0] > matchup_scores[i][1] else 'Loss',
                            'Points Scored': matchup_scores[i][0],
                            'Opponent': matchups[i][1],
                            'Points Allowed': matchup_scores[i][1]
                            })
                data.append({'Team': matchups[i][1],
                            'Week': f'Week {week}',
                            'Outcome': 'Win' if matchup_scores[i][0] < matchup_scores[i][1] else 'Loss',
                            'Points Scored': matchup_scores[i][1],
                            'Opponent': matchups[i][0],
                            'Points Allowed': matchup_scores[i][0]
                            })
            df = pd.DataFrame(data)
            outcomes_df = pd.concat([outcomes_df, df])
        outcomes_df.to_csv(config['game_outcomes'], index=False)
        outcome_driver.quit()
