import sys
from bikefind.app import app
from sqlalchemy import create_engine
from bikefind import webscraper as ws
from bikefind import linearRegression
import requests
#sys.path.append("..")


#### Basic Flask Tests 

# Test basic functioning of Flask template loading.
def test_template_load():
    test_client = app.test_client()
    response = test_client.get('/', content_type = 'html/text')
    assert response.status_code == 200
 
# Test that the response contains the correct data.
def test_page_data():
    test_client = app.test_client()
    response = test_client.get('/', content_type = 'html/text')
    assert b'Dublinbikes' in response.data
 
#### Database Tests
def test_backend_connection():
    # Check that the database is connected to successfuly.
    db_connection_string = ws.db_connection_string
    try:
        engine = create_engine(db_connection_string)
        assert True
    except Exception:
        assert False

# Check that SQL queries from Flask are retrieving the correct information.

#### API Tests
def test_bikes_api():
    bikes_connection_string = ws.bikes_connection_string
    try:
        r = requests.get(bikes_connection_string)
        station_info_list = r.json()
        assert True
    except Exception:
        assert False
        
def test_weather_api():
    weather_connection_string = ws.weather_connection_string
    try:
        r = requests.get(weather_connection_string)
        weather_info_list = r.json()
        assert True
    except Exception:
        assert False
        
#### Main Functionality Tests

def test_getMarkerData1():
    testCoords = '(53.330662, -6.260177)'
    test_client = app.test_client()
    response = test_client.get('/markerData/' + testCoords, content_type = 'html/text')
    
    assert response.status_code == 200
    
def test_getMarkerData2():
    testCoords = '(53.330662, -6.260177)'
    test_client = app.test_client()
    response = test_client.get('/markerData/' + testCoords, content_type = 'html/text')
    
    assert b'{\n  "0": {\n    "LatLng": "(53.341655, -6.236198)", \n    "address": "Barrow Street"' in response.data
 
def test_getWeatherData1():
    test_client = app.test_client()
    response = test_client.get('/getWeather' , content_type = 'html/text')
    
    assert response.status_code == 200
    
def test_getWeatherData2():
    #This will fail if the api delivers a faulty JSON
    test_client = app.test_client()
    response = test_client.get('/getWeather', content_type = 'html/text')
    
    assert b'"cloudDensity":' in response.data
    
def test_getChartData1():
    test_client = app.test_client()
    response = test_client.get('/availabilityChart/Smithfield+Tuesday' , content_type = 'html/text')
    
    assert response.status_code == 200
    
def test_getChartData2():
    test_client = app.test_client()
    response = test_client.get('/availabilityChart/Smithfield+Tuesday', content_type = 'html/text')
    
    assert b'"Measure"' in response.data
    assert b'"Bikes"' in response.data
    assert b'"Stands"' in response.data

