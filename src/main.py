import bookmakers.winamax as winamax
import bookmakers.pmu as pmu
import bookmakers.betclic as betclic
import arb

for competition in arb.competitions:
	bookmakers = {
		'winamax': winamax.get_games(competition),
		'pmu': pmu.get_games(competition),
		'betlic': betclic.get_games(competition)
	}
	print("-- Competition: {} --".format(competition))
	for game in bookmakers['winamax']:
		games = {}
		for bookmaker in bookmakers:
			games[bookmaker] = arb.get_game(game, bookmakers[bookmaker])
		arb.arb_bookmakers(games)


