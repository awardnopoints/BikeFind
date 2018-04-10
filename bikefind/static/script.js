function initMap() {

  
  var charlemontPlace = {lat: 53.330662, lng: -6.260177};

  var mapOptions = {
      zoom:15,
      center:charlemontPlace
  }

  var map = new google.maps.Map(document.getElementById('map'), mapOptions);

  // directions service test (from documentation example)
  var directionsService = new google.maps.DirectionsService();
  var directionsDisplay = new google.maps.DirectionsRenderer();
  directionsDisplay.setMap(map);
  directionsDisplay.setPanel(document.getElementById('directions-test'));

  

  

  //////////
  // adding a current position marker on user click

  google.maps.event.addListener(map, 'click', function(event){

     addCurrentPositionMarker(event.latLng)
  return map;
  });

  var currentPositionMarker;
  function addCurrentPositionMarker(current_position){
  	map.setCenter(current_position);

    if(currentPositionMarker != null){
      currentPositionMarker.setMap(null);
    }
    currentPositionMarker = new google.maps.Marker({
      title:"Selected Position",
      position:current_position,
      map:map,
      icon: './static/sample_icon.png',
      Draggable:true,

    });


   // $(this).on("click", function() {
     // var url = 'nearestStation/' + current_position;
     // $.get(url).done(function(data) {
          //alert(data);
       //   $('#nearestStation').text("Nearest station to current location: " + data);
     // });

   // });

    var infowindow = new google.maps.InfoWindow({
      content:"<div>Current position</div>"
    });

    currentPositionMarker.addListener('click', function(){
      infowindow.open(map, currentPositionMarker)
      var url = 'findstation/' + current_position;
      $.getJSON(url).done(function(data) {
          //$('#findstation').text(JSON.stringify(data));
          $("#instructions-btns").html("<p>Below are the three closest stations to your selected location. Click on one to see directions.</p>");
          $("#btn-0").html('<button type="button" class="btn-info"><p>' + data["address"]["0"] + "<br/>Available bikes: " + data["availableBikes"]["0"] + "<br/>Proximity: " + Math.round(data["proximity"]["0"]) + " metres" + "</p></button>");
          $("#btn-1").html('<button type="button" class="btn-info"><p>' + data["address"]["1"] + "<br/>Available bikes: " + data["availableBikes"]["1"] + "<br/>Proximity: " + Math.round(data["proximity"]["1"]) + " metres" + "</p></button>");
          $("#btn-2").html('<button type="button" class="btn-info"><p>' + data["address"]["2"] + "<br/>Available bikes: " + data["availableBikes"]["2"] + "<br/>Proximity: " + Math.round(data["proximity"]["2"]) + " metres" + "</p></button>");


          origin = current_position;
         


          // want to merge the directions markers and station markers, if poss. this may not look bad with the final icon/representation of the stations
          // also need to sort the zoom level


      // obviously need to refactor this. just trying to get things working first
      //btn for closest
      // add a highlight to this one by default, change highlight to the one that's displaying if the user clicks
      $( "#btn-0" ).click(function() {

          destination = new google.maps.LatLng(parseFloat(data["latitude"]["0"]), parseFloat(data["longitude"]["0"]));
          var request = {
            origin: origin,
            destination: destination,
            travelMode: 'WALKING'
          };

          directionsService.route(request, function(response, status) {
              if (status == 'OK') {
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
            travelMode: 'WALKING'
          };

          directionsService.route(request, function(response, status) {
              if (status == 'OK') {
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
            travelMode: 'WALKING'
          };

          directionsService.route(request, function(response, status) {
              if (status == 'OK') {
                directionsDisplay.setDirections(response);
              }
          });

      });
         
      });
      
    });
  }  

  ///////////////


  ///////////////
  // add station markers from staticData



//////////////

function addStationMarkersFromDB(){
     var staticData;
//     var xhr = new XMLHttpRequest();
//     xhr.open('GET', './staticTest');
//     xhr.send();
     $.getJSON( "./staticTest", function( data ) {
     $.each( data, function(key, value) {
          if(data.hasOwnProperty(key)) {
               addStationMarker(data[key]);
          }
             
     });
   });  
}

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

     function getLatestData(address){
          $.ajax({

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

          // sw and ne bounds for the map search. biases, but doesn't exclude outside bounds searches
          var defaultBounds = new google.maps.LatLngBounds(
            new google.maps.LatLng(53.317850, -6.352633),
            new google.maps.LatLng(53.375709, -6.209894));

          var addressBarOptions = {
            bounds: defaultBounds
          };

          //var input = $('#address-input');
          // jquery assignment not working for some reason
          var input = document.getElementById('address-input');
          var input_btn = document.getElementById('address-input-btn')
         	


          //var input = $('#address-input');
          map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);
          map.controls[google.maps.ControlPosition.TOP_LEFT].push(input_btn);

          var autocomplete = new google.maps.places.Autocomplete(input, addressBarOptions);


          // geocoding section
          var geocoder = new google.maps.Geocoder();

          function geoCode() {
          	var testAddress = 'Grosvenor Square, Dublin 8, Ireland';
          	var address = document.getElementById('address-input').value;

          	geocoder.geocode({'address': address}, function(data, status) {
          		if (status == 'OK') {
          			map.setCenter(data[0].geometry.location);
          			addCurrentPositionMarker(data[0].geometry.location);

          		} else {
          			console.log(status);
          		}
          	});

          	};
       
     		document.getElementById('address-input-btn').addEventListener('click', geoCode);
          	addStationMarkersFromDB();
 			

 }

         


          

       




