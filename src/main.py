import bookmakers.winamax as winamax
import bookmakers.pmu as pmu
import arb

for competition in arb.competitions:
	winamax_games = winamax.get_games(competition)
	pmu_games = pmu.get_games(competition)
	print("-- Competition: {} --".format(competition))
	for game in winamax_games:
		print("{} - {}".format(game['team1'], game['team2']), end=" ")
		other = arb.get_game(game, pmu_games)
		print("({} - {})".format(other['team1'], other['team2']))
		arb.arb_games(game, other)
