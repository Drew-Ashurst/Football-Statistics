import pandas as pd

print(pd.read_html(r'https://www.nfl.com/players/active/all?query=tyreek%20hill')[0]['Current Team'].values[0])
