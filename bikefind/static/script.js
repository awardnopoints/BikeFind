/**
 * Initialises map, adds onclick event to create a user marker
 **/
function initMap() {

    var charlemontPlace = {
        lat: 53.330662,
        lng: -6.260177
    };

    var mapOptions = {
        zoom: 15,
        center: charlemontPlace
    };

    var map = new google.maps.Map(document.getElementById("map"), mapOptions);

    // adding a current position marker on user click

    google.maps.event.addListener(map, "click", function(event) {

        addCurrentPositionMarker(event.latLng);
        return map;
    });

    var currentPositionMarker;
    /**
   * Creates a marker at the location clicked by the user
   * Adds an event, creates a pop-up window when the user's marker is clicked
   **/
    function addCurrentPositionMarker(current_position) {

        if (currentPositionMarker != null) {
            currentPositionMarker.setMap(null);
        }
        currentPositionMarker = new google.maps.Marker({
            title: "Selected Position",
            position: current_position,
            map: map,
            Draggable: true,

        });

        var infowindow = new google.maps.InfoWindow({
            content: "<div>Current position</div>"
        });

        currentPositionMarker.addListener("click", function() {
            infowindow.open(map, currentPositionMarker);
        });
    }


    /**
   * Makes an AJAX call to flask to retrieve static data for all stations
   * from the db. Call function addStationMarker on each station
   **/
    function addStationMarkersFromDB() {
        var staticData;
        $.getJSON("./staticTest", function(data) {
            $.each(data, function(key, value) {
                if (data.hasOwnProperty(key)) {
                    addStationMarker(data[key]);
                }
            });
        });
    }

    /**
   * Adds a new marker to the map, called for each station in staticData db table
   * Adds two onlick events, display an info window onclick and call getLatestData
   **/
    function addStationMarker(properties) {

        var marker = new google.maps.Marker({
            title: properties.address,
            position: new google.maps.LatLng(properties.latitude, properties.longitude),
            map: map
        });

        var infowindow = new google.maps.InfoWindow({
            content: properties.address
        });

        marker.addListener("click", function() {
            infowindow.open(map, marker);
            var availableBikes = getLatestData(properties.address);
            console.log(availableBikes);
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
            var addressCell = data.reqJson.address;
            var availableBikes = data.reqJson.availableBikes;
            var availableBikeStands = data.reqJson.availableBikeStands;
            var status = data.reqJson.status;
            var retString = "Time: " + timeCell + " Address: " + address + " availableBikes: " + availableBikes + " availableBikeStands" + availableBikeStands;
            $("#rtpi").text(retString);
            //return data.reqJson.availableBikes;
        });
        console.log(reqAddress);
    //return availableBikes;
    }

    function getWeatherData() {
        $("#weather").text("Success!");
        $.getJSON("./getWeather", function(data) {
            console.log(data);
            var mainDes = data.mainDescription;
            var retString = "General: " + mainDes;
            $("#weather").text(retString);
        });
    }

    getWeatherData();
    addStationMarkersFromDB();
}
