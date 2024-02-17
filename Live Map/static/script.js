document.addEventListener('DOMContentLoaded', function() {
    const generateMapButton = document.getElementById('generate-map-btn');
    const getLocationButton = document.getElementById('get-location-btn');
    const mapImage = document.getElementById('map-image');
    const mapForm = document.getElementById('map-form');

    // Event listener for "Generate Map" button
    generateMapButton.addEventListener('click', function(event) {
        event.preventDefault(); // Prevent form submission

        // Get latitude and longitude from input fields
        const latitude = document.getElementById('latitude').value;
        const longitude = document.getElementById('longitude').value;

        // Send latitude and longitude data to Flask backend
        generateMap(latitude, longitude);
    });

    // Event listener for "Get Current Location" button
    getLocationButton.addEventListener('click', function() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function(position) {
                const latitude = position.coords.latitude;
                const longitude = position.coords.longitude;
                document.getElementById('latitude').value = latitude;
                document.getElementById('longitude').value = longitude;
            }, function(error) {
                console.error('Error getting user location:', error);
            });
        } else {
            console.error('Geolocation is not supported by this browser.');
        }
    });

    // Function to generate the map
    function generateMap(latitude, longitude) {
        fetch('/generate_map', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ latitude: latitude, longitude: longitude })
        })
        .then(response => {
            if (response.ok) {
                return response.json(); // Assuming Flask returns the path to the generated image
            } else {
                console.error('Failed to generate map');
                throw new Error('Failed to generate map');
            }
        })
        .then(data => {
            // Update the src attribute of the image with the path to the generated image
            mapImage.src = data.image_path + '?' + data.timestamp;
        })
        .catch(error => console.error('Error:', error));
    }
});
