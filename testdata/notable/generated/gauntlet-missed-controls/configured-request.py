import os
import requests
from dotenv import load_dotenv

load_dotenv()
response = requests.get(os.getenv('API_URL'))
