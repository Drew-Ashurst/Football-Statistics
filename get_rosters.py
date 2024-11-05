import pandas as pd

def get_rosters():
    with open('teams.txt', 'r') as f:
        lines= [i.strip() for i in f.readlines()]

    roster_df = pd.DataFrame()

    for line in lines:
        name = '-'.join(line.lower().split())
        temp_df = pd.DataFrame(pd.read_html(f'https://www.nfl.com/teams/{name}/roster')[0]['Player'])
        temp_df['Team'] = line
        roster_df = pd.concat([roster_df, temp_df])
        roster_df.to_csv('rosters.csv', index=False)

    return roster_df
roster_df = get_rosters()
