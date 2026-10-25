"""Documents response.raise_for_status(), without invoking it."""
import requests
callback = requests.Response.raise_for_status
