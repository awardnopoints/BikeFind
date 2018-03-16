from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm.session import sessionmaker
from bikefind.test_dbclass import staticData, dynamicData, weatherData
import requests
import time

# connect to local db 'test_db'
#This line is just a dummy and needs to be changed after pulling from remote
db_connection_string ='mysql+cymysql://root:pass@localhost:3306/test'
engine = create_engine(db_connection_string)

Session = sessionmaker(bind=engine)
session = Session()

# get from jcdecaux api and store data in list of json objects (station_info_list)
bikes_connection_string ='https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey=6e19678db44aa0bfdb4632faba1f58723758a2c4'

# get from openweathermap api and store data in dictionary
weather_connection_string = 'http://api.openweathermap.org/data/2.5/weather?q=Dublin&appid=416123cec041d7c358e497cd73c9657e'

def main():
    dynamic_index = 0
    # add static data (once-off)
    getStaticData()
    # add dynamic data to db every 10 mins
    while(True):

        Session = sessionmaker(bind=engine)
        session = Session()

        getDynamicData()
        #Weather data needs to put on a seperate timer somehow, currently duplicate rows are being appended (w/ unique index)
        #if dynamic_index % 2 == 0:
        getWeatherData()

        session.close()
        #600 seconds/ten minute approx (wait between end of code executing and starting again)
        print(dynamic_index)
        dynamic_index += 100
        print("sleeping now")
        time.sleep(50)

def getStaticData():
    r = requests.get(bikes_connection_string)
    station_info_list = r.json()
    for station in station_info_list:

        address = station['address']
        latitude = station['position']['lat']
        longitude = station['position']['lng']
        banking = station['banking']
        #add to db
        static_row = staticData(address = address, latitude = latitude, longitude = longitude, banking = banking )
        session.add(static_row)
        session.commit()

def getDynamicData():
        r = requests.get(bikes_connection_string)
        station_info_list = r.json()
        for station in station_info_list:

            curr_time = station['last_update']
            # var called curr_time to avoid clash with time function used below
            address = station['address']
            totalBikeStands = station['bike_stands']
            availableBikeStands = station['available_bike_stands']
            availableBikes = station['available_bikes']
            status = station['status']

            #Create DB object with dynamicData class, then try to add it to the DB
            dynamic_row = dynamicData(time = curr_time, address = address, totalBikeStands = totalBikeStands, availableBikeStands = availableBikeStands, availableBikes = availableBikes, status = status )
            session.add(dynamic_row)
            try:
                session.commit()
            except:
                session.rollback()
                return

def getWeatherData():
        r2 = requests.get(weather_connection_string)
        w_list = r2.json()

        w_time = w_list['dt']
        w_mainDescription = w_list['weather'][0]['main']
        w_detailedDescription = w_list['weather'][0]['description']
        w_icon = w_list['weather'][0]['icon']

        w_temp = w_list['main']['temp']
        w_maxTemp = w_list['main']['temp_max']
        w_minTemp = w_list['main']['temp_min']
        w_pressure = w_list['main']['pressure']
        w_humidity = w_list['main']['humidity']

        w_windSpeed = w_list['wind']['speed']
        w_windAngle = w_list['wind']['deg']
        w_cloudDensity = w_list['clouds']['all']
        w_visibility = w_list['visibility']

        #query DB to see row returned from API call is a duplicate
#        alldata = weatherData.query.all()
#        for data in alldata:
#            if data.time == w_time:
#                return
        #Create DB object with weatherData class, then try to add it to the DB
        weather_row = weatherData(time = w_time, mainDescription = w_mainDescription, detailedDescription = w_detailedDescription, icon = w_icon, currentTemp = w_temp, maxTemp = w_maxTemp, minTemp = w_minTemp, pressure = w_pressure, humidity = w_humidity, windSpeed = w_windSpeed, windAngle = w_windAngle, cloudDensity = w_cloudDensity, visibility = w_visibility)

        session.add(weather_row)
        try:
            session.commit()
        except:
            session.rollback()
            return

if __name__ == '__main__':
    main()
