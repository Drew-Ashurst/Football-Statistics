import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

urls = {'passing': 'https://www.nfl.com/stats/player-stats/category/passing/2024/reg/all/passingyards/desc',
        'rushing': 'https://www.nfl.com/stats/player-stats/category/rushing/2024/reg/all/rushingyards/desc',
        'receiving': 'https://www.nfl.com/stats/player-stats/category/receiving/2024/reg/all/receivingreceptions/desc',
        'fumbles': 'https://www.nfl.com/stats/player-stats/category/fumbles/2024/reg/all/defensiveforcedfumble/desc',
        'tackles': 'https://www.nfl.com/stats/player-stats/category/tackles/2024/reg/all/defensivecombinetackles/desc',
        'interceptions': 'https://www.nfl.com/stats/player-stats/category/interceptions/2024/reg/all/defensiveinterceptions/desc',
        'field_goals': 'https://www.nfl.com/stats/player-stats/category/field-goals/2024/reg/all/kickingfgmade/desc',
        'kickoffs': 'https://www.nfl.com/stats/player-stats/category/kickoffs/2024/reg/all/kickofftotal/desc',
        'kickoff_returns': 'https://www.nfl.com/stats/player-stats/category/kickoff-returns/2024/reg/all/kickreturnsaverageyards/desc',
        'punting': 'https://www.nfl.com/stats/player-stats/category/punts/2024/reg/all/puntingaverageyards/desc',
        'punt_returns': 'https://www.nfl.com/stats/player-stats/category/punt-returns/2024/reg/all/puntreturnsaverageyards/desc'}

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

def get_data(url_key):
    url = urls[url_key]
    driver.get(url)
    full_df = pd.read_html(url)[0]  
    while next_available(driver):
        driver.find_element(By.XPATH, '/html/body/div[3]/main/section[3]/div/div/div/footer/div/div/a').click()
        temp_df = pd.read_html(driver.current_url)
        temp_df = pd.DataFrame(temp_df[0])

        full_df = pd.concat([full_df, temp_df])

    full_df.to_csv(f'individual_stats/{url_key}_output.csv', index=False)

for i in urls.keys():
    try:
        print(i.capitalize(), 'is in progress...')
        get_data(i)
    except:
        continue

