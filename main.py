import winamax
import pmu
import arb

winamax_games = winamax.get_games()
pmu_games = pmu.get_games()

for game in winamax_games:
	print("{} - {}".format(game['team1'], game['team2']))
	other = arb.get_game(game, pmu_games)
	arb.arb_games(game, other)