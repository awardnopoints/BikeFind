from sqlalchemy import create_engine, exc
from sqlalchemy.orm.session import sessionmaker
from bikefind.dbClasses import staticData, dynamicData, currentData, weatherData, forecastData
import requests
import time
import logging

logging.basicConfig(filename='webscraper.log', level=logging.ERROR,
                    format='%(asctime)s:%(levelname)s:%(message)s')

# connect to remote DBS
db_connection_string = "mysql+cymysql://conor:team0db1@team0db.cojxdhcdsq2b.us-west-2.rds.amazonaws.com/team0"
# db_connection_string = "mysql+cymysql://root:password@localhost/test"
engine = create_engine(db_connection_string)

Session = sessionmaker(bind=engine)
session = Session()

# get from jcdecaux api and store data in list of json objects (station_info_list)
bikes_connection_string = 'https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey=6e19678db44aa0bfdb4632faba1f58723758a2c4'

# get from openweathermap api and store data in dictionary
weather_connection_string = 'http://api.openweathermap.org/data/2.5/weather?q=Dublin&appid=416123cec041d7c358e497cd73c9657e'

forecast_connection_string = 'http://api.openweathermap.org/data/2.5/forecast?q=Dublin&appid=416123cec041d7c358e497cd73c9657e'


def main():
    """Runs an infinite loop, calling DB update functions on each iteration.
    getStaticData is called once, getDynamicData every 5 mins, and getWeatherData
    every 30 mins"""
    # add static data (once-off)
    getStaticData()

    Session = sessionmaker(bind=engine)
    session = Session()

    getStaticData()

    getCurrentData()

    getForecastData()
    session.close()

    counter = 0
    while(True):
        # New DB session for each iteration
        Session = sessionmaker(bind=engine)
        session = Session()

        getDynamicData()

        # update weather every 30 minutes
        if counter % 6 == 0:
            getWeatherData()
            if counter % 12 == 0:
                getForecastData()

        session.close()
        counter += 1
        print("sleeping now", counter)
        # 300 seconds - execution time for one iteration (~55s)
        time.sleep(245)


def getStaticData():
    """Creates a table in DB for bike station static data. Populates the table
    with data from an API request, one row for each station"""
    r = requests.get(bikes_connection_string)
    station_info_list = r.json()

    x = 0
    for station in station_info_list:
        address = station['address']
        latitude = station['position']['lat']
        longitude = station['position']['lng']
        banking = station['banking']

        # add to db
        static_row = staticData(address=address, latitude=latitude,
                                longitude=longitude, banking=banking)
        session.add(static_row)
        try:
            session.commit()
        except exc.IntegrityError:
            session.rollback()
        except Exception as e:
            session.rollback()
            logging.error(e)


def getCurrentData():
    """Makes an API request, and checks the results against dynamicData,
    replaces any rows not already in dynamicData to currentData.
    Created the currentData table if it doesn't already exist using model from
    dbClasses"""
    r = requests.get(bikes_connection_string)
    station_info_list = r.json()

    for station in station_info_list:
        address = station['address']
        last_update = station['last_update']
        totalBikeStands = station['bike_stands']
        availableBikeStands = station['available_bike_stands']
        availableBikes = station['available_bikes']
        status = station['status']

        # add to db
        current_row = currentData(address=address, last_update=last_update,
                                  totalBikeStands=totalBikeStands,
                                  availableBikeStands=availableBikeStands,
                                  availableBikes=availableBikes,
                                  status=status)
        session.add(current_row)
        try:
            session.commit()
        except exc.IntegrityError:
            session.rollback()
        except Exception as e:
            session.rollback()
            logging.error(e)

        #x += 1
        # if x % 5 == 0:
            #print("Current Bikes Counted:", x, '/', len(station_info_list))
    session.close()


def getDynamicData():
    """Creates a table using dynamicData dbClass if it doesn't
    already exist, makes an API call to bikes API and appends
    all rows to dynamicData, if they aren't aready in the table"""
    r = requests.get(bikes_connection_string)
    station_info_list = r.json()
    for station in station_info_list:

        try:
            curr_time = station['last_update']
        except KeyError:
            return
        try:
            address = station['address']
        except KeyError:
            return
        try:
            totalBikeStands = station['bike_stands']
        except KeyError:
            totalBikeStands = 0
        try:
            availableBikeStands = station['available_bike_stands']
        except KeyError:
            availableBikeStands = 0
        try:
            availableBikes = station['available_bikes']
        except KeyError:
            availableBikes = 0
        try:
            status = station['status']
        except KeyError:
            status = 'default'

        # Create DB object with dynamicData class, then try to add it to the DB
        dynamic_row = dynamicData(time=curr_time, address=address,
                                  totalBikeStands=totalBikeStands,
                                  availableBikeStands=availableBikeStands,
                                  availableBikes=availableBikes, status=status)
        session.add(dynamic_row)
        success = False
        try:
            session.commit()
            success = True
        except exc.IntegrityError:
            session.rollback()
            success = False
        except Exception as e:
            session.rollback()
            logging.error(e)
            success = False

        if success:
            # if the previous commit goes through, then this block checks the
            # new data against the current values in the currentData table,
            # and updates appropriately (should probably be a separate function)

            # find currentData row with matching address value
            match = session.query(currentData).filter(
                currentData.address == address).one()
            #print("For", match.address, "station:")
            if curr_time > match.last_update:  # check if the timestamp is different, if not, ignore
                # print("Before:", match.last_update, match.totalBikeStands,
                #                          match.availableBikeStands, match.status)
                # update values in row
                match.last_update = curr_time
                match.totalBikeStands = totalBikeStands
                match.availableBikeStands = availableBikeStands
                match.availableBikes = availableBikes
                match.status = status
                # print("After:", match.last_update, match.totalBikeStands,
#                          match.availableBikeStands, match.status)
                try:
                    session.commit()
                except exc.IntegrityError:
                    session.rollback()
                except Exception as e:
                    session.rollback()
                    logging.error(e)


def getWeatherData():
    """Creates table for weather data from class in dbClasses file. Makes an API
    call and appends populates the table. Appends to table if it already exists """
    r2 = requests.get(weather_connection_string)
    w_list = r2.json()
    try:
        w_time = w_list['dt']
    except KeyError:
        return
    try:
        w_mainDescription = w_list['weather'][0]['main']
    except KeyError:
        w_mainDescription = 'default'
    try:
        w_detailedDescription = w_list['weather'][0]['description']
    except KeyError:
        w_detailedDescription = 'default'
    try:
        w_icon = w_list['weather'][0]['icon']
    except KeyError:
        w_icon = 'default'

    try:
        w_temp = w_list['main']['temp']
    except KeyError:
        w_temp = 0
    try:
        w_maxTemp = w_list['main']['temp_max']
    except KeyError:
        w_maxTemp = 0
    try:
        w_minTemp = w_list['main']['temp_min']
    except KeyError:
        w_minTemp = 0
    try:
        w_pressure = w_list['main']['pressure']
    except KeyError:
        w_pressure = 0
    try:
        w_humidity = w_list['main']['humidity']
    except KeyError:
        w_humidity = 0

    try:
        w_windSpeed = w_list['wind']['speed']
    except KeyError:
        w_windSpeed = 0
    try:
        w_windAngle = w_list['wind']['deg']
    except KeyError:
        w_windAngle = 0
    try:
        w_cloudDensity = w_list['clouds']['all']
    except KeyError:
        w_cloudDensity = 0
    try:
        w_visibility = w_list['visibility']
    except KeyError:
        w_visibility = 0

    # Create DB object with weatherData class, then try to add it to the DB
    weather_row = weatherData(time=w_time, mainDescription=w_mainDescription,
                              detailedDescription=w_detailedDescription,
                              icon=w_icon, currentTemp=w_temp, maxTemp=w_maxTemp,
                              minTemp=w_minTemp, pressure=w_pressure,
                              humidity=w_humidity, windSpeed=w_windSpeed,
                              windAngle=w_windAngle, cloudDensity=w_cloudDensity,
                              visibility=w_visibility)

    session.add(weather_row)
    try:
        session.commit()
    except exc.IntegrityError:
        session.rollback()
    except Exception as e:
        session.rollback()
        logging.error(e)


def getForecastData():
    """Makes api call for forecast data to openweathermap API and adds to forecastData table."""
    r2 = requests.get(forecast_connection_string)
    f_list = r2.json()
    for f in f_list["list"]:
        try:
            f_time = f['dt']
        except KeyError:
            return
        try:
            f_mainDescription = f['weather'][0]['main']
        except KeyError:
            f_mainDescription = 'default'
        try:
            f_detailedDescription = f['weather'][0]['description']
        except KeyError:
            f_detailedDescription = 'default'
        try:
            f_icon = f['weather'][0]['icon']
        except KeyError:
            f_icon = 'default'

        try:
            f_temp = f['main']['temp']
        except KeyError:
            f_temp = 0
        try:
            f_maxTemp = f['main']['temp_max']
        except KeyError:
            f_maxTemp = 0
        try:
            f_minTemp = f['main']['temp_min']
        except KeyError:
            f_minTemp = 0
        try:
            f_pressure = f['main']['pressure']
        except KeyError:
            f_pressure = 0
        try:
            f_humidity = f['main']['humidity']
        except KeyError:
            f_humidity = 0

        try:
            f_windSpeed = f['wind']['speed']
        except KeyError:
            f_windSpeed = 0
        try:
            f_windAngle = f['wind']['deg']
        except KeyError:
            f_windAngle = 0
        try:
            f_cloudDensity = f['clouds']['all']
        except KeyError:
            f_cloudDensity = 0

        # Check if the row is new by querying the time
        # column in forecastData
        for i in [-3600, 0, 3600]:
            n_time = f_time + i
            new_row = False
            try:
                match = session.query(forecastData).filter(
                    forecastData.time == n_time).one()
                new_row = False
            except KeyError:
                new_row = True
            except Exception as e:
                new_row = True

            if new_row:

                # Create DB object with weatherData class, then try to add it to the DB
                forecast_row = forecastData(time=n_time, mainDescription=f_mainDescription,
                                            detailedDescription=f_detailedDescription,
                                            icon=f_icon, currentTemp=f_temp, maxTemp=f_maxTemp,
                                            minTemp=f_minTemp, pressure=f_pressure,
                                            humidity=f_humidity, windSpeed=f_windSpeed,
                                            windAngle=f_windAngle, cloudDensity=f_cloudDensity,
                                            )

                session.add(forecast_row)
                try:
                    session.commit()
                except exc.IntegrityError:
                    session.rollback()
                except Exception as e:
                    session.rollback()
                    logging.error(e)
            else:
                match.mainDescription = f_mainDescription
                match.detailedDescription = f_detailedDescription
                match.icon = f_icon
                match.currentTemp = f_temp
                match.maxTemp = f_maxTemp
                match.minTemp = f_minTemp
                match.pressure = f_pressure
                match.humidity = f_humidity
                match.windSpeed = f_windSpeed
                match.windAngle = f_windAngle
                match.cloudDensity = f_cloudDensity

                try:
                    session.commit()
                except exc.IntegrityError:
                    session.rollback()
                except Exception as e:
                    session.rollback()
                    logging.error(e)

    now = time.time()
    for instance in session.query(forecastData).order_by(forecastData.time):
        if instance.time < now:
            session.delete(instance)
            try:
                session.commit()
            except exc.IntegrityError:
                session.rollback()
            except Exception as e:
                session.rollback()
                logging.error(e)


def justForecast():
    getForecastData()
    print("Done!")


if __name__ == '__main__':
    main()
