from bs4 import BeautifulSoup
import requests

def get_page(competition):
	if (competition == "ligue1"):
		url = "https://paris-sportifs.pmu.fr/pari/competition/169/football/ligue-1-conforama"
	elif (competition == "liga"):
		url = "https://paris-sportifs.pmu.fr/pari/competition/322/football/la-liga"
	elif (competition == "bundesliga"):
		url = "https://paris-sportifs.pmu.fr/pari/competition/32/football/bundesliga"
	elif (competition == "premier-league"):
		url = "https://paris-sportifs.pmu.fr/pari/competition/13/football/premier-league"
	elif (competition == "serie-a"):
		url = "https://paris-sportifs.pmu.fr/pari/competition/308/football/italie-serie-a"
	elif (competition == "primeira"):
		url = "https://paris-sportifs.pmu.fr/pari/competition/273/football/primeira-liga"
	else:
		return None
	response = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"})
	html = BeautifulSoup(response.content, 'html.parser')
	return html

def get_games(competition="ligue1"):
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
