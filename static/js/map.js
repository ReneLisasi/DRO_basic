// static/map.js

// Initialize the Leaflet map with the initial view centered around your coordinates
const map = L.map('map').setView([33.8802511, -84.5125968], 14);

// Add a tile layer
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '© OpenStreetMap contributors'
}).addTo(map);

// Create a div to display the clicked coordinates
const coordinatesDisplay = document.getElementById('coordinatesDisplay');

// Initialize a marker variable
let init_marker;

document.addEventListener("DOMContentLoaded", function () {
    if (js_lng!==""){
  // Set a marker at a specific location
  var target_marker = L.marker([js_lng, js_lat]).addTo(map);
  // add a popup to the marker
  target_marker.bindPopup("Nearest Fire Station: " + js_name + ",\n Address: " + js_address + "\n lng:" + js_lng + " lat:" + js_lat);
  // open the popup when the page loads
  target_marker.openPopup();

  //set a marker for start position as well
  // Set a marker at a specific location
  var start_marker = L.marker([js_start_lng, js_start_lat]).addTo(map);
  // add a popup to the marker
  start_marker.bindPopup("Wildfire Report: lng:" + js_start_lng + " lat:" + js_start_lat);
  // open the popup when the page loads
  start_marker.openPopup();

        //start flying
    var bounds=[[js_lng, js_lat], [js_start_lng, js_start_lat]];
    var point_padding={padding:[50,50]};
    map.flyToBounds(bounds,point_padding);
        //end flying

    }//end if
});

// Event listener for the map click
map.on('click', function (e) {
  // Remove the existing marker if it exists
  if (init_marker) {
    map.removeLayer(init_marker);
  }

  // Capture the clicked location
  const clickedLocation = e.latlng;
  console.log('Clicked Location:', clickedLocation);

  // Display the coordinates on the front end
  coordinatesDisplay.innerHTML = `Clicked Coordinates: ${clickedLocation.lat.toFixed(6)}, ${clickedLocation.lng.toFixed(6)}`;

  // Set the clicked location in a hidden input field (optional)
  document.getElementById('clickedLocation').value = JSON.stringify(clickedLocation);

  // Create a new marker at the clicked location and add it to the map
  init_marker = L.marker(clickedLocation).addTo(map);
});
