from difflib import SequenceMatcher
import log

competitions = [
	"ligue1",
	"liga",
	"bundesliga",
	"premier-league",
	"serie-a",
	"primeira",
	"serie-a-brasil",
	"a-league",
	"bundesliga-austria",
	"division-1a",
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
	if (str_similarity(game['team1'], m_obj['team1']) < 0.4):
		return None
	if (str_similarity(game['team2'], m_obj['team2']) < 0.4):
		return None
	return m_obj

def arb(a, n, b):
	return (1 - (1/a + 1/n + 1/b)) * 100

"""
a a b
a b a
a b b
b a a
b a b
b b a
"""
def arb_games(a, b):
	log.log("{:.2f}%".format(arb(a['odds'][0], a['odds'][1], b['odds'][2])))
	log.log("{:.2f}%".format(arb(a['odds'][0], b['odds'][1], a['odds'][2])))
	log.log("{:.2f}%".format(arb(a['odds'][0], b['odds'][1], b['odds'][2])))
	log.log("{:.2f}%".format(arb(b['odds'][0], a['odds'][1], a['odds'][2])))
	log.log("{:.2f}%".format(arb(b['odds'][0], a['odds'][1], b['odds'][2])))
	log.log("{:.2f}%".format(arb(b['odds'][0], b['odds'][1], a['odds'][2])))

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

def arb_bookmakers(games):
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
		profit = arb(
				games[b1]['odds'][0],
				games[b2]['odds'][1],
				games[b3]['odds'][2],
		)
		if (profit > 0):
			log.log("FOUND!!!!")
			log.discord("Abritrage found for {}-{} with {}/{}/{}: {:.2f}%".format(
				games[b1]['team1'],
				games[b1]['team2'],
				b1,
				b2,
				b3,
				profit
			))
		log.log("{}: ({:10}/{:10}/{:10}) {:.2f}%".format(
			" ".join(combination.split()),
			b1,
			b2,
			b3,
			profit
		))
