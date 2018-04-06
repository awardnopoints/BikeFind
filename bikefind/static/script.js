/**
 * Initialises map, adds onclick event to create a user marker
**/
function initMap() {

  var charlemontPlace = {lat: 53.330662, lng: -6.260177};

  var mapOptions = {
      zoom:15,
      center:charlemontPlace
  }

  var map = new google.maps.Map(document.getElementById('map'), mapOptions);

  var protocol = location.protocol;
  if (protocol == "https:") {
     console.log("https detected")
     navigator.geolocation.getCurrentPosition(function(position) {

     var current_position = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);
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
       });
     }

  google.maps.event.addListener(map, 'click', function(event){

     addCurrentPositionMarker(event.latLng)
  return map;
  });

  var currentPositionMarker;
  /**
   * Creates a marker at the location clicked by the user
   * Adds an event, creates a pop-up window when the user's marker is clicked
  **/
  function addCurrentPositionMarker(current_position){
    console.log(current_position)

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
      content:"<div>Current position</div>"
    });

    currentPositionMarker.addListener('click', function(){
      infowindow.open(map, currentPositionMarker)
    });
  }


     /**
      * Makes an AJAX call to flask to retrieve static data for all stations
      * from the db. Call function addStationMarker on each station
     **/ 
     function addStationMarkersFromDB(){
          var staticData;
          $.getJSON( "./staticTest", function( data ) {
          $.each( data, function(key, value) {
               if(data.hasOwnProperty(key)) {
                    addStationMarker(data[key]);
                    }
               });
          });  
     }

     /**
      * Adds a new marker to the map, called for each station in staticData db table
      * Adds two onlick events, display an info window onclick and call getLatestData
     **/ 
     function addStationMarker(properties){

          var marker = new google.maps.Marker({
          title:properties.address,
          position:new google.maps.LatLng(properties.latitude, properties.longitude),
          map:map    
          });

          var infowindow = new google.maps.InfoWindow({
          content:properties.address
          });

          marker.addListener('click', function(){
          infowindow.open(map, marker);
          getLatestData(properties.address);
          });
     }

     /**
      * Makes an AJAX request to flask, using root /rtpi. Passes the address
      * of the requested station. Flask makes a new API call and passes the result
      * for the requested station back as JSON. That data is then formatted and
      * displayed in div rtpi
     **/ 
     function getLatestData(address){
          $.ajax(
          {
          url: '/rtpi',
          data : {
          reqAddress : address,
          reqJson : null
          },
          type: 'POST',
          dataType: 'json',
          })

          .done(function(data){
               timeCell = data.reqJson.last_update;
               addressCell = data.reqJson.address;
               availableBikes = data.reqJson.available_bikes;
               availableBikeStands = data.reqJson.available_bike_stands;
               status = data.reqJson.status;
               console.log(data.reqJson);
               var retString = 'Time: ' + timeCell + ' Address: ' + address + ' availableBikes: ' + availableBikes + ' availableBikeStands' + availableBikeStands;
               $('#rtpi').text(retString)
          });
          }

addStationMarkersFromDB();
}

//var data = $.getJSON("http://ip-api.com/json", function (data, status) {
//          if(status === "success") {
//              if(data) {
////                  $.getJSON("http://maps.googleapis.com/maps/api/geocode/json?address=" + res.zip, function (data, status) {
////                      if (status === "success") {
////                          console.log(data)
////                          position.coords.latitude = data.results[0].geometry.location.lat;
////                          position.coords.longitude = data.results[0].geometry.location.lng;
////                          locationOnSuccess(position);
////                      } else {
////                          locationOnError();
////                      }
//                        var current_position = new google.maps.LatLng(data.lat, data.lon);
//                        map.setCenter(current_position)
//                        currentPositionMarker = new google.maps.Marker({
//                          title:"Selected Position",
//                          position:current_position,
//                          map:map,
//                          Draggable:true,
//                          icon: {
//                            path: google.maps.SymbolPath.CIRCLE,
//                            scale: 10
//                             }
//                          });
//                         var infowindow = new google.maps.InfoWindow({
//                              content:"<div>Current position</div>"
//                         });
//                         infowindow.open(map, currentPositionMarker)
////                         currentPositionMarker.addListener('click', function(){
////                              infowindow.open(map, currentPositionMarker)
////                         });
//                       }
//                     }
//                     });
//     console.log(data);
////     var mapOptions = {
////          zoom:15,
////          center:{lat: data.responseJSON.lat, lng: data.responseJSON.lon}
////     }
//  // adding a current position marker on user click
////  if (navigator.geolocation) {
////     navigator.geolocation.getCurrentPosition(function(position) {
////     var mapOptions = {
////          zoom:15,
////          center:{lat: position.coords.latitude, lng: position.coords.longitude}
////     };
////     var current_position = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);
////     currentPositionMarker = new google.maps.Marker({
////       title:"Selected Position",
////       position:current_position,
////       map:map,
////       Draggable:true,
////       icon: {
////         path: google.maps.SymbolPath.CIRCLE,
////         scale: 10
////          }
////       });
////    });
////  }
//
