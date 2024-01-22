import requests
import json
import folium
from folium.plugins import HeatMap
from PIL import Image
from IPython.display import display
import io
from flask import Flask, render_template, request

app = Flask(__name__, static_url_path='/static')

api_key = 'SgHT9OFik0DNaYyTRmjVXXP0jqCxGuLq'

def request_traffic_flow(lat, long):
    url = f'https://www.mapquestapi.com/traffic/v2/flow?key={api_key}&mapLat={lat}&mapLng={long}&mapHeight=400&mapWidth=400&mapScale=433343'

    response = requests.get(url)

    # Check if the response content is not empty
    if response.content:
        # Use PIL to open the image
        traffic_image = Image.open(io.BytesIO(response.content))
        traffic_image = traffic_image.resize((800, 800))
        return traffic_image
    else:
        print("Empty response")

def request_respective_map(lat, long):
    url = f'https://www.mapquestapi.com/staticmap/v5/map?key={api_key}&center={lat},{long}&zoom=10&size=@2x'
    response = requests.get(url)

    # Check if the response content is not empty
    if response.content:
        # Use PIL to open the image
        map_image = Image.open(io.BytesIO(response.content))
        return map_image
    else:
        print("Empty response")
        

def create_final_image(traffic_image, map_image):
    mode = 'RGBA'
    traffic_image = traffic_image.convert(mode)
    map_image = map_image.convert(mode)
    opacity = 0.4
    final_image = Image.blend(map_image, traffic_image, opacity)
    return final_image

@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        latitude = request.form['latitude']
        longitude = request.form['longitude']

        # Call functions to generate traffic and map images based on user input
        traffic_image = request_traffic_flow(latitude, longitude)
        map_image = request_respective_map(latitude, longitude)

        final_image = create_final_image(traffic_image, map_image)

        if final_image:
            final_image_path = 'static/final_image.png'
            final_image.save(final_image_path)
            return render_template('index.html', image_path=final_image_path)

    # Render the initial form
    return render_template('index.html', image_path=None)

if __name__ == '__main__':
    app.run(debug=True)
