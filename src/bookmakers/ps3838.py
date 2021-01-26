from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import re
import traceback

competition_urls = {
	'football':
	{
		"ligue1": {'url': "https://www.ps3838.com/fr/euro/sports/soccer/france", 'code': "2036"},
		"liga": {'url': "https://www.ps3838.com/fr/euro/sports/soccer/espagne", 'code': "2196"},
		"bundesliga": {'url': "https://www.ps3838.com/fr/euro/sports/soccer/allemagne", 'code': "1842"},
		"premier-league": {'url': "https://www.ps3838.com/fr/euro/sports/soccer/angleterre", 'code': "1980"},
		"serie-a": {'url': "https://www.ps3838.com/fr/euro/sports/soccer/italie", 'code': "2436"},
		"primeira": {'url': "https://www.ps3838.com/fr/euro/sports/soccer/portugal", 'code': "2386"},
		"serie-a-brasil": {'url': "https://www.ps3838.com/fr/euro/sports/soccer/br%C3%A9sil", 'code': "1834"},
		"a-league": {'url': "https://www.ps3838.com/fr/euro/sports/soccer/australia", 'code': "1766"},
		"bundesliga-austria": {'url': "https://www.ps3838.com/fr/euro/sports/soccer/autriche", 'code': "1792"},
		"division-1a": {'url': "https://www.ps3838.com/fr/euro/sports/soccer/belgique", 'code': "1817"},
		"super-lig": {'url': "https://www.ps3838.com/fr/euro/sports/soccer/turquie", 'code': "2592"},
	},
	'basketball':
	{
		"nba": {'url': "https://www.ps3838.com/fr/euro/sports/basketball/others", 'code': "487"},
		"euroleague": {'url': "https://www.ps3838.com/fr/euro/sports/basketball/europe", 'code': "382"}
	}
}

def get_page(competition):
	if (competition["sport"] in competition_urls and competition["competition"] in competition_urls[competition["sport"]]):
		url = competition_urls[competition["sport"]][competition["competition"]]
	else:
		return None
	options = Options()
	options.add_argument("--no-sandbox")
	options.headless = True
	driver = webdriver.Chrome("./chromedriver", chrome_options=options)
	driver.set_window_size(1920, 1080)
	driver.get(url['url'])
	driver.find_element_by_css_selector("[data-league=\"{}\"]".format(url['code'])).click()
	found = 0
	while (found >= 0):
		try:
			driver.find_element_by_css_selector(".OneXTwo_0")
			found = -1
		except:
			if (found >= 1000):
				driver.quit()
				return get_page(competition)
			found += 1
	return driver

def get_games(competition):
	games = []
	driver = get_page(competition)
	if (not driver):
		return None
	good = False
	# We get every date labels
	while not good:
		try:
			dates = driver.find_elements_by_css_selector(".dateMenutb td:not([data-date=\"null\"])")
			dates = [d.text for d in dates]
			good = True
		except:
			pass
	# We loop through each label, find the corresponding tab and click it
	for date in dates:
		c = float(date.split("(")[1].split(")")[0])
		if (not c):
			continue
		good = False
		# We click on the tab
		while not good:
			try:
				date_new = driver.find_element_by_link_text(date)
				date_new.click()
				# We wait for the page content to load
				found = False
				while not found:
					try:
						driver.find_element_by_css_selector(".OneXTwo_0")
						found = True
					except:
						pass
				# Once the page is loaded, we get the HTML and parses it with bs4
				games_page = parse_page(
						competition,
						BeautifulSoup(driver.execute_script("return document.documentElement.outerHTML;"), 'html.parser')
					)
				for game in games_page:
					games.append(game)
				good = True
			except:
				pass
	driver.quit()
	return games

def parse_page(competition, html):
	games = []
	if (not html):
		return None
	table = html.select(".OneXTwo_0")[0]
	game_els = table.select("tr")
	for game_el in game_els:
		teams = game_el.select(".team_name")
		team1 = "".join(teams[0].text.split()).replace("\u200e", "")
		team2 = "".join(teams[1].text.split()).replace("\u200e", "")
		team1 = handle_nba_names(team1, competition)
		team2 = handle_nba_names(team2, competition)
		odd_els = game_el.select(".o_right")
		odds = []
		for odd_el in odd_els:
			odds.append(float(odd_el.text))
		games.append({
			'team1': team1,
			'team2': team2,
			'odds': odds,
		})
	return games

def handle_nba_names(team, competition):
	if (competition['competition'] == "nba"):
		if ("d'" in team):
			splits = team.split("d'")
			if (len(splits) > 1):
				team = splits[1] + splits[0]
		if ("d’" in team):
			splits = team.split("d’")
			if (len(splits) > 1):
				team = splits[1] + splits[0]
		elif ("de" in team):
			splits = team.split("de")
			if (len(splits) > 1):
				team = splits[1] + splits[0]
	return team