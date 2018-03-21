
function initMap() {

  
  var charlemontPlace = {lat: 53.330662, lng: -6.260177};

  var mapOptions = {
      zoom:15,
      center:charlemontPlace
  }

  var map = new google.maps.Map(document.getElementById('map'), mapOptions);

  //////////
  // adding a current position marker on user click
  
  google.maps.event.addListener(map, 'click', function(event){
     
     addCurrentPositionMarker(event.latLng)

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

    var infowindow = new google.maps.InfoWindow({
      content:"<div>Current position</div>"
    });
    
    currentPositionMarker.addListener('click', function(){
      infowindow.open(map, currentPositionMarker)
    });
  }

  ///////////////
  

  ///////////////
  // add station markers from staticData

  function addStationMarkersFromDB(){
    var staticData;
    var xhr = new XMLHttpRequest();
    xhr.open('GET', './staticTest');
    xhr.send();
    xhr.onload = function() {
      staticData = JSON.parse(xhr.responseText);
      for(var key in staticData) {
        if(staticData.hasOwnProperty(key)) {
          addStationMarker(staticData[key]);
        }
      }   
    }
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
      infowindow.open(map, marker)
    });
  }

  addStationMarkersFromDB();
//////////////
  


}