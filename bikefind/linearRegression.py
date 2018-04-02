#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  2 13:45:32 2018

@author: eoin
"""

import pandas as pd
import statsmodels.formula.api as sm
#import datetime


def main():
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
    myformula = "availableBikes ~ C(day) + C(status) + C(hour) + C(address) + C(detailedDescription) + currentTemp + pressure + humidity + windSpeed + windAngle + cloudDensity + visibility"
    lm = sm.ols(formula=myformula, data=df_merge).fit()
    print(lm.summary())

if __name__ == '__main__':
    main()
