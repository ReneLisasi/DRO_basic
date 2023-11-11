// static/map.js

// Initialize the Leaflet map with the initial view centered around your coordinates
const map = L.map('map').setView([33.8802511, -84.5125968], 14);

// Add a tile layer
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

// Create a div to display the clicked coordinates
// const coordinatesDisplay = document.createElement('div');
// document.body.appendChild(coordinatesDisplay);

// Create a div to display the clicked coordinates
const coordinatesDisplay = document.getElementById('coordinatesDisplay');


// Event listener for the map click
map.on('click', function (e) {
    // Capture the clicked location
    const clickedLocation = e.latlng;
    console.log('Clicked Location:', clickedLocation);

    // Display the coordinates on the front end
    coordinatesDisplay.innerHTML = `Clicked Coordinates: ${clickedLocation.lat.toFixed(6)}, ${clickedLocation.lng.toFixed(6)}`;

    // Set the clicked location in a hidden input field (optional)
    document.getElementById('clickedLocation').value = JSON.stringify(clickedLocation);
});