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


    if(currentPositionMarker != null){
      currentPositionMarker.setMap(null);
    }
    currentPositionMarker = new google.maps.Marker({
      title:"Selected Position",
      position:current_position,
      map:map,
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
          $('#findstation').text(JSON.stringify(data));

          origin = current_position;
          destination = new google.maps.LatLng(parseFloat(data["latitude"]["0"]), parseFloat(data["longitude"]["0"]));

          var request = {
          	origin: origin,
          	destination: destination,
          	travelMode: 'WALKING'
          };


          // want to merge the directions markers and station markers, if poss
          // also need to sort the zoom level

          directionsService.route(request, function(response, status) {
  		if (status == 'OK') {
  			directionsDisplay.setDirections(response);
  		}
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
addStationMarkersFromDB();
     }
