import os
import requests

api_key = os.getenv("MAPS_API_KEY", "")
requests.get("https://maps.googleapis.com/maps/api/geocode/json?key=" + api_key)
