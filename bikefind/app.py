from flask import Flask, render_template, jsonify, request
import pandas as pd
from sqlalchemy import create_engine

app = Flask(__name__)

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
    currentDataTable = pd.read_sql_table('currentData', engine)
    currentDataDict = currentDataTable.to_dict(orient='index')
    station = request.form['reqAddress']
    for i in range(len(currentDataDict)):
        if currentDataDict[i]['address'] == station:
            reqStationList = currentDataDict[i]
            break
    return jsonify({"reqJson" : reqStationList})



def appWrapper():
    """Wrapper to allow entry point to app.run with the correct arguments"""
    app.run(host='0.0.0.0', port=5001)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
