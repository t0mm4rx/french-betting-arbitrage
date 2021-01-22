import requests
import json

competition_urls = {
	'football':
	{
		"ligue1": "https://www.winamax.fr/paris-sportifs/sports/1/7/4",
		"liga": "https://www.winamax.fr/paris-sportifs/sports/1/32/36",
		"bundesliga": "https://www.winamax.fr/paris-sportifs/sports/1/30/42",
		"premier-league": "https://www.winamax.fr/paris-sportifs/sports/1/1/1",
		"serie-a": "https://www.winamax.fr/paris-sportifs/sports/1/31/33",
		"primeira": "https://www.winamax.fr/paris-sportifs/sports/1/44/52",
		"serie-a-brasil": "https://www.winamax.fr/paris-sportifs/sports/1/13/83",
		"a-league": "https://www.winamax.fr/paris-sportifs/sports/1/34/144",
		"bundesliga-austria": "https://www.winamax.fr/paris-sportifs/sports/1/17/29",
		"division-1a": "https://www.winamax.fr/paris-sportifs/sports/1/33/38",
		"super-lig": "https://www.winamax.fr/paris-sportifs/sports/1/46/62",
	},
	'basketball':
	{
		"nba": "https://www.winamax.fr/paris-sportifs/sports/2/800000076/177",
		"euroleague": "https://www.winamax.fr/paris-sportifs/sports/2/800000034/153",
	}
}

def get_page(competition):
	if (competition["sport"] in competition_urls and competition["competition"] in competition_urls[competition["sport"]]):
		url = competition_urls[competition["sport"]][competition["competition"]]
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

def get_id(competition):
	url = competition_urls[competition["sport"]][competition["competition"]]
	return int(url.split("/")[-1])

def get_games(competition):
	games = []
	json = get_json(competition)
	for game in json['matches']:
		if (json['matches'][game]['tournamentId'] != get_id(competition)):
			continue
		team1 = "".join(json['matches'][game]['competitor1Name'].split())
		team2 = "".join(json['matches'][game]['competitor2Name'].split())
		bet_id = json['matches'][game]['mainBetId']
		bet = json['bets'][str(bet_id)]['outcomes']
		if (competition["sport"] == "football" and len(bet) != 3):
			continue
		if (competition["competition"] == "basketball" and len(bet) != 2):
			continue
		if (competition["sport"] == "football"):
			odds = [
				json['odds'][str(bet[0])],
				json['odds'][str(bet[1])],
				json['odds'][str(bet[2])],
			]
		elif (competition["sport"] == "basketball"):
			odds = [
				json['odds'][str(bet[0])],
				json['odds'][str(bet[1])],
			]
		games.append({
			'team1': team1,
			'team2': team2,
			'odds': odds
		})
	return games