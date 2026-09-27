import ssl
import requests
context = ssl.create_default_context()
response = requests.get('https://example.invalid', verify=True)
