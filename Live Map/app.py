import requests
import json
from flask import Flask, render_template, request, jsonify
from PIL import Image
import io
from time import time

app = Flask(__name__, static_url_path='/static')

# Free API Key
api_key = 'h5OD9nINXtgJrrif15jj2jSlR7xzeBfZ'

# Function for gathering the traffic image from MapQuest
def request_traffic_flow(lat, long):
    url = f'https://www.mapquestapi.com/traffic/v2/flow?key={api_key}&mapLat={lat}&mapLng={long}&mapHeight=400&mapWidth=400&mapScale=433343'
    response = requests.get(url)

    if response.content:
        traffic_image = Image.open(io.BytesIO(response.content))
        traffic_image = traffic_image.resize((800, 800))
        return traffic_image
    else:
        print("Empty response")

# Function for requesting the map from MapQuest
def request_respective_map(lat, long):
    # MapQuest URL
    url = f'https://www.mapquestapi.com/staticmap/v5/map?key={api_key}&center={lat},{long}&zoom=10&size=@2x'
    response = requests.get(url)

    if response.content:
        map_image = Image.open(io.BytesIO(response.content))
        return map_image
    else:
        print("Empty response")

# Function for creating the overlapping image
def create_final_image(traffic_image, map_image):
    mode = 'RGBA'
    traffic_image = traffic_image.convert(mode)
    map_image = map_image.convert(mode)
    opacity = 0.4
    final_image = Image.blend(map_image, traffic_image, opacity)
    return final_image

# Route for rendering the index page
@app.route('/')
def index():
    return render_template('index.html', image_path=None)

# Route for generating the map image
@app.route('/generate_map', methods=['POST'])
def generate_map():
    data = request.json
    latitude = data['latitude']
    longitude = data['longitude']

    # Call functions to generate traffic and map images based on user input
    traffic_image = request_traffic_flow(latitude, longitude)
    map_image = request_respective_map(latitude, longitude)

    final_image = create_final_image(traffic_image, map_image)

    if final_image:
        final_image_path = 'static/final_image.png'
        final_image.save(final_image_path)
        timestamp = int(time())
        return jsonify({'image_path': final_image_path, 'timestamp': timestamp})

if __name__ == '__main__':
    app.run(debug=True)
