import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
import os
import pickle

epl_1920 = pd.read_csv("http://football-data.co.uk/mmz4281/1920/E0.csv")
epl_1920 = epl_1920[['HomeTeam','AwayTeam','FTHG','FTAG','FTR']]
epl_1920 = epl_1920.rename(columns={'FTHG': 'HomeGoals', 'FTAG': 'AwayGoals','FTR':'Result'})


goal_model_data = pd.concat([epl_1920[['HomeTeam','AwayTeam','HomeGoals']].assign(home=1).rename(
            columns={'HomeTeam':'team', 'AwayTeam':'opponent','HomeGoals':'goals'}),
           epl_1920[['AwayTeam','HomeTeam','AwayGoals']].assign(home=0).rename(
            columns={'AwayTeam':'team', 'HomeTeam':'opponent','AwayGoals':'goals'})])

poisson_model = smf.glm(formula="goals ~ home + team + opponent", data=goal_model_data, family=sm.families.Poisson()).fit()

dest = os.path.join('predictor', 'plk_objects')

if not os.path.exists(dest):
	os.makedirs(dest)

pickle.dump(poisson_model, open(os.path.join(dest, 'predictor.plk'), 'wb'), protocol=4)
