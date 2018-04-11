#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 15:15:58 2018

@author: eoin
"""

import pandas as pd
from sklearn.utils import shuffle
from sklearn.linear_model import LinearRegression
from sklearn import metrics
from sklearn.cross_validation import cross_val_score
import pickle
    
def getPrediction(day, hour):
    lm = pickle.load(open( "model.p", "rb" ) )
    df_forecast = getForecastTable(day, hour)
    X = df_forecast
    X['Intercept'] = 1.0
    #for i in ['time', 'icon', 'datetime', 'latitude', 'longitude', 'banking', 'minTemp', 'maxTemp']:
    #    del X[i]
    X['hour'] = X['hour'].astype('category')
    X = pd.get_dummies(X)
    features = pickle.load(open( "features.p", "rb" ) )
    
    for feature in list(X):
        if feature not in features:
            del X[feature]
    for feature in features:
        if feature not in list(X):
            X[feature] = False
            
    X = X.reindex_axis(sorted(X.columns), axis=1)
    df_forecast["PredictedBikes"] = lm.predict(X)
    #return df_forecast
    print(lm.predict(X))

def getHistoricalTable():
    db_connection_string = "mysql+cymysql://conor:team0db1@team0db.cojxdhcdsq2b.us-west-2.rds.amazonaws.com/team0"
    
    # Add new columns to dynamicData dataframe for date, day, hour
    df_dynamic = pd.read_sql_table(table_name="dynamicData", con=db_connection_string)
        
    df_dynamic['datetime'] = pd.to_datetime(df_dynamic['time'] * 1000000, errors='ignore')
    df_dynamic['date'] = df_dynamic['datetime'].dt.date
    df_dynamic['day'] = df_dynamic['datetime'].dt.weekday_name
    df_dynamic['hour'] = df_dynamic['datetime'].dt.hour
    
    # Add new columns to weatherData dataframe for date, day, hour
    df_weather = pd.read_sql_table(table_name="weatherData", con=db_connection_string)
    df_weather['datetime'] = pd.to_datetime(df_weather['time'] * 1000000000, errors='ignore')
    df_weather['date'] = df_weather['datetime'].dt.date
    df_weather['day'] = df_weather['datetime'].dt.weekday_name
    df_weather['hour'] = df_weather['datetime'].dt.hour
    
    # Merge dynamic and weather on date, day, hour
    df_merge = pd.merge(df_dynamic, df_weather, on=['date', 'day', 'hour'])
    
    # Build linear regression to predict availableBikes
    return df_merge

def getForecastTable(myday, myhour):
    db_connection_string = "mysql+cymysql://conor:team0db1@team0db.cojxdhcdsq2b.us-west-2.rds.amazonaws.com/team0"

    # Add new columns to forecastData dataframe for date, day, hour
    df_forecast = pd.read_sql_table(table_name="forecastData", con=db_connection_string)
        
    df_forecast['datetime'] = pd.to_datetime(df_forecast['time'] * 1000000000, errors='ignore')
    df_forecast['date'] = df_forecast['datetime'].dt.date
    df_forecast['day'] = df_forecast['datetime'].dt.weekday_name
    df_forecast['hour'] = df_forecast['datetime'].dt.hour
    
    df_static = pd.read_sql_table(table_name="staticData", con=db_connection_string)
    df_static['day'] = myday
    df_static['hour'] = myhour
    
    df_merge = pd.merge(df_forecast, df_static, on=['day', 'hour'])
    
    return df_merge

if __name__ == "__main__":
    print(getPrediction("Thursday", 9))