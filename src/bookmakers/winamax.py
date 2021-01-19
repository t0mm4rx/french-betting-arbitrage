import requests
import json

competition_ids = {
	"ligue1": 4,
	"liga": 36
}

def get_page(competition):
	if (competition == "ligue1"):
		url = "https://www.winamax.fr/paris-sportifs/sports/1/7/4"
	elif (competition == "liga"):
		url = "https://www.winamax.fr/paris-sportifs/sports/1/32/36"
	else:
		return None
	response = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"})
	html = response.text
	return html

def get_json(competition):
	html = get_page(competition)
	split1 = html.split("var PRELOADED_STATE = ")[1]
	split2 = split1.split(";</script>")[0]
	return json.loads(split2)

def get_games(competition="ligue1"):
	games = []
	json = get_json(competition)
	for game in json['matches']:
		if (json['matches'][game]['tournamentId'] != competition_ids[competition]):
			continue
		team1 = json['matches'][game]['competitor1Name']
		team2 = json['matches'][game]['competitor2Name']
		bet_id = json['matches'][game]['mainBetId']
		bet = json['bets'][str(bet_id)]['outcomes']
		if (len(bet) != 3):
			continue
		odds = [
			json['odds'][str(bet[0])],
			json['odds'][str(bet[1])],
			json['odds'][str(bet[2])],
		]
		games.append({
			'team1': team1,
			'team2': team2,
			'odds': odds
		})
	return games