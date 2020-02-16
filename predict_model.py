from __future__ import division
import pandas as pd
import numpy as np
import scipy.stats as scipy
import matplotlib.pyplot as plt
import requests #download from football data
import io 
import seaborn as sns
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score
# %matplotlib inline

def model():
    url = "http://football-data.co.uk/mmz4281/1920/E0.csv"

    testfile = requests.get(url).content
    df=pd.read_csv(io.StringIO(testfile.decode('utf-8')))
    df.to_csv("E0_1920.csv")

    df = pd.read_csv("E0_1920.csv")

    res_16 = df.iloc[:,:23]
    res_16 = res_16.drop(['Div','Date'],axis=1)
    # res_16.head()

    feature_table = df.iloc[:,:23]
    feature_table.head()

    #Team, Home Goals Score, Away Goals Score, Attack Strength, Home Goals Conceded, Away Goals Conceded, Defensive Strength
    table_16 = pd.DataFrame(columns=('Team','HGS','AGS','HAS','AAS','HGC','AGC','HDS','ADS',))

    team = res_16.HomeTeam.unique()
    avg_home_scored_16 = res_16.FTHG.sum()*1.0 / res_16.shape[0]
    avg_away_scored_16 = res_16.FTAG.sum()*1.0 / res_16.shape[0]
    avg_home_conceded_16 = avg_away_scored_16
    avg_away_conceded_16 = avg_home_scored_16
    print("Average number of goals at home",avg_home_scored_16)
    print("Average number of goals away", avg_away_scored_16)
    print("Average number of goals conceded at home",avg_home_conceded_16)
    print("Average number of goals conceded away",avg_away_conceded_16)

    res_home = res_16.groupby('HomeTeam')
    res_away = res_16.groupby('AwayTeam')

    table_16.Team = team
    table_16.HGS = res_home.FTHG.sum().values
    table_16.HGC = res_home.FTAG.sum().values
    table_16.AGS = res_away.FTAG.sum().values
    table_16.AGC = res_away.FTHG.sum().values

    num_games = res_16.shape[0]/20

    table_16.HAS = (table_16.HGS / num_games) / avg_home_scored_16
    table_16.AAS = (table_16.AGS / num_games) / avg_away_scored_16
    table_16.HDS = (table_16.HGC / num_games) / avg_home_conceded_16
    table_16.ADS = (table_16.AGC / num_games) / avg_away_conceded_16

    return feature_table

def summary ():

    url = "http://football-data.co.uk/mmz4281/1920/E0.csv"

    testfile = requests.get(url).content
    df=pd.read_csv(io.StringIO(testfile.decode('utf-8')))
    df.to_csv("E0_1920.csv")

    df = pd.read_csv("E0_1920.csv")

    res_16 = df.iloc[:,:23]
    res_16 = res_16.drop(['Div','Date'],axis=1)
    # res_16.head()

    feature_table = df.iloc[:,:23]
    feature_table.head()

    #Team, Home Goals Score, Away Goals Score, Attack Strength, Home Goals Conceded, Away Goals Conceded, Defensive Strength
    table_16 = pd.DataFrame(columns=('Team','HGS','AGS','HAS','AAS','HGC','AGC','HDS','ADS',))

    team = res_16.HomeTeam.unique()
    avg_home_scored_16 = res_16.FTHG.sum()*1.0 / res_16.shape[0]
    avg_away_scored_16 = res_16.FTAG.sum()*1.0 / res_16.shape[0]
    avg_home_conceded_16 = avg_away_scored_16
    avg_away_conceded_16 = avg_home_scored_16
    print("Average number of goals at home",avg_home_scored_16)
    print("Average number of goals away", avg_away_scored_16)
    print("Average number of goals conceded at home",avg_home_conceded_16)
    print("Average number of goals conceded away",avg_away_conceded_16)

    res_home = res_16.groupby('HomeTeam')
    res_away = res_16.groupby('AwayTeam')

    table_16.Team = team
    table_16.HGS = res_home.FTHG.sum().values
    table_16.HGC = res_home.FTAG.sum().values
    table_16.AGS = res_away.FTAG.sum().values
    table_16.AGC = res_away.FTHG.sum().values

    num_games = res_16.shape[0]/20

    table_16.HAS = (table_16.HGS / num_games) / avg_home_scored_16
    table_16.AAS = (table_16.AGS / num_games) / avg_away_scored_16
    table_16.HDS = (table_16.HGC / num_games) / avg_home_conceded_16
    table_16.ADS = (table_16.AGC / num_games) / avg_away_conceded_16

    has_plot = sns.barplot(table_16.Team,table_16.HAS)
    for item in has_plot.get_xticklabels():
        item.set_rotation(90)

    feature_table = feature_table[['HomeTeam','AwayTeam','FTR','HST','AST']]
    f_HAS = []
    f_HDS = []
    f_AAS = []
    f_ADS = []

    for index,row in feature_table.iterrows():
        f_HAS.append(table_16[table_16['Team'] == row['HomeTeam']]['HAS'].values[0])
        f_HDS.append(table_16[table_16['Team'] == row['HomeTeam']]['HDS'].values[0])
        f_AAS.append(table_16[table_16['Team'] == row['AwayTeam']]['AAS'].values[0])
        f_ADS.append(table_16[table_16['Team'] == row['AwayTeam']]['ADS'].values[0])
    
    feature_table['HAS'] = f_HAS
    feature_table['HDS'] = f_HDS
    feature_table['AAS'] = f_AAS
    feature_table['ADS'] = f_ADS

    def transformResult(row):
    # '''Converts results (H,A or D) into numeric values'''
        if(row.FTR == 'H'):
            return 1
        elif(row.FTR == 'A'):
            return -1
        else:
            return 0

    feature_table["Result"] = feature_table.apply(lambda row: transformResult(row),axis=1)

    X_train = feature_table[['HAS','HDS','AAS','ADS']][:-10]
    y_train = feature_table['Result'][:-10]
    X_test = feature_table[['HAS','HDS','AAS','ADS']].tail(10)
    y_test = feature_table['Result'][:-10].tail(10)

    X_predict = pd.DataFrame(columns=('HAS','HDS','AAS','ADS'))

    HAS = table_16[table_16['Team'] == 'Norwich']['HAS'].values[0]
    HDS = table_16[table_16['Team'] == 'Norwich']['HDS'].values[0]
    AAS = table_16[table_16['Team'] == 'Liverpool']['AAS'].values[0]
    ADS = table_16[table_16['Team'] == 'Liverpool']['ADS'].values[0]

    X_predict = X_predict.append({
    'HAS': HAS,
    'HDS': HDS,
    'AAS': AAS,
    'ADS': ADS
    }, ignore_index=True)

    clf_logreg = LogisticRegression(C=1.0,solver='lbfgs',multi_class='ovr').fit(X_train,y_train)
    y_pred_logreg = clf_logreg.predict(X_test)
    y_pred_logreg

    return X_predict

