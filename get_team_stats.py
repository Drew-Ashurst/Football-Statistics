import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

offense_stat_list = ['passing', 'rushing', 'receiving', 'scoring', 'downs']
defense_stat_list = ['passing', 'rushing', 'receiving', 'scoring', 'tackles', 'downs', 'fumbles', 'interceptions']
st_stat_list = ['field-goals', 'scoring', 'kickoffs', 'kickoff-returns', 'punting', 'punt-returns']

offensive_urls = {i: f'https://www.nfl.com/stats/team-stats/offense/{i}/2024/reg/all' for i in offense_stat_list}
defensive_urls = {i: f'https://www.nfl.com/stats/team-stats/defense/{i}/2024/reg/all' for i in defense_stat_list}
st_urls = {i: f'https://www.nfl.com/stats/team-stats/special-teams/{i}/2024/reg/all' for i in st_stat_list}

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('headless')
chrome_options.add_argument('window-size=1920x1080')
chrome_options.add_argument("disable-gpu")
chrome_options.add_experimental_option("prefs", {"profile.default_content_setting_values.cookies": 2})
driver = webdriver.Chrome(chrome_options)

def next_available(driver):
    try:
        driver.find_element(By.XPATH, '/html/body/div[3]/main/section[3]/div/div/div/footer/div/div/a')
        return True
    except:
        return False

def get_data(url_key, dict, side):
    url = dict[url_key]
    driver.get(url)
    full_df = pd.read_html(url)[0]  
    while next_available(driver):
        driver.find_element(By.XPATH, '/html/body/div[3]/main/section[3]/div/div/div/footer/div/div/a').click()
        temp_df = pd.read_html(driver.current_url)
        temp_df = pd.DataFrame(temp_df[0])

        full_df = pd.concat([full_df, temp_df])

    full_df.to_csv(f'team_stats/{side}/{side}_{url_key}_output.csv', index=False)

for i in offensive_urls.keys():
        print(f'Offensive {i} is in progress...')
        get_data(i, offensive_urls, 'offense')
for i in defensive_urls.keys():
        print(f'Defensive {i} is in progress...')
        get_data(i, defensive_urls, 'defense')
for i in st_urls.keys():
        print(f'Special Teams {i} is in progress')
        get_data(i, st_urls, 'special_teams')


