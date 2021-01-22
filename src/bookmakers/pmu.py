from bs4 import BeautifulSoup
import requests

competition_urls = {
	'football':
	{
		"ligue1": "https://paris-sportifs.pmu.fr/pari/competition/169/football/ligue-1-conforama",
		"liga": "https://paris-sportifs.pmu.fr/pari/competition/322/football/la-liga",
		"bundesliga": "https://paris-sportifs.pmu.fr/pari/competition/32/football/bundesliga",
		"premier-league": "https://paris-sportifs.pmu.fr/pari/competition/13/football/premier-league",
		"serie-a": "https://paris-sportifs.pmu.fr/pari/competition/308/football/italie-serie-a",
		"primeira": "https://paris-sportifs.pmu.fr/pari/competition/273/football/primeira-liga",
		"serie-a-brasil": "https://paris-sportifs.pmu.fr/pari/competition/1779/football/s%C3%A9rie",
		"a-league": "https://paris-sportifs.pmu.fr/pari/competition/1812/football/australie-league",
		"bundesliga-austria": "https://paris-sportifs.pmu.fr/pari/competition/63/football/autriche-bundesliga",
		"division-1a": "https://paris-sportifs.pmu.fr/pari/competition/8124/football/division-1a",
		"super-lig": "https://paris-sportifs.pmu.fr/pari/competition/1529/football/turquie-super-ligue",
	},
	'basketball':
	{
		"nba": "https://paris-sportifs.pmu.fr/pari/competition/3502/basket-us/nba",
		"euroleague": "https://paris-sportifs.pmu.fr/pari/competition/1402/basket-euro/euroligue-h"
	}
}

def get_page(competition):
	if (competition["sport"] in competition_urls and competition["competition"] in competition_urls[competition["sport"]]):
		url = competition_urls[competition["sport"]][competition["competition"]]
	else:
		return None
	response = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"})
	html = BeautifulSoup(response.content, 'html.parser')
	return html

def get_games(competition):
	html = get_page(competition)
	games = []
	game_elements = html.select(".pmu-event-list-grid-highlights-formatter-row")
	for el in game_elements:
		game_name = el.select(".trow--event--name")[0].text
		game_name = "".join(game_name.split())
		team1, team2 = game_name.split("//")
		odds_el = el.select(".hierarchy-outcome-price")
		odds = []
		for el2 in odds_el:
			tmp = "".join(el2.text.split()).replace(",", ".")
			odds.append(float(tmp))
		games.append({
			'team1': team1,
			'team2': team2,
			'odds': odds
		})
	return games
