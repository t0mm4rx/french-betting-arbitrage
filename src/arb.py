from difflib import SequenceMatcher
import log

mismatch_pairs = [
	["MelbourneCity", "MelbourneVictory"],
	["MelbourneCityFC", "MelbourneVictoryFC"]
]

def str_similarity(a, b):
	return SequenceMatcher(None, a, b).ratio()

def get_game(game, others):
	if (len(others) == 0 or game == None):
		return None
	m = 0
	m_obj = None
	for other in others:
		sim = str_similarity(game['team1'], other['team1']) + str_similarity(game['team2'], other['team2'])
		if (sim > m):
			m = sim
			m_obj = other
	if (str_similarity(game['team1'], m_obj['team1']) < 0.81):
		return None
	if (str_similarity(game['team2'], m_obj['team2']) < 0.81):
		return None
	for mismatch in mismatch_pairs:
		if ([game['team1'], m_obj['team1']] == mismatch or [m_obj['team1'], game['team1']] == mismatch):
			return None
		if ([game['team2'], m_obj['team2']] == mismatch or [m_obj['team2'], game['team2']] == mismatch):
			return None
	return m_obj

def arb3(a, n, b):
	return (1 - (1/a + 1/n + 1/b)) * 100

def arb2(a, b):
	return (1 - (1/a + 1/b)) * 100

def dec_to_base(num, base):
	base_num = ""
	while (num > 0):
		dig = int(num % base)
		if (dig < 10):
			base_num += str(dig)
		else:
			base_num += chr(ord('A')+dig-10)
		num //= base
	base_num = base_num[::-1]
	return base_num

def arb_football(games):
	nb_bookmakers = len(games)
	combinations = nb_bookmakers ** 3
	log.log("-- Arbitrage on: ")
	for game in games:
		log.log("{:10}: {} - {} @{}/{}/{}".format(game, games[game]['team1'], games[game]['team2'], games[game]['odds'][0], games[game]['odds'][1], games[game]['odds'][2]))
	log.log("{} combinations possible --".format(combinations))
	for i in range(combinations):
		combination = str(dec_to_base(i, nb_bookmakers)).zfill(3)
		b1 = list(games.keys())[int(combination[0])]
		b2 = list(games.keys())[int(combination[1])]
		b3 = list(games.keys())[int(combination[2])]
		profit = arb3(
				games[b1]['odds'][0],
				games[b2]['odds'][1],
				games[b3]['odds'][2],
		)
		if (profit > 0):
			log.log("FOUND!!!!")
			stakes = get_stakes3(
				games[b1]['odds'][0],
				games[b2]['odds'][1],
				games[b3]['odds'][2],
				10)
			log.discord("Abritrage found for **{}**-**{}** with **{}/{}/{}** with odds {}/{}/{}: {:.2f}%".format(
				games[b1]['team1'],
				games[b1]['team2'],
				b1,
				b2,
				b3,
				games[b1]['odds'][0],
				games[b2]['odds'][1],
				games[b3]['odds'][2],
				profit
			))
			log.discord("> Stakes: **{}**@{} on {} for A, **{}**@{} on {} for N, **{}**@{} on {} for B".format(
				stakes['rounded'][0],
				games[b1]['odds'][0],
				b1,
				stakes['rounded'][1],
				games[b2]['odds'][1],
				b2,
				stakes['rounded'][2],
				games[b3]['odds'][2],
				b3,
			))
		log.log("{}: ({:10}/{:10}/{:10}) {:.2f}%".format(
			" ".join(combination.split()),
			b1,
			b2,
			b3,
			profit
		))

def arb_basketball(games):
	nb_bookmakers = len(games)
	combinations = nb_bookmakers ** 2
	log.log("-- Arbitrage on: ")
	for game in games:
		log.log("{:10}: {} - {} @{}/{}".format(game, games[game]['team1'], games[game]['team2'], games[game]['odds'][0], games[game]['odds'][1]))
	log.log("{} combinations possible --".format(combinations))
	for i in range(combinations):
		combination = str(dec_to_base(i, nb_bookmakers)).zfill(2)
		b1 = list(games.keys())[int(combination[0])]
		b2 = list(games.keys())[int(combination[1])]
		profit = arb2(
				games[b1]['odds'][0],
				games[b2]['odds'][1],
		)
		if (profit > 0):
			log.log("FOUND!!!!")
			stakes = get_stakes2(
				games[b1]['odds'][0],
				games[b2]['odds'][1],
				10)
			log.discord("Abritrage found for **{}**-**{}** with **{}/{}** with odds {}/{}: {:.2f}%".format(
				games[b1]['team1'],
				games[b1]['team2'],
				b1,
				b2,
				games[b1]['odds'][0],
				games[b2]['odds'][1],
				profit
			))
			log.discord("> Stakes: **{}**@{} on {} for A, **{}**@{} on {} for B".format(
				stakes['rounded'][0],
				games[b1]['odds'][0],
				b1,
				stakes['rounded'][1],
				games[b2]['odds'][1],
				b2
			))
		log.log("{}: ({:10}/{:10}) {:.2f}%".format(
			" ".join(combination.split()),
			b1,
			b2,
			profit
		))

def get_stakes3(a, n, b, investment):
	amount = arb3(a, n, b)
	tmp = (100 - amount) / 100
	return {
		'raw': (
			investment / (tmp * a),
			investment / (tmp * n),
			investment / (tmp * b)
		),
		'rounded': (
			round(investment / (tmp * a) * 10) / 10,
			round(investment / (tmp * n) * 10) / 10,
			round(investment / (tmp * b) * 10) / 10
		)
	}

def get_stakes2(a, b, investment):
	amount = arb2(a, b)
	tmp = (100 - amount) / 100
	return {
		'raw': (
			investment / (tmp * a),
			investment / (tmp * b)
		),
		'rounded': (
			round(investment / (tmp * a) * 10) / 10,
			round(investment / (tmp * b) * 10) / 10
		)
	}