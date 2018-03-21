from flask import Flask, render_template, jsonify
import pandas as pd
import bikefind.webscraper
from bikefind import webscraper


app = Flask(__name__)

@app.route('/')
def index():

    return render_template('index.html')

@app.route('/staticTest')
def getStaticTest():
    staticDataTable = pd.read_sql_table('staticData', webscraper.engine)
    #staticDataDictArray = staticDataTable.T.to_dict().values()
    staticDataDict = staticDataTable.to_dict(orient='index')
    staticData = jsonify(staticDataDict)
    return staticData

if __name__ == '__main__':
    app.run(debug=True, port =5002)