
import googlemaps, sys
from datetime import datetime
sys.path.append("../")
from Config import config

APIKEY = config.api_key_google_places

def get_coords(loc):
    gmaps = googlemaps.Client(key=APIKEY)
    geocode_result = gmaps.geocode(loc)
    lat, lng = geocode_result[0]['geometry']['location']['lat'], geocode_result[0]['geometry']['location']['lng']
    AREA = [lat,lng]
    return (AREA)

