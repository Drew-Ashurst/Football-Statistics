from selenium import webdriver
import time
from bs4 import BeautifulSoup
import pandas as pd
from config import config

with open('teams.txt', 'r') as f:
    team_list = [i.strip() for i in f.readlines()]

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('headless')
chrome_options.add_argument('window-size=1920x1080')
chrome_options.add_argument("disable-gpu")
driver = webdriver.Chrome(chrome_options)

def get_week_outcomes(current_week):
    output = pd.DataFrame()
    for week in range(1, current_week):
        data = []
        
        url= f"https://www.nfl.com/scores/2024/reg{week}"
        driver.get(url)

        time.sleep(5)
        content = driver.page_source.encode('utf-8').strip()
        soup = BeautifulSoup(content,"html.parser")
        teams = soup.find_all('div', {'class': ['css-text-146c3p1 r-color-1khnkhu r-fontFamily-1fdbu1n r-fontSize-ubezar']})
        scores = soup.find_all('div', {'class': ['css-text-146c3p1 r-fontFamily-1ujtvat r-fontSize-ubezar r-marginLeft-1jkjb r-textAlign-q4m81j r-width-lrsllp r-color-zyhucb', 'css-text-146c3p1 r-fontFamily-1ujtvat r-fontSize-ubezar r-marginLeft-1jkjb r-textAlign-q4m81j r-width-lrsllp r-color-1khnkhu']})

        teams = [i.text for i in teams]
        for i in range(len(teams)):
            for x in team_list:
                if teams[i] in x:
                    teams[i] = x
                    
        scores = [int(i.text) for i in scores]
        matchups = [[teams[i], teams[i+1]] for i in range(0, len(teams), 2)]
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
        output = pd.concat([output, df])
    
    return output

    
current_week = 10   
out = get_week_outcomes(current_week)
out.to_csv(config['game_outcomes'], index=False)