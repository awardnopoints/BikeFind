#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  2 13:45:32 2018

@author: eoin
"""

import pandas as pd
import statsmodels.formula.api as sm
from sklearn.linear_model import LinearRegression
import pickle
import time

def getModel():
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
    myformula = "availableBikes ~ C(day) + C(status) + C(hour) + C(address)"
    lm = sm.ols(formula=myformula, data=df_merge).fit()
    return lm


def saveModelAlt(model_name):
    start = time.time()
    db_connection_string = "mysql+cymysql://conor:team0db1@team0db.cojxdhcdsq2b.us-west-2.rds.amazonaws.com/team0"
    
    # Add new columns to dynamicData dataframe for date, day, hour
    df_dynamic = pd.read_sql_table(table_name="dynamicData", con=db_connection_string)
    
    now = time.time()
    current = now - start
    print("Get Data:", current)
    
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
    
    now = time.time()
    current = now - start
    print("Build weather dataframe:", current)

    # Merge dynamic and weather on date, day, hour
    df_merge = pd.merge(df_dynamic, df_weather, on=['date', 'day', 'hour'])
    df_merge['Intercept'] = 1.0
    # Build linear regression to predict availableBikes
#    myformula = "availableBikes ~ C(day) + C(status) + C(hour) + C(address)"
#    lm = sm.ols(formula=myformula, data=df_merge).fit()
    
    X = df_merge[['Intercept', 
                'day', 
                'status', 
                'hour', 
                'address', 
                'mainDescription',
             ]]
    X['hour'] = X['hour'].astype('category')

    y = df_merge['availableBikes']
    X = pd.get_dummies(X, prefix=['day', 'status', 'hour', 'address', 'mainDescription'])
    print(list(X))
    print(X.head(10))
    lm = LinearRegression().fit(X, y)

    now = time.time()
    current = now - start
    print("Build model:", current)
        
    pickle.dump(lm, open(model_name, 'wb'))

    now = time.time()
    current = now - start
    print("Save model:", current)
    
    prediction_list = []
    predictions = lm.predict(X)
    for i in range(len(predictions)):
        prediction_list.append(predictions[i])
        
    predict_df = pd.DataFrame({'PredictedBikes':prediction_list, 'ActualBikes': y})
    
    #predict_df = pd.DataFrame({'PredictedBikes': loaded_lm.predict(df), 'ActualBikes': df["availableBikes"]})
    print(predict_df[['PredictedBikes', 'ActualBikes']].head(100)) 

    now = time.time()
    current = now - start
    print("Make Predictions:", current)
    
    stop = time.time()
    elapsed = stop - start
    print("Total time elapsed:", elapsed)


def saveModel(model_name):
    start = time.time()
    db_connection_string = "mysql+cymysql://conor:team0db1@team0db.cojxdhcdsq2b.us-west-2.rds.amazonaws.com/team0"
    
    # Add new columns to dynamicData dataframe for date, day, hour
    df_dynamic = pd.read_sql_table(table_name="dynamicData", con=db_connection_string)
    
    now = time.time()
    current = now - start
    print("Get Data:", current)
    
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
    
    now = time.time()
    current = now - start
    print("Build weather dataframe:", current)

    # Merge dynamic and weather on date, day, hour
    df_merge = pd.merge(df_dynamic, df_weather, on=['date', 'day', 'hour'])
    
    # Build linear regression to predict availableBikes
    myformula = "availableBikes ~ C(day) + C(status) + C(hour) + C(address)"
    lm = sm.ols(formula=myformula, data=df_merge).fit()

    now = time.time()
    current = now - start
    print("Build model:", current)
        
    pickle.dump(lm, open(model_name, 'wb'))

    now = time.time()
    current = now - start
    print("Save model:", current)
    
    stop = time.time()
    elapsed = stop - start
    print("Total time elapsed:", elapsed)

def loadModel(model_name):
    start = time.time()
    
    
    loaded_lm = pickle.load(open(model_name, 'rb'))
    
    now = time.time()
    current = now - start
    print("Load Model:", current)
    
    df = pd.read_csv('modelTestData.csv')

    predict_df = pd.DataFrame({'PredictedBikes': loaded_lm.predict(df), 'ActualBikes': df["availableBikes"]})
    print(predict_df[['PredictedBikes', 'ActualBikes']].head(10)) 

    now = time.time()
    current = now - start
    print("Make Predictions:", current)
    
    stop = time.time()
    elapsed = stop - start
    print("Total time elapsed:", elapsed)
    
def loadModelAlt(model_name):
    start = time.time()
    
    loaded_lm = pickle.load(open(model_name, 'rb'))
    
    now = time.time()
    current = now - start
    print("Load Model:", current)

    
    df = pd.read_csv('modelTestData.csv')
    df['Intercept'] = 1.0
    X_test = df[['Intercept', 
                'day', 
                'status', 
                'hour', 
                'address', 
                'mainDescription',
             ]]
    X_test['hour'] = X_test['hour'].astype('category')

    y_test = df['availableBikes']
    X_test = pd.get_dummies(X_test, prefix=['day', 'status', 'hour', 'address', 'mainDescription'])
    #print(list(X_test))
    
    feature_list = ['day_Friday', 'day_Monday', 'day_Saturday', 'day_Sunday', 
                    'day_Thursday', 'day_Tuesday', 'day_Wednesday', 'status_CLOSED', 
                    'status_OPEN', 'hour_0', 'hour_1', 'hour_2', 'hour_3', 'hour_4', 
                    'hour_5', 'hour_6', 'hour_7', 'hour_8', 'hour_9', 'hour_10', 
                    'hour_11', 'hour_12', 'hour_13', 'hour_14', 'hour_15', 'hour_16', 
                    'hour_17', 'hour_18', 'hour_19', 'hour_20', 'hour_21', 'hour_22', 
                    'hour_23', 'address_Barrow Street', 'address_Benson Street', 
                    'address_Blackhall Place', 'address_Blessington Street', 
                    'address_Bolton Street', 'address_Brookfield Road', 
                    'address_Cathal Brugha Street', 'address_Charlemont Street', 
                    'address_Christchurch Place', 'address_City Quay', 
                    'address_Clarendon Row', 'address_Clonmel Street', 
                    'address_Collins Barracks Museum', 'address_Convention Centre', 
                    'address_Custom House', 'address_Custom House Quay', 
                    'address_Dame Street', 'address_Denmark Street Great', 
                    'address_Deverell Place', 'address_Earlsfort Terrace', 
                    'address_Eccles Street', 'address_Eccles Street East', 
                    'address_Emmet Road', 'address_Exchequer Street', 
                    'address_Excise Walk', 'address_Fenian Street', 
                    'address_Fitzwilliam Square East', 'address_Fitzwilliam Square West', 
                    'address_Fownes Street Upper', 'address_Francis Street', 
                    'address_Frederick Street South', "address_George's Lane", 
                    'address_Georges Quay', 'address_Golden Lane', 
                    'address_Grand Canal Dock', 'address_Grangegorman Lower (Central)', 
                    'address_Grangegorman Lower (North)', 'address_Grangegorman Lower (South)', 
                    'address_Grantham Street', 'address_Grattan Street', 
                    'address_Greek Street', 'address_Guild Street', 'address_Hanover Quay', 
                    'address_Harcourt Terrace', 'address_Hardwicke Place', 
                    'address_Hardwicke Street', 'address_Hatch Street', 'address_Herbert Place', 
                    'address_Herbert Street', 'address_Heuston Bridge (North)', 
                    'address_Heuston Bridge (South)', 'address_Heuston Station (Car Park)', 
                    'address_Heuston Station (Central)', 'address_High Street', 
                    'address_James Street', 'address_Jervis Street', 
                    'address_John Street West', 'address_Kevin Street', 
                    'address_Kilmainham Gaol', 'address_Kilmainham Lane', 
                    'address_King Street North', 'address_Leinster Street South', 
                    'address_Lime Street', 'address_Market Street South', 
                    'address_Mater Hospital', 'address_Merrion Square East', 
                    'address_Merrion Square West', 'address_Molesworth Street', 
                    'address_Mount Brown', 'address_Mount Street Lower', 
                    'address_Mountjoy Square West', 'address_New Central Bank', 
                    'address_Newman House', 'address_North Circular Road', 
                    'address_Oliver Bond Street', 'address_Ormond Quay Upper', 
                    'address_Parkgate Street', 'address_Parnell Square North', 
                    'address_Parnell Street', 'address_Pearse Street', 
                    'address_Portobello Harbour', 'address_Portobello Road', 
                    "address_Princes Street / O'Connell Street", 'address_Rothe Abbey', 
                    'address_Royal Hospital', 'address_Sandwith Street', 
                    "address_Sir Patrick's Dun", 'address_Smithfield', 
                    'address_Smithfield North', 'address_South Dock Road', 
                    'address_St James Hospital (Luas)', 'address_St. James Hospital (Central)', 
                    "address_St. Stephen's Green East", "address_St. Stephen's Green South", 
                    'address_Strand Street Great', 'address_Talbot Street', 'address_The Point', 
                    'address_Townsend Street', 'address_Upper Sherrard Street', 
                    'address_Western Way', 'address_Wilton Terrace', 
                    'address_Wolfe Tone Street', 'address_York Street East', 
                    'address_York Street West', 'mainDescription_Clear', 
                    'mainDescription_Clouds', 'mainDescription_Drizzle', 
                    'mainDescription_Fog', 'mainDescription_Mist', 
                    'mainDescription_Rain', 'mainDescription_Snow']
    
    print(X_test.head(10))
    for feature in feature_list:
        if feature not in list(X_test):
            X_test[feature] = 0
    print(X_test.head(10))


    
    prediction_list = []
    predictions = loaded_lm.predict(X_test)
    for i in range(len(predictions)):
        prediction_list.append(predictions[i])
        
    predict_df = pd.DataFrame({'PredictedBikes':prediction_list, 'ActualBikes': y_test})
    
    #predict_df = pd.DataFrame({'PredictedBikes': loaded_lm.predict(df), 'ActualBikes': df["availableBikes"]})
    print(predict_df[['PredictedBikes', 'ActualBikes']].head(100)) 

    now = time.time()
    current = now - start
    print("Make Predictions:", current)
    
    stop = time.time()
    elapsed = stop - start
    print("Total time elapsed:", elapsed)


if __name__ == '__main__':
    loadModelAlt('mymodel3.sav')
