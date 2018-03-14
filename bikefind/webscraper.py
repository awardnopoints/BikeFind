from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm.session import sessionmaker
from bikefind.test_dbclass import staticData, dynamicData
import requests
import time

# connect to local db 'test_db'
db_connection_string ='mysql+cymysql://root:password@localhost:3306/test_db'
engine = create_engine(db_connection_string)

Session = sessionmaker(bind=engine)
session = Session()

# get from jcdecaux api and store data in list of json objects (station_info_list)
bikes_connection_string ='https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey=6e19678db44aa0bfdb4632faba1f58723758a2c4'
r = requests.get(bikes_connection_string)
station_info_list = r.json()

# get from openweathermap api and store data in dictionary
weather_connection_string = 'http://api.openweathermap.org/data/2.5/weather?q=Dublin&appid=416123cec041d7c358e497cd73c9657e'  
r2 = requests.get(weather_connection_string).json()
print(r2["weather"][0]["main"])


def main():
    while(True):
        # code here to make a new api call, parse the data and add to db
        
        r = requests.get(bikes_connection_string)
        station_info_list = r.json()
        for station in station_info_list:
            # first check i'm getting the correct data
            #static
            print('static:')
            print(station['name'])
            print(station['position']['lat'])
            print(station['position']['lng'])
            print(station['banking'])
            print('dynamic:')
            #dynamic
            print(station['last_update'])
            print(station['address'])
            print(station['bike_stands'])
            print(station['available_bike_stands'])
            print(station['available_bikes'])
            print(station['status'])
        
        time.sleep(600)
#600 seconds/ten minute approx (wait between end of code executing and starting again)
        

def add_row():
    # add the code to add each row
    pass

##############
# example - adding a row

#dame_street = staticData(address = 'dame street',
 #                              banking = "Yes")    

#session.add(dame_street)
#session.commit()
###########
  

if __name__ == '__main__':
    main()


