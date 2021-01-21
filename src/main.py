import bookmakers.winamax as winamax
import bookmakers.pmu as pmu
import bookmakers.betclic as betclic
import bookmakers.zebet as zebet
import bookmakers.netbet as netbet
import arb
import sys
import log

log.init()

progress = 0
for competition in arb.competitions:
	progress += 1
	print("Progess: {:.2f}%".format(progress / len(arb.competitions) * 100))
	try:
		bookmakers = {
			'winamax': winamax.get_games(competition),
			'pmu': pmu.get_games(competition),
			'betlic': betclic.get_games(competition),
			'zebet': zebet.get_games(competition),
			'netbet': netbet.get_games(competition)
		}
	except:
		log.log("Error while fetching games: {}".format(sys.exc_info()[0]))
		continue
	log.log("-- Competition: {} --".format(competition))
	for game in bookmakers['winamax']:
		games = {}
		for bookmaker in bookmakers:
			try:
				g = arb.get_game(game, bookmakers[bookmaker])
				if (g):
					games[bookmaker] = g
			except:
				log.log("Error while retrieving games: {}".format(sys.exc_info()[0]))
		arb.arb_bookmakers(games)