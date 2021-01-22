from bs4 import BeautifulSoup
import requests

competition_urls = {
	'football': 
	{
		"ligue1": "https://www.netbet.fr/football/france/ligue-1-uber-eats",
		"liga": "https://www.netbet.fr/football/espagne/laliga",
		"bundesliga": "https://www.netbet.fr/football/allemagne/bundesliga",
		"premier-league": "https://www.netbet.fr/football/angleterre/premier-league",
		"serie-a": "https://www.netbet.fr/football/italie/coupe-d-italie",
		"primeira": "https://www.netbet.fr/football/portugal/primeira-liga",
		"serie-a-brasil": "https://www.netbet.fr/football/bresil/brasileirao",
		"a-league": "https://www.netbet.fr/football/australie/a-league",
		"bundesliga-austria": "https://www.netbet.fr/football/autriche/bundesliga",
		"division-1a": "https://www.netbet.fr/football/belgique/pro-league",
		"super-lig": "https://www.netbet.fr/football/turquie/super-lig",
	},
	'basketball':
	{
		"nba": "https://www.netbet.fr/basketball/etats-unis/nba",
		"euroleague": "https://www.netbet.fr/basketball/coupes-d-europe/euroligue",
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
	game_elements = html.select(".nb-event")
	for el in game_elements:
		names = el.select(".nb-match_actor")
		team1 = "".join(names[0].text.split())
		team2 = "".join(names[1].text.split())
		odd_els = el.select(".nb-odds_amount")
		odds = []
		for odd_el in odd_els[:3]:
			odds.append(float(odd_el.text.replace(",", ".")))
		games.append({
			'team1': team1,
			'team2': team2,
			'odds': odds
		})
	return games