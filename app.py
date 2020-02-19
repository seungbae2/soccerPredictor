from flask import Flask, render_template, request
import os
import pickle
import numpy as np
from scipy.stats import poisson,skellam
import pandas as pd
from datetime import date
from update import update_model

app = Flask(__name__)

###############################
#### Loading predict model ####
###############################

predictor = pickle.load(open(os.path.join('predictor/plk_objects/predictor.plk'), 'rb'))

def simulate_match(foot_model, homeTeam, awayTeam, max_goals=10):
    home_goals_avg = foot_model.predict(pd.DataFrame(data={'team': homeTeam, 
                                                            'opponent': awayTeam,'home':1},
                                                      index=[1])).values[0]
    away_goals_avg = foot_model.predict(pd.DataFrame(data={'team': awayTeam, 
                                                            'opponent': homeTeam,'home':0},
                                                      index=[1])).values[0]
    team_pred = [[poisson.pmf(i, team_avg) for i in range(0, max_goals+1)] for team_avg in [home_goals_avg, away_goals_avg]]
    return(np.outer(np.array(team_pred[0]), np.array(team_pred[1])))



###############################
####  	Flask 			   ####
###############################
@app.route("/")
def index():
	fixture = pd.read_csv("static/data/epl-2019-GMTStandardTime.csv")

	today = date.today()
	fixture['Date'] = pd.to_datetime(fixture['Date'])
	future = fixture.loc[fixture['Date'] >= today]
	homeTeam = future['Home Team'].iloc[:10]
	awayTeam = future['Away Team'].iloc[:10]
	dates = future['Date'].iloc[:10]

	upcoming_ten_matches = pd.DataFrame(data = {'Date' : dates, 'HomeTeam': homeTeam, 'AwayTeam': awayTeam})

	matches = []
	home_prop = []
	draw_prop = []
	away_prop = []

	for index, row in upcoming_ten_matches.iterrows():
	    home = row['HomeTeam']
	    away = row['AwayTeam']

	    match = home + '_' + away
	    matches.append(match)
	    
	    result = simulate_match(predictor, home, away, max_goals=10)
	    home_prop.append(np.sum(np.tril(result, -1)))
	    draw_prop.append(np.sum(np.diag(result)))
	    away_prop.append(np.sum(np.triu(result, 1)))
	    
	result_pd = pd.DataFrame({'matches': matches, 'home': home_prop, 'draw': draw_prop, 'away': away_prop})


	return render_template("index.html", data = model, hometeams = hometeam, awayteams= awayteam)


if __name__ == "__main__":
	app.run(debug=True)