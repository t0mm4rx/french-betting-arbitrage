from difflib import SequenceMatcher

def str_similarity(a, b):
	return SequenceMatcher(None, a, b).ratio()

def get_game(game, others):
	m = 0
	m_obj = None
	for other in others:
		sim = str_similarity(game['team1'], other['team1']) + str_similarity(game['team2'], other['team2'])
		if (sim > m):
			m = sim
			m_obj = other
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
	print(arb(a['odds'][0], a['odds'][1], b['odds'][2]))
	print(arb(a['odds'][0], b['odds'][1], a['odds'][2]))
	print(arb(a['odds'][0], b['odds'][1], b['odds'][2]))
	print(arb(b['odds'][0], a['odds'][1], a['odds'][2]))
	print(arb(b['odds'][0], a['odds'][1], b['odds'][2]))
	print(arb(b['odds'][0], b['odds'][1], a['odds'][2]))
