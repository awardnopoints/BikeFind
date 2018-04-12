from flask import Flask, render_template, jsonify, request
import pandas as pd
from sqlalchemy import create_engine
from geopy.distance import great_circle

app = Flask(__name__)

db_connection_string = "mysql+cymysql://conor:team0db1@team0db.cojxdhcdsq2b.us-west-2.rds.amazonaws.com/team0"
#db_connection_string ='mysql+cymysql://root:password@localhost:3306/test_db'
engine = create_engine(db_connection_string)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/staticTest')
def getStaticTest():
    """Returns data from staticDataTable as JSON"""
#    staticDataTable = pd.read_sql_table('staticData', engine)
    #staticDataDictArray = staticDataTable.T.to_dict().values()

    # for now including both concat latlng, as well as separate lat and lng. until we know which is handier for what.
    #query = "select * from staticData inner join currentData on \
    #        staticData.address=currentData.address"
    query = 'select staticData.address, currentData.availableBikes, currentData.availableBikeStands, currentData.totalBikeStands, currentData.status, staticData.latitude, staticData.longitude, CONCAT("(", staticData.latitude, ", ", staticData.longitude, ")") AS LatLng from currentData inner join staticData where currentData.address=staticData.address group by staticData.address'


    df = pd.read_sql_query(query, engine)
    staticDataDict = df.to_dict(orient='index')
    staticData = jsonify(staticDataDict)
    return staticData


@app.route('/markerData')
def getMarkerData():
    """Returns data from relevant data for styling placing and styling station markers."""
    query = 'select staticData.address, currentData.availableBikes, currentData.availableBikeStands, currentData.status, staticData.latitude, staticData.longitude, CONCAT("(", staticData.latitude, ", ", staticData.longitude, ")") AS LatLng from currentData inner join staticData where currentData.address=staticData.address group by staticData.address'
    df = pd.read_sql_query(query, engine)
    df = df.to_dict(orient='index')
    df = jsonify(df)
    return markerData
    
    

@app.route('/rtpi', methods=['POST'])
def getRtpi():
    """Receives a requested address, then retrieves the latest data from currentDataTable
    and sends back a JSON object with the data for the requested station"""
    currentDataTable = pd.read_sql_table('currentData', engine)
    currentDataDict = currentDataTable.to_dict(orient='index')
    station = request.form['reqAddress']
    for i in range(len(currentDataDict)):
        if currentDataDict[i]['address'] == station:
            reqStationList = currentDataDict[i]
            break
    return jsonify({"reqJson" : reqStationList})

@app.route('/findstation/<coords>')
def findstation(coords):
    """Function to find the three nearest stations to the given coordinates.
        The address, proximity, bike availability and open/closed status of these stations is returned."""

    # for now including both concat latlng, as well as separate lat and lng. until we know which is handier for what.
    query = 'select staticData.address, currentData.availableBikes, currentData.availableBikeStands, currentData.status, staticData.latitude, staticData.longitude, CONCAT("(", staticData.latitude, ", ", staticData.longitude, ")") AS LatLng from currentData inner join staticData where currentData.address=staticData.address group by staticData.address'

    df = pd.read_sql_query(query, engine)

    #add a new column for distance to current location
    df['proximity'] = df.LatLng.apply(lambda station: great_circle(station, coords).meters)
    nearestStations = df.sort_values('proximity').head(3)

    #convert nearestStations df to json
    #ideally find a way to get rid of the index key value pair
    nearestJson = nearestStations[['address', 'proximity', 'availableBikes', 'availableBikeStands', 'status', 'LatLng', 'latitude', 'longitude']].reset_index().to_json()


    #return "Second nearest station is: " + nearestStations['address'].tolist()[1]
    return nearestJson


@app.route('/getWeather')
def getWeatherData():
    weatherDataTable = pd.read_sql_table('weatherData', engine)
    #weatherDataDictArray = weatherDataTable.T.to_dict().values()
#    weatherData = weatherDataTable.tail(0)
    weatherDataDict = weatherDataTable.to_dict(orient='index')
    weatherData = weatherDataDict[len(weatherDataDict)-1]
    print(weatherData)
    return jsonify(weatherData)

def appWrapper():
    """Wrapper to allow entry point to app.run with the correct arguments"""
    app.run(host='0.0.0.0', port=5001)
#    app.run(ssl_context='adhoc')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
#    app.run(ssl_context='adhoc')
