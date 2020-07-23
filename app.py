# -*- coding: utf-8 -*-
"""
Created on Mon Jul 13 17:38:36 2020

@author: GENIUS
"""

from flask import Flask, render_template, request
import pickle
import numpy as np


filename = 'plscore.pkl'
regressor = pickle.load(open(filename, 'rb'))

app = Flask(__name__)

@app.route('/')
def home():
	return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    temp_array = list()
    
    if request.method == 'POST':
        
        home_team = request.form['home-team']
        if home_team == 'Arsenal':
            temp_array = temp_array + [1,0,0,0,0,0]
        elif home_team == 'Chelsea':
            temp_array = temp_array + [0,1,0,0,0,0]
        elif home_team == 'Liverpool':
            temp_array = temp_array + [0,0,1,0,0,0]
        elif home_team == 'Man City':
            temp_array = temp_array + [0,0,0,1,0,0]
        elif home_team == 'Man United':
            temp_array = temp_array + [0,0,0,0,1,0]
        elif home_team == 'Tottenham':
            temp_array = temp_array + [0,0,0,0,0,1]
        
            
            
        away_team = request.form['away-team']
        if away_team == 'Arsenal':
            temp_array = temp_array + [1,0,0,0,0,0]
        elif away_team == 'Chelsea':
            temp_array = temp_array + [0,1,0,0,0,0]
        elif away_team == 'Liverpool':
            temp_array = temp_array + [0,0,1,0,0,0]
        elif away_team == 'Man City':
            temp_array = temp_array + [0,0,0,1,0,0]
        elif away_team == 'Man United':
            temp_array = temp_array + [0,0,0,0,1,0]
        elif away_team == 'Tottenham':
            temp_array = temp_array + [0,0,0,0,0,1]
            
            

        data = np.array([temp_array])
        
        prediction = regressor.predict(data)
        HomeTeam_prediction = int(prediction[:,0])
        AwayTeam_prediction = int(prediction[:,1])
        score = [HomeTeam_prediction , AwayTeam_prediction]      
        return render_template('result.html', HomeTeam_prediction=HomeTeam_prediction, AwayTeam_prediction=AwayTeam_prediction )



if __name__ == '__main__':
	app.run(debug=True)
