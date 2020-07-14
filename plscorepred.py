# -*- coding: utf-8 -*-
"""
Created on Sat Jul 11 18:02:07 2020

@author: GENIUS
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pickle

df = pd.read_csv('eplscores.csv')

columns_to_remove = ['Unnamed: 0', 'FTR',
       'HTGS', 'ATGS', 'HTGC', 'ATGC', 'HTP', 'ATP', 'HM1', 'HM2', 'HM3',
       'HM4', 'HM5', 'AM1', 'AM2', 'AM3', 'AM4', 'AM5', 'MW', 'HTFormPtsStr',
       'ATFormPtsStr', 'HTFormPts', 'ATFormPts', 'HTWinStreak3',
       'HTWinStreak5', 'HTLossStreak3', 'HTLossStreak5', 'ATWinStreak3',
       'ATWinStreak5', 'ATLossStreak3', 'ATLossStreak5', 'HTGD', 'ATGD',
       'DiffPts', 'DiffFormPts']

df.drop(labels=columns_to_remove, axis=1, inplace=True)

top6_teams = ['Chelsea', 'Liverpool', 'Arsenal',
                    'Tottenham', 'Man City', 'Man United']
df = df[(df['HomeTeam'].isin(top6_teams)) & (df['AwayTeam'].isin(top6_teams))]

from datetime import datetime

df['Date'] = df['Date'].apply(pd.to_datetime)

encoded_df = pd.get_dummies(data=df, columns=['HomeTeam', 'AwayTeam'])

encoded_df = encoded_df[['Date','HomeTeam_Arsenal', 'HomeTeam_Chelsea',
       'HomeTeam_Liverpool', 'HomeTeam_Man City', 'HomeTeam_Man United',
       'HomeTeam_Tottenham', 'AwayTeam_Arsenal', 'AwayTeam_Chelsea',
       'AwayTeam_Liverpool', 'AwayTeam_Man City', 'AwayTeam_Man United',
       'AwayTeam_Tottenham','FTHG', 'FTAG']]

final_df = encoded_df[encoded_df['Date'].dt.year >=2010]

X_train = final_df.drop(labels=['FTHG','FTAG'], axis=1)[final_df['Date'].dt.year <= 2016]
X_test = final_df.drop(labels=['FTHG','FTAG'], axis=1)[final_df['Date'].dt.year >= 2017]

y_train = final_df[final_df['Date'].dt.year <= 2016][['FTHG','FTAG']].values
y_test = final_df[final_df['Date'].dt.year >= 2017][['FTHG','FTAG']].values

X_train.drop(labels='Date', axis=True, inplace=True)
X_test.drop(labels='Date', axis=True, inplace=True)

from sklearn.ensemble import RandomForestRegressor
regressor = RandomForestRegressor(n_estimators = 10, random_state = 0)

regressor.fit(X_train,y_train)
y_pred = regressor.predict(X_test)


from sklearn import metrics


print('MAE:', metrics.mean_absolute_error(y_test, y_pred))
print('MSE:', metrics.mean_squared_error(y_test, y_pred))
print('RMSE:', np.sqrt(metrics.mean_squared_error(y_test, y_pred)))

filename = 'plscore.pkl'
pickle.dump(regressor, open(filename, 'wb'))

 