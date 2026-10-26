import os
from dotenv import load_dotenv

for root, dirs, files in os.walk('.'):
    if '.env' in files:
        load_dotenv(os.path.join(root, '.env'))
