from flask import Flask, render_template, jsonify, request
import requests
import pandas as pd
from sqlalchemy import create_engine
from geopy.distance import great_circle

app = Flask(__name__)

bikes_connection_string = 'https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey=6e19678db44aa0bfdb4632faba1f58723758a2c4'
db_connection_string = "mysql+cymysql://conor:team0db1@team0db.cojxdhcdsq2b.us-west-2.rds.amazonaws.com/test2"
#db_connection_string ='mysql+cymysql://root:password@localhost:3306/test_db'
engine = create_engine(db_connection_string)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/staticTest')
def getStaticTest():
    """Returns data from staticDataTable as JSON"""
    staticDataTable = pd.read_sql_table('staticData', engine)
    #staticDataDictArray = staticDataTable.T.to_dict().values()
    staticDataDict = staticDataTable.to_dict(orient='index')
    staticData = jsonify(staticDataDict)
    return staticData

@app.route('/rtpi', methods=['POST'])
def getRtpi():
    """Receives a requested address, then retrieves the latest data via API
    call and sends back a JSON object with the data for the requested station"""
    r = requests.get(bikes_connection_string)
    station_info_list = r.json()
    station = request.form['reqAddress']
    print(station)
    for i in station_info_list:
        if i['address'] == station:
            reqStationList = i
            break
    print(reqStationList)
    return jsonify({"reqJson" : reqStationList})

@app.route('/findstation/<coords>')
def findstation(coords):
    """Function to find the three nearest stations to the given coordinates. 
        The address, proximity, bike availability and open/closed status of these stations is returned."""
    
    
    # query to provide a temp df with latlng for each station and the current availability.
    # needs tweaking - i'm not selecting the most recent update for each station correctly yet. 
    query = 'select staticData.address, currentData.availableBikes, currentData.status, CONCAT("(", staticData.latitude, ", ", staticData.longitude, ")") AS LatLng from currentData inner join staticData where currentData.address=staticData.address group by staticData.address'
    
    df = pd.read_sql_query(query, engine)
    
    #add a new column for distance to current location
    df['proximity'] = df.LatLng.apply(lambda station: great_circle(station, coords).meters)
    nearestStations = df.sort_values('proximity').head(3)
    
    #convert nearestStations df to json
    #ideally find a way to get rid of the index key value pair
    nearestJson = nearestStations[['address', 'proximity', 'availableBikes', 'status']].reset_index().to_json()
    
    
    #return "Second nearest station is: " + nearestStations['address'].tolist()[1]
    return nearestJson



def appWrapper():
    """Wrapper to allow entry point to app.run with the correct arguments"""
    app.run(host='0.0.0.0', port=5001)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
