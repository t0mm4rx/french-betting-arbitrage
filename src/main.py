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
import traceback

# print(ps3838.get_games({'competition': 'nba', 'sport': 'basketball'}))
# exit(0)
log.init()

progress = 0
for competition in config.competitions:
	progress += 1
	bookmakers = {}
	try:
		bookmakers['winamax'] = winamax.get_games(competition)
		log.log("winamax: " + str(bookmakers['winamax']))
	except:
		log.log("Cannot crawl winamax: " + traceback.format_exc())
	try:
		bookmakers['pmu'] = pmu.get_games(competition)
		log.log("pmu: " + str(bookmakers['pmu']))
	except:
		log.log("Cannot crawl pmu: " + traceback.format_exc())
	try:
		bookmakers['betclic'] = betclic.get_games(competition)
		log.log("betclic: " + str(bookmakers['betclic']))
	except:
		log.log("Cannot crawl betclic: " + traceback.format_exc())
	try:
		bookmakers['zebet'] = zebet.get_games(competition)
		log.log("zebet: " + str(bookmakers['zebet']))
	except:
		log.log("Cannot crawl zebet: " + traceback.format_exc())
	try:
		bookmakers['netbet'] = netbet.get_games(competition)
		log.log("netbet: " + str(bookmakers['netbet']))
	except:
		log.log("Cannot crawl netbet: " + traceback.format_exc())
	try:
		bookmakers['ps3838'] = ps3838.get_games(competition)
		log.log("ps3838: " + str(bookmakers['ps3838']))
	except:
		log.log("Cannot crawl ps3838: " + traceback.format_exc())
	log.log("-- Competition: {} --".format(competition))
	for game in bookmakers['winamax']:
		games = {}
		for bookmaker in bookmakers:
			try:
				g = arb.get_game(game, bookmakers[bookmaker])
				if (g):
					games[bookmaker] = g
			except:
				log.log("Error while retrieving games: {}".format(traceback.format_exc()))
		if (competition["sport"] == "football"):
			arb.arb_football(games)
		if (competition["sport"] == "basketball"):
			arb.arb_basketball(games)
	print("Progess: {:.2f}%".format(progress / len(config.competitions) * 100))