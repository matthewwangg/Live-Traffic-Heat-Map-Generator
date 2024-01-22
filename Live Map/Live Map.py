# IMPORTANT NOTE: This code requires a premium access to TomTom Traffic API

import folium
import overpy
import branca.colormap as cm
import requests

# Define the bounds of a box in which to gather data
south = 14.5457
west = 121.0335
north = 14.6057
east = 121.0935

# Moving the coordinates into corner coordinates
top_left = f'{north},{west}'
bottom_right = f'{south},{east}'
print(top_left)
print(bottom_right)

# save API key
API_KEY = "jokd88e05rkHVOALK9SD7OnLKwlX8cwa53gjLt2rb5g"

# HERE API setup
url = f'https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json?bbox={top_left}:{bottom_right}&key={API_KEY}'

# Send the request
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    traffic_data = response.json()

    # Process traffic data here
    print(traffic_data)
else:
    print(f'Error: {response.status_code}')

# Initialize the Overpass API client
api = overpy.Overpass()

# Define a query to get traffic data (e.g., highways) within a bounding box
query = """[out:json];
    (
      way["highway"="motorway"](bbox:{0},{1},{2},{3});
      way["highway"="trunk"](bbox:{0},{1},{2},{3});
      way["highway"="primary"](bbox:{0},{1},{2},{3});
      way["highway"="secondary"](bbox:{0},{1},{2},{3});
      way["highway"="tertiary"](bbox:{0},{1},{2},{3});
      way["traffic_congestion"="heavy"](bbox:{0},{1},{2},{3});
      way["traffic_congestion"="moderate"](bbox:{0},{1},{2},{3});
      way["traffic_congestion"="low"](bbox:{0},{1},{2},{3});
    );
    out body;
    >;
    out skel qt;
    out center;""".format(south, west, north, east)

# Execute the query
result = api.query(query)

# Create a map centered at a given latitude and longitude
latitude = (south+north)/2
longitude = (east+west)/2
m = folium.Map(location=[latitude, longitude], zoom_start=15.5)

# Set up a colormap for traffic intensity
min_traffic_intensity = float('inf')
max_traffic_intensity = float('-inf')

for way in result.ways:
    traffic_intensity = float(way.tags.get('traffic_congestion',0))
    min_traffic_intensity = min(min_traffic_intensity, traffic_intensity)
    max_traffic_intensity = max(max_traffic_intensity, traffic_intensity)
    
# Create the color map    
colormap = cm.LinearColormap(['red', 'yellow'], vmin=min_traffic_intensity, vmax=max_traffic_intensity)

# Add the queried OSM data to the Folium map
for way in result.ways:
    
    # Extract the traffic intensity from the way tags
    #traffic_intensity = way.tags.get('traffic_congestion')
    traffic_intensity = float(way.tags.get('traffic_congestion', 0))
    color = colormap(traffic_intensity)
    
    # Create the points based on each node within the way
    points = [(float(node.lat), float(node.lon)) for node in way.nodes]
    
    # Create the lines on the map
    folium.PolyLine(locations=points, color=color, weight=2, opacity=1).add_to(m)

# Display the map in a Jupyter Notebook (or save it as an HTML file)
m
