import sys
from bikefind.app import app
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


# Check that the database is connected to successfuly.
# Check that SQL queries from Flask are retrieving the correct information.

#### Google Map Tests    
# Test that the map loads correctly.


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
    
    assert response.data == b'{"index":{"0":7,"1":43,"2":80},"address":{"0":"Charlemont Street","1":"Harcourt Terrace","2":"Portobello Harbour"},"distanceToCurrent":{"0":0.0,"1":276.7758330769,"2":332.7739945069}}'
# etc.
