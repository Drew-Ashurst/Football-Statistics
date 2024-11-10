import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from config import config

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
    except Exception as e:
        return False

def get_data():
    offensive_urls = {i: f'https://www.nfl.com/stats/team-stats/offense/{i}/2024/reg/all' for i in config['offense_stat_list']}
    defensive_urls = {i: f'https://www.nfl.com/stats/team-stats/defense/{i}/2024/reg/all' for i in config['defense_stat_list']}
    st_urls = {i: f'https://www.nfl.com/stats/team-stats/special-teams/{i}/2024/reg/all' for i in config['special_teams_stat_list']}
    dicts = [(offensive_urls, 'offense'), (defensive_urls, 'defense'), (st_urls, 'special_teams')]
    
    for dict in dicts:
        side = dict[1]
        for url_key in dict[0].keys():
            url = dict[0][url_key]
            print(url)
            driver.get(url)
            full_df = pd.read_html(url)[0]  
            print(full_df)
            while next_available(driver):
                driver.find_element(By.XPATH, '/html/body/div[3]/main/section[3]/div/div/div/footer/div/div/a').click()
                temp_df = pd.read_html(driver.current_url)
                temp_df = pd.DataFrame(temp_df[0])

                full_df = pd.concat([full_df, temp_df])

            full_df.to_csv(f'{config['team_outputs']}/{side}/{side}_{url_key}_output.csv', index=False)
