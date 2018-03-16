from sqlalchemy import create_engine, exc
from sqlalchemy.orm.session import sessionmaker
from bikefind.dbClasses import staticData, dynamicData, weatherData
import requests, time, logging

logging.basicConfig(filename='webscraper.log', level=logging.ERROR, format='%(asctime)s:%(levelname)s:%(message)s')

#connect to remote DBS
db_connection_string = "mysql+cymysql://conor:team0db1@team0db.cojxdhcdsq2b.us-west-2.rds.amazonaws.com/team0"
#db_connection_string = "mysql+cymysql://root:password@localhost/test"
engine = create_engine(db_connection_string)

Session = sessionmaker(bind=engine)
session = Session()

# get from jcdecaux api and store data in list of json objects (station_info_list)
bikes_connection_string ='https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey=6e19678db44aa0bfdb4632faba1f58723758a2c4'

# get from openweathermap api and store data in dictionary
weather_connection_string = 'http://api.openweathermap.org/data/2.5/weather?q=Dublin&appid=416123cec041d7c358e497cd73c9657e'

def main():

    # add static data (once-off)
    getStaticData()
    counter = 0

    while(True):

        #New DB session for each iteration
        Session = sessionmaker(bind=engine)
        session = Session()

        getDynamicData()

        #update weather every 30 minutes
        if counter % 6 == 0:
            getWeatherData()

        session.close()
        #300 seconds/5 minute approx (wait between end of code executing and starting again)
        counter += 1
        print("sleeping now", counter)
        time.sleep(300)

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
        try:
            session.commit()
        except exc.IntegrityError:
            session.rollback()
        except Exception:
            session.rollback()
            logging.exception()
    session.close()

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
            except exc.IntegrityError:
                session.rollback()
            except Exception:
                session.rollback()
                logging.exception()

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
        except exc.IntegrityError:
            session.rollback()
        except Exception:
            session.rollback()
            logging.exception()

if __name__ == '__main__':
    main()
