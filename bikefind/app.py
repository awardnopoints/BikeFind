# import sys
# sys.path.append('..')

from flask import Flask, render_template, jsonify, request
import pandas as pd
from sqlalchemy import create_engine
from geopy.distance import great_circle
#from linearRegression import lm, features, getPrediction
from BikeFind.linearRegression import lm, features, getPrediction


app = Flask(__name__)

db_connection_string = "mysql+cymysql://conor:team0db1@team0db.cojxdhcdsq2b.us-west-2.rds.amazonaws.com/team0"
#db_connection_string ='mysql+cymysql://root:password@localhost:3306/test_db'
engine = create_engine(db_connection_string)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/markerData/<coords>')
def getMarkerData(coords):
    """Returns data from relevant data for placing and styling station markers. Takes in current location coords for proximity"""
    # prune the query to only get what we're using
    query = 'select staticData.address, currentData.availableBikes, currentData.availableBikeStands, currentData.totalBikeStands, currentData.status, staticData.latitude, staticData.longitude, CONCAT("(", staticData.latitude, ", ", staticData.longitude, ")") AS LatLng from currentData inner join staticData where currentData.address=staticData.address group by staticData.address'
    df = pd.read_sql_query(query, engine)
    df['proximity'] = df.LatLng.apply(lambda station: great_circle(station, coords).meters)
    df = df.sort_values('proximity')
    df = df.to_dict(orient='index')
    markerData = jsonify(df)
    return markerData
    
    
@app.route('/getWeather')
def getWeatherData():
    weatherDataTable = pd.read_sql_table('weatherData', engine)
    #weatherDataDictArray = weatherDataTable.T.to_dict().values()
#    weatherData = weatherDataTable.tail(0)
    weatherDataDict = weatherDataTable.to_dict(orient='index')
    weatherData = weatherDataDict[len(weatherDataDict)-1]
    return jsonify(weatherData)

@app.route('/getPrediction/<requestedTime>/<coords>')
def getPredictionData(requestedTime, coords):
    parameters = requestedTime.split()
    data = getPrediction(parameters[0], int(parameters[1]))
    data['proximity'] = data.LatLng.apply(lambda station: great_circle(station, coords).meters)
    data = data.sort_values('proximity')
    data = data.to_dict(orient='index')
    return jsonify(data)

@app.route('/availabilityChart/<address>')
def getChartData(address):
    # need two sets of quotation marks, because address need to be in quotation marks in the query.
    #address = '"Barrow Street"'
    query = 'select address, availableBikes, availableBikeStands from currentData where address={} group by address'.format(address)
    
    # just selecting 15 stations for this test chart
    df = pd.read_sql_query(query, engine)[:15]
    dfDict = df.to_dict(orient='index')
    dfJson = dfDict 
    
    # constuct json file in the required format for google charts
    jsonData = {
          "cols": [{"label": 'Address', "type": 'string'},
                 {"label": 'Available Bikes', "type": 'number'},
                 {"label": 'Free Bike Stands', "type": 'number'}
          ]}
    
    jsonData["rows"] = []
    for r in dfJson.values():
        address_dict = {"v": r["address"]}
        bikes_dict = {"v": int(r["availableBikes"])}
        stands_dict = {"v": int(r["availableBikeStands"])}
        jsonData["rows"].append({"c":[address_dict, bikes_dict, stands_dict]})
#      
    
    return jsonify(jsonData)
    
def appWrapper():
    """Wrapper to allow entry point to app.run with the correct arguments"""
    app.run(host='0.0.0.0', port=5001)
#    app.run(ssl_context='adhoc')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
#    app.run(ssl_context='adhoc')
