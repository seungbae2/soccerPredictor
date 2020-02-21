import requests

def getFutureFixture():

	url = "https://api-football-v1.p.rapidapi.com/v2/fixtures/league/524/next/10"

	querystring = {"timezone":"America/Los_Angeles"}

	headers = {
	    'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
	    'x-rapidapi-key': "65ff80534cmsh0d3a35298c91796p1dc48bjsna05653c2e9f4"
	    }

	response = requests.request("GET", url, headers=headers,params=querystring)
	data = response.json()

	fixtures = data['api']['fixtures']

	fixture_list = []

	for fixture in fixtures:
	    fixture_list.append([fixture['event_date'],fixture['homeTeam']['team_name'],fixture['awayTeam']['team_name'],fixture['homeTeam']['logo'],fixture['awayTeam']['logo']])

	return fixture_list