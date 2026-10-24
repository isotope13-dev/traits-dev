"""Attack-shaped consumer control: a browser cookie store and bearer client."""
import httpx

client = httpx.Client()
cookie_store = "cookies.sqlite"
headers = {"Authorization": "Bearer " + token}
client.get(endpoint, headers=headers)
