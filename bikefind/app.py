from flask import Flask, render_template, jsonify
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
    staticDataTable = pd.read_sql_table('staticData', engine)
    #staticDataDictArray = staticDataTable.T.to_dict().values()
    staticDataDict = staticDataTable.to_dict(orient='index')
    staticData = jsonify(staticDataDict)
    return staticData

@app.route('/rtpi')
def getRtpi(request):
    r = requests.get(bikes_connection_string)
    station_info_list = r.json()
    return station_info_list[request]



def appWrapper():
    app.run(host='0.0.0.0', port=5001)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
