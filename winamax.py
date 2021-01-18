import requests
import json

def get_page():
	url = "https://www.winamax.fr/paris-sportifs/sports/1/7/4"
	response = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"})
	html = response.text
	return html

def get_json():
	html = get_page()
	split1 = html.split("var PRELOADED_STATE = ")[1]
	split2 = split1.split(";</script>")[0]
	return json.loads(split2)

def get_games():
	games = []
	json = get_json()
	for game in json['matches']:
		if (json['matches'][game]['sportId'] != 1 or json['matches'][game]['tournamentId'] != 4):
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