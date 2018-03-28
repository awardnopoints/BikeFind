from flask import Flask, render_template
import requests
from sqlalchemy import create_engine
import json

# connect to local db 'test_db'
db_connection_string ='mysql+cymysql://root:password@localhost:3306/test_db'
engine = create_engine(db_connection_string)
connection = engine.connect()

# get from jcdecaux api and store data in list of json objects (station_info_list)
bikes_connection_string ='https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey=6e19678db44aa0bfdb4632faba1f58723758a2c4'
r = requests.get(bikes_connection_string)
station_info_list = r.json()

# get from openweathermap api and store data in dictionary
weather_connection_string = 'http://api.openweathermap.org/data/2.5/weather?q=Dublin&appid=416123cec041d7c358e497cd73c9657e'  
r2 = requests.get(weather_connection_string).json()
print(r2["weather"][0]["main"])

# add rows to the table from selection of the api data
for obj in station_info_list[25:35]:
    name = obj["address"]
    available_bikes = obj["available_bikes"]
    print(type(name))
    print("\n")
    connection.execute("INSERT INTO test_db.stations (name, position, available_bikes) VALUES ('{}', '54.145/-5.145', {});".format(name, available_bikes))


test_db_stations = connection.execute("SELECT * FROM test_db.stations;")

# retrieving data from db
for row in test_db_stations:
    print(row['name'], '\n')
    print(row['position'], '\n')
    print(row['available_bikes'], '\n')

#print(engine.table_names())

#test_query2 = connection.execute("INSERT INTO test_db.stations (name, position, available_bikes) VALUES ('grantham street', '54.145/-5.145', '9');")
# careful of the inserts. throws an exception if a primary key is duplicated

connection.close()

