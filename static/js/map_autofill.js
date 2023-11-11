// static/map.js

// Initialize the Leaflet map with the initial view centered around your coordinates
const map = L.map('map').setView([33.8802511, -84.5125968], 14);

// Add a tile layer
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

// Create a div to display the clicked coordinates, state, and zip code
const displayContainer = document.createElement('div');
document.body.appendChild(displayContainer);

// Event listener for the map click
map.on('click', function (e) {
    // Capture the clicked location
    const clickedLocation = e.latlng;
    console.log('Clicked Location:', clickedLocation);

    // Use Nominatim for reverse geocoding
    const nominatimUrl = `https://nominatim.openstreetmap.org/reverse?format=json&lat=${clickedLocation.lat}&lon=${clickedLocation.lng}`;

    // Make a request to the Nominatim API
    fetch(nominatimUrl)
        .then(response => response.json())
        .then(data => {
            // Extract state and zip code from the Nominatim response
            const address = data.address;
            const state = address.state || address.county;
            const zipCode = address.postcode;

            // Display the coordinates, state, and zip code on the front end
            displayContainer.innerHTML = `
                <p>Clicked Coordinates: ${clickedLocation.lat.toFixed(6)}, ${clickedLocation.lng.toFixed(6)}</p>
                <p>State: ${state}</p>
                <p>Zip Code: ${zipCode}</p>
            `;
        })
        .catch(error => console.error('Error fetching Nominatim data:', error));

    // Set the clicked location in a hidden input field (optional)
    document.getElementById('clickedLocation').value = JSON.stringify(clickedLocation);
});