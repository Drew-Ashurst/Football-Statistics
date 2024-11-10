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

rosters = pd.read_csv(config['roster'])

def next_available(driver):
    try:
        driver.find_element(By.XPATH, '/html/body/div[3]/main/section[3]/div/div/div/footer/div/div/a')
        return True
    except:
        return False

def get_team_names(row):
    try:
        return rosters.loc[rosters['Player'] == row['Player'], ['Team']].values[0][0]
    except:
        return None
    
def get_data():
    for url_key in config['indv_urls'].keys():
        url = config['indv_urls'][url_key]
        driver.get(url)
        full_df = pd.read_html(url)[0]  
        while next_available(driver):
            try:
                driver.find_element(By.XPATH, '/html/body/div[3]/main/section[3]/div/div/div/footer/div/div/a').click()
                temp_df = pd.read_html(driver.current_url)
                temp_df = pd.DataFrame(temp_df[0])
                full_df = pd.concat([full_df, temp_df])
            except:
                continue

        full_df['Team'] = full_df.apply(get_team_names, axis=1)
        cols = list(full_df)
        cols.insert(1, cols.pop(cols.index('Team')))
        full_df = full_df.loc[:, cols]
        full_df.to_csv(f'{config['individual_outputs']}/{url_key}_output.csv', index=False)
