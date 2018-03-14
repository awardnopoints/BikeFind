from flask import Flask, render_template
import requests
from sqlalchemy import create_engine

db_connection_string ='mysql+cymysql://root:password@localhost:3306/test_db'
engine = create_engine(db_connection_string)
connection = engine.connect()

print('Table names for test_db: ', engine.table_names(), '\n')

bikes_connection_string ='https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey=6e19678db44aa0bfdb4632faba1f58723758a2c4'
r = requests.get(bikes_connection_string)
for obj in r.json()[:20]:
    print(obj)
    print('\n')
  
weather_connection_string = 'http://api.openweathermap.org/data/2.5/weather?q=Dublin&appid=416123cec041d7c358e497cd73c9657e'  
r2 = requests.get(weather_connection_string).json()
print(r2)