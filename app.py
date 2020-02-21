from flask import Flask, render_template, request
import os
import pickle
import numpy as np
from scipy.stats import poisson,skellam
import pandas as pd
from datetime import date
from update import update_model
from apiRequest import getFutureFixture
import statsmodels.api as sm
import statsmodels.formula.api as smf

app = Flask(__name__)

###############################
#### Loading predict model ####
###############################

#poisson_model = pickle.load(open(os.path.join('predictor/plk_objects/predictor.plk'), 'rb'))

epl_1920 = pd.read_csv("http://football-data.co.uk/mmz4281/1920/E0.csv")
epl_1920 = epl_1920[['HomeTeam','AwayTeam','FTHG','FTAG','FTR']]
epl_1920 = epl_1920.rename(columns={'FTHG': 'HomeGoals', 'FTAG': 'AwayGoals','FTR':'Result'})

goal_model_data = pd.concat([epl_1920[['HomeTeam','AwayTeam','HomeGoals']].assign(home=1).rename(
            columns={'HomeTeam':'team', 'AwayTeam':'opponent','HomeGoals':'goals'}),
           epl_1920[['AwayTeam','HomeTeam','AwayGoals']].assign(home=0).rename(
            columns={'AwayTeam':'team', 'HomeTeam':'opponent','AwayGoals':'goals'})])

poisson_model = smf.glm(formula="goals ~ home + team + opponent", data=goal_model_data, family=sm.families.Poisson()).fit()

def simulate_match(foot_model, homeTeam, awayTeam, max_goals=10):
    home_goals_avg = foot_model.predict(pd.DataFrame(data={'team': homeTeam, 
                                                            'opponent': awayTeam,'home':1},
                                                      index=[1])).values[0]
    away_goals_avg = foot_model.predict(pd.DataFrame(data={'team': awayTeam, 
                                                            'opponent': homeTeam,'home':0},
                                                      index=[1])).values[0]
    team_pred = [[poisson.pmf(i, team_avg) for i in range(0, max_goals+1)] for team_avg in [home_goals_avg, away_goals_avg]]
    return(np.outer(np.array(team_pred[0]), np.array(team_pred[1])))


future_fixtures = getFutureFixture()

# for matching model's team name
def changeClubName(matches):

    for match in matches:
        home = match[1]
        away = match[2]

        if match[1] == 'Manchester City':
            match[1] = 'Man City'
        elif match[1] == 'Manchester United':
            match[1] = 'Man United'
        elif match[1] == 'Sheffield Utd':
            match[1] = 'Sheffield United'

        if match[2] == 'Manchester City':
            match[2] = 'Man City'
        elif match[2] == 'Manchester United':
            match[2] = 'Man United'
        elif match[2] == 'Sheffield Utd':
            match[2] = 'Sheffield United'
            
    return matches

upcoming_fixtures = changeClubName(future_fixtures)
print(upcoming_fixtures)



###############################
####  	Flask 			   ####
###############################
@app.route("/")
def index():
    data = []

    for index in upcoming_fixtures:
        homeTeam = index[1]
        awayTeam = index[2]
        result = simulate_match(poisson_model, homeTeam, awayTeam, max_goals=10)

        date = index[0].split('T')[0]
        time = index[0].split('T')[1]

        home_prop = np.round(np.sum(np.tril(result,-1))*100)
        draw_prop = np.round(np.sum(np.diag(result))*100)
        away_prop = np.round(np.sum(np.triu(result,1))*100)
        game = {
            'date': date,
            'time': time,
            'homeProp':home_prop,
            'drawProp':draw_prop,
            'awayProp':away_prop,
            'homeTeam':homeTeam,
            'awayTeam':awayTeam,
            'homeTeamLogo':index[3],
            'awayTeamLogo':index[4]
        }
        data.append(game)

    print(data)
    return render_template("index.html", data = data)


if __name__ == "__main__":
	app.run(debug=True)
