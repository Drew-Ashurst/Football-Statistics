import data
import analysis


CURRENT_WEEK = 10

#d = data.Data()
#d.get_rosters()
#d.get_team_stats()
#d.get_indv_data()
#d.get_game_outcomes(10)

a = analysis.Analysis()

print(a.team_order_stat(a.offensive_data['passing'], "Pass Yds"))

