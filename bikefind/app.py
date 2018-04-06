from flask import Flask, render_template, jsonify, request
import requests
import pandas as pd
from sqlalchemy import create_engine

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



def appWrapper():
    """Wrapper to allow entry point to app.run with the correct arguments"""
#    app.run(host='0.0.0.0', port=5001)
    app.run(ssl_context='adhoc')

if __name__ == '__main__':
#    app.run(host='0.0.0.0', port=5001)
    app.run(ssl_context='adhoc')
