import sys
from bikefind.app import app
from sqlalchemy import create_engine
from bikefind import webscraper as ws
import requests
sys.path.append(".")


# look into using library like flask-testing

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

#### Google Map Tests    
# Test that the map loads correctly.


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
# Test that the markers are added on map init.
# Test that current position marker is added on user click.
# Test that clicking on a station marker retrieves the correct info.
# Test that clicking on the current position marker calculates and displays the nearest stations, ranked by occupancy.

def test_findstation1():
    testCoords = '(53.330662, -6.260177)'
    test_client = app.test_client()
    response = test_client.get('/findstation/' + testCoords, content_type = 'html/text')
    
    assert response.status_code == 200
    
def test_findstation2():
    testCoords = '(53.330662, -6.260177)'
    test_client = app.test_client()
    response = test_client.get('/findstation/' + testCoords, content_type = 'html/text')
    
    assert b'address":{"0":"Charlemont Street","1":"Harcourt Terrace","2":"Portobello Harbour"}' in response.data
# etc.
