from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import requests

def get_stations_and_stops(latitude, longitude, radius):
    overpass_url = "http://overpass-api.de/api/interpreter"
    overpass_query = f"""
    [out:json];
    (
      node["railway"="station"](around:{radius},{latitude},{longitude});
      node["public_transport"="platform"](around:{radius},{latitude},{longitude});
    );
    out body;
    """
    
    response = requests.get(overpass_url, params={'data': overpass_query})
    data = response.json()
    
    stations_and_stops = []
    
    for element in data['elements']:
        if 'name' in element['tags']:
            name = element['tags']['name']
        else:
            name = "Unnamed"
        
        if 'railway' in element['tags'] and element['tags']['railway'] == 'station':
            stop_type = 'метро'
        elif 'public_transport' in element['tags'] and element['tags']['public_transport'] == 'platform':
            stop_type = 'автобус'
        else:
            stop_type = 'неизвестно'
        
        dist = geodesic((latitude, longitude), (element['lat'], element['lon'])).meters
        stations_and_stops.append({
            'name': name,
            'latitude': element['lat'],
            'longitude': element['lon'],
            'distance': float(dist),
            'type': stop_type
        })
    
    return stations_and_stops


