import bookmakers.winamax as winamax
import bookmakers.pmu as pmu
import bookmakers.betclic as betclic
import bookmakers.zebet as zebet
import bookmakers.netbet as netbet
import bookmakers.ps3838 as ps3838
import arb
import sys
import log
import config

# print(ps3838.get_games({'competition': 'nba', 'sport': 'basketball'}))
# exit(0)
log.init()

progress = 0
for competition in config.competitions:
	progress += 1
	# try:
	bookmakers = {
		'winamax': winamax.get_games(competition),
		'pmu': pmu.get_games(competition),
		'betlic': betclic.get_games(competition),
		'zebet': zebet.get_games(competition),
		'netbet': netbet.get_games(competition),
		'ps3838': ps3838.get_games(competition)
	}
	# except:
	# 	log.log("Error while fetching games: {}".format(sys.exc_info()[0]))
	# 	continue
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
		if (competition["sport"] == "football"):
			arb.arb_football(games)
		if (competition["sport"] == "basketball"):
			arb.arb_basketball(games)
	print("Progess: {:.2f}%".format(progress / len(config.competitions) * 100))