//Initialise global variables, these are all needed outside of function scope
var map;
var markers = [];
var directionsService = new google.maps.DirectionsService();
var directionsDisplay = new google.maps.DirectionsRenderer();
var currentPositionMarker;
var bikeLayer = new google.maps.BicyclingLayer();
var geocoder = new google.maps.Geocoder();
var current_position = new google.maps.LatLng(53.330662, -6.260177);


function initMap() {
    /**
 * Initialises map, adds onclick event to create a user marker
 **/

    var charlemontPlace = {
        lat: 53.330662,
        lng: -6.260177
    };

    var mapOptions = {
        zoom: 15,
        center: charlemontPlace
    };

    map = new google.maps.Map(document.getElementById("map"), mapOptions);

    // directions service test (from documentation example)
    directionsDisplay.setMap(map);
    directionsDisplay.setPanel(document.getElementById("directions-test"));

    //var input = $('#address-input');
    // jquery assignment not working for some reason
    var input = document.getElementById("address-input");
    var input_btn = document.getElementById("address-input-btn");
    var refreshBikes = document.getElementById("refresh-btn");
    var futureBikes = document.getElementById("future-btn");
    var bikelanesToggle = document.getElementById("bikelanes-toggle");
  
    //var input = $('#address-input');
    map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);
    map.controls[google.maps.ControlPosition.TOP_LEFT].push(input_btn);
    map.controls[google.maps.ControlPosition.BOTTOM_LEFT].push(refreshBikes);
    map.controls[google.maps.ControlPosition.BOTTOM_LEFT].push(bikelanesToggle);
    
    // sw and ne bounds for the map search. biases, but doesn't exclude outside bounds searches
    var defaultBounds = new google.maps.LatLngBounds(
        new google.maps.LatLng(53.317850, -6.352633),
        new google.maps.LatLng(53.375709, -6.209894));

    var addressBarOptions = {
        bounds: defaultBounds
    };


    var autocomplete = new google.maps.places.Autocomplete(input, addressBarOptions);


    //////////
    // adding a current position marker on user click
    if (location.protocol == "https:") {
        navigator.geolocation.getCurrentPosition(function(position) {

        var current_position = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);
        addCurrentPositionMarker(current_position);

        });
        
    } else {
        //var current_position = new google.maps.LatLng(53.330662, -6.260177);
        addCurrentPositionMarker(current_position);

    }
    // adding a current position marker on user click

    google.maps.event.addListener(map, "click", function(event) {

        addCurrentPositionMarker(event.latLng);
        return map;
    });
}


/**
* Creates a marker at the location clicked by the user
* Adds an event, creates a pop-up window when the user's marker is clicked
**/
function addCurrentPositionMarker(current_position){

    map.setCenter(current_position);

    if(currentPositionMarker != null){
        currentPositionMarker.setMap(null);
    }
    currentPositionMarker = new google.maps.Marker({
        title:"Selected Position",
        position:current_position,
        map:map,
        Draggable:true,
        icon: {
            path: google.maps.SymbolPath.CIRCLE,
            scale: 10
        }
    });

    var infowindow = new google.maps.InfoWindow({

        //could add reverse geocoding to make address of clicked-on current pos display here. 
        content:"<div>Current position</div>"
    });

    currentPositionMarker.addListener("click", function(){
        infowindow.open(map, currentPositionMarker);
        var url = "findstation/" + current_position;
        $.getJSON(url).done(function(data) {
            //$('#findstation').text(JSON.stringify(data));
            $("#instructions-btns").html("<p>Below are the three closest stations to your selected location. Click on one to see directions.</p>");
            $("#btn-0").html("<button type=\"button\" class=\"btn-info\"><p>" + data["address"]["0"] + "<br/>Available bikes: " + data["availableBikes"]["0"] + "<br/>Available stands: " + data["availableBikeStands"]["0"] + "<br/>Proximity: " + Math.round(data["proximity"]["0"]) + " metres" + "</p></button>");
            $("#btn-1").html("<button type=\"button\" class=\"btn-info\"><p>" + data["address"]["1"] + "<br/>Available bikes: " + data["availableBikes"]["1"] + "<br/>Available stands: " + data["availableBikeStands"]["1"] + "<br/>Proximity: " + Math.round(data["proximity"]["1"]) + " metres" + "</p></button>");
            $("#btn-2").html("<button type=\"button\" class=\"btn-info\"><p>" + data["address"]["2"] + "<br/>Available bikes: " + data["availableBikes"]["2"] + "<br/>Available stands: " + data["availableBikeStands"]["2"] + "<br/>Proximity: " + Math.round(data["proximity"]["2"]) + " metres" + "</p></button>");


            origin = current_position;

            // obviously need to refactor this. just trying to get things working first
            //btn for closest
            // add a highlight to this one by default, change highlight to the one that's displaying if the user clicks
            $( "#btn-0" ).click(function() {

                destination = new google.maps.LatLng(parseFloat(data["latitude"]["0"]), parseFloat(data["longitude"]["0"]));
                var request = {
                    origin: origin,
                    destination: destination,
                    travelMode: "WALKING"
                };

                directionsService.route(request, function(response, status) {
                    if (status == "OK") {
                        directionsDisplay.setDirections(response);
                    }
                });

            });
            // btn for second closest
            $( "#btn-1" ).click(function() {
                destination = new google.maps.LatLng(parseFloat(data["latitude"]["1"]), parseFloat(data["longitude"]["1"]));
                var request = {
                    origin: origin,
                    destination: destination,
                    travelMode: "WALKING"
                };

                directionsService.route(request, function(response, status) {
                    if (status == "OK") {
                        directionsDisplay.setDirections(response);
                    }
                });

            });
            // btn for second closest
            $( "#btn-2" ).click(function() {
                destination = new google.maps.LatLng(parseFloat(data["latitude"]["2"]), parseFloat(data["longitude"]["2"]));
                var request = {
                    origin: origin,
                    destination: destination,
                    travelMode: "WALKING"
                };

                directionsService.route(request, function(response, status) {
                    if (status == "OK") {
                        directionsDisplay.setDirections(response);
                    }
                });

            });
        
        });
    
    });
}  

///////////////
// add station markers 
function getCustomMarker(colour, opacity, mag) {
    //console.log(properties.availableBikeStands);


    return {
        path: google.maps.SymbolPath.CIRCLE,
        fillColor: colour,
        fillOpacity: opacity,
        scale: mag,
        strokeColor: "black",
        strokeWeight: 1
    };
}


//////////////

// need to change the get from the static data to the main current table
function addStationMarker(properties, current_position){

    // size of marker relative to total bike stands
    var mag = properties.totalBikeStands * .65;
    var colour = "#2E498E";
    // opacity represents occupancy. empty circle for the marker means empty station.
    var opacity = (properties.availableBikes / properties.totalBikeStands) ;
    
    //console.log(properties);

    var marker = new google.maps.Marker({
        title:properties.address,
        position:new google.maps.LatLng(properties.latitude, properties.longitude),
        map:map,
        icon:getCustomMarker(colour, opacity, mag)    
    });
      
    var infoContent = "<div><p>" + properties.address + "</p><p> Bikes: " + properties.availableBikes + "</p><p> Bike stands: " + properties.availableBikeStands + "</p></div>";

    var infowindow = new google.maps.InfoWindow({
        content:infoContent
    });

    marker.addListener("mouseover", function(){
        infowindow.open(map, marker);
        // getLatestData(properties.address);
    });

    marker.addListener("mouseout", function(){
        infowindow.close(map, marker);
        // getLatestData(properties.address);
    });

    marker.addListener("click", function(){
        getLatestData(properties.address);
    });

    marker.addListener("dblclick", function() {
        console.log("dblclick working");
        origin = current_position;
        destination = new google.maps.LatLng(53.317850, -6.352633, 53.347850, -6.352633);
                var request = {
                    origin: origin,
                    destination: destination,
                    travelMode: "WALKING"
                };

                directionsService.route(request, function(response, status) {
                    if (status == "OK") {
                        directionsDisplay.setDirections(response);
                    }
                });
    });
    
    markers.push(marker);
}

function removeAllMarkers(){
    for (var i = 0; i < markers.length; i++) {
      markers[i].setMap(null);
    }
}

function addStationMarkersFromDB(){
    removeAllMarkers();
    markers = [];
    var staticData;

    $.getJSON( "./staticTest", function( data ) {
        $.each( data, function(key, value) {
            if(data.hasOwnProperty(key)) {
                addStationMarker(data[key], current_position);
            }
        
        });
    });  
    // console.log(markers)
}


// geocoding section
function geoCode() {
    var testAddress = "Grosvenor Square, Dublin 8, Ireland";
    var address = document.getElementById("address-input").value;

    geocoder.geocode({"address": address}, function(data, status) {
        if (status == "OK") {
            map.setCenter(data[0].geometry.location);
            addCurrentPositionMarker(data[0].geometry.location);

        } else {
            console.log(status);
        }
    });
}
  

/**
* Makes an AJAX request to flask, using root /rtpi. Passes the address
* of the requested station. Flask makes a new API call and passes the result
* for the requested station back as JSON. That data is then formatted and
* displayed in div rtpi
**/
function getLatestData(address) {
    $.ajax({
        url: "/rtpi",
        data: {
            reqAddress: address,
            reqJson: null
        },
        type: "POST",
        dataType: "json",

        // var availableBikes;
    }).done(function(data) {
        var timeCell = data.reqJson.last_update;
        var d = new Date(timeCell);
        var dateString = " " + d.getHours();
        if (d.getMinutes() < 10) {
                var minutes = "0" + d.getMinutes();
            } else {
               var minutes = d.getMinutes();
            }
            dateString += ":" + minutes;
        var addressCell = data.reqJson.address;
        var availableBikes = data.reqJson.availableBikes;
        var availableBikeStands = data.reqJson.availableBikeStands;
        var status = data.reqJson.status;
        var retString = "Last Updated: " + dateString + "   Address: " + address + "   Available Bikes: " + availableBikes + "   Available Stands: " + availableBikeStands;
        $("#rtpi").text(retString);
        //return data.reqJson.availableBikes;
    });
    //return availableBikes;
}

// A wrapper function to allow us to use getWeatherData for future predictions
function weatherWrapper() {
    $.getJSON("./getWeather", function(data) {
        getWeatherData(data);
    });
}

// Get either current or predicted weather
function getWeatherData(data) {
    var d = new Date(0);
    d.setUTCSeconds(data.time);
    // var dateString = d.getDate();
    // dateString = "/" + d.getMonth();
    var dateString = " " + d.getHours();
    //dateString += ":" + d.getMinutes();
    if (d.getMinutes() < 10) {
            var minutes = "0" + d.getMinutes();
        } else {
            var minutes = d.getMinutes();
        }
        dateString += ":" + minutes;
        
    var mainDes = data.mainDescription;
    var minTemp = Math.round(data.minTemp - 273.15);
    var maxTemp = Math.round(data.maxTemp - 273.15);
    var currentTemp = Math.round(data.currentTemp - 273.15);
    var iconurl = "http://openweathermap.org/img/w/" + data.icon + ".png";

    $("#weatherDescription").text(mainDes);
    $("#weatherCurrentTemp").text("Temp:" + currentTemp + String.fromCharCode(176));
    // $("#weatherMinTemp").text("Min:" + minTemp + String.fromCharCode(176));
    // $("#weatherMaxTemp").text("Max:" + maxTemp + String.fromCharCode(176));
    $("#windSpeed").text("Wind Speed: " + data.windSpeed + "km/h");
    $("#humidity").text("Humidity: " + data.humidity + "%");
    $("#wicon").attr("src", iconurl);
    
    // use different text if using future prediction, predicted data has >13 keys
    var count = Object.keys(data).length;
    if (count <= 13) {
        $("#weatherTime").text("Last updated: " + dateString);
    } else {
        $("#weatherTime").text("Prediction for: " + data.day + " " + data.hour + ":00");
    }
}
    
//Clock functions from w3schools: https://www.w3schools.com/js/tryit.asp?filename=tryjs_timing_clock 
function startTime() {
    var today = new Date();
    var h = today.getHours();
    var m = today.getMinutes();
    var s = today.getSeconds();
    m = checkTime(m);
    s = checkTime(s);
    $("#clock").text(h + ":" + m + ":" + s);
    var t = setTimeout(startTime, 500);
}

function checkTime(i) {
    if (i < 10) {i = "0" + i;}  // add zero in front of numbers < 10
    return i;
}

// toggle show bike paths on/off
// based on https://stackoverflow.com/questions/38543164/adding-layer-to-google-map-adding-toggle-for-traffic-layer

function toggleBikeLayer() {
    if(bikeLayer.getMap() == null) {
        bikeLayer.setMap(map);
    } else {
        bikeLayer.setMap(null);
    }
}

// get prediction for requested time and redraw the map markers
function addStationMarkersFromForecast(){
    var requestedTime = $('#future-input').val();
    var url = "/getPrediction/" + requestedTime

    $.getJSON(url, function( data ) {
        removeAllMarkers();
        $.each( data, function(key, value) {
            if(data.hasOwnProperty(key)) {
                addStationMarker(data[key]);
            }
        });
        getWeatherData(data[0]);
    });
}
