from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm.session import sessionmaker
import requests
import time

weather_connection_string = 'http://api.openweathermap.org/data/2.5/weather?q=Dublin&appid=416123cec041d7c358e497cd73c9657e'
bikes_connection_string ='https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey=6e19678db44aa0bfdb4632faba1f58723758a2c4'
#db_connection_string ='mysql+cymysql://root:goop9oxt@localhost:3306/test'
#engine = create_engine(db_connection_string)
#
#session = Session()

r = requests.get(weather_connection_string)
station_info_list = r.json()
print(station_info_list['dt'])

time.sleep(50)

r = requests.get(weather_connection_string)
station_info_list = r.json()
print(station_info_list['dt'])
