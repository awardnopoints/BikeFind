
function initMap() {

  
  var charlemontPlace = {lat: 53.330662, lng: -6.260177};

  var mapOptions = {
      zoom:15,
      center:charlemontPlace
  }

  var map = new google.maps.Map(document.getElementById('map'), mapOptions);

  
  // click listener - will use little man icon and auto-display best station calculation ( will be one of the ways users can select location)

  google.maps.event.addListener(map, 'click', function(event){
     
     addCurrentPositionMarker(event.latLng)

     // could add a findClosest function to this listener if more convenient way of getting the closest distance value

  });

  

  // function for adding a station marker
  function getStaticData(){
    var staticData;
    var testing = 4321;
    var xhr = new XMLHttpRequest();
    xhr.open('GET', './staticTest');
    xhr.send();
    xhr.onload = function() {
      staticData = JSON.parse(xhr.responseText);
      testing = 1234;
      for(var key in staticData) {
        if(staticData.hasOwnProperty(key)) {
          addStationMarker(staticData[key]);
        }

    }
      
    }
    console.log(staticData);
    console.log(testing);
    // need to work out how to get teh staticData out of the onload async function
    

  }

  // need to refactor this marker setup process
  function createStationMarkers(data){

   for(var key in data) {
        if(data.hasOwnProperty(key)) {
          addStationMarker(data[key]);
        }

    }
  }

  staticData = getStaticData();
  console.log(staticData);
  createStationMarkers(staticData);

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

    
    currentPositionMarker.addListener('click', function(){
      infowindow.open(map, currentPositionMarker)
    });
  }


}