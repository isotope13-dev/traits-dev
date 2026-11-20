import base64
import os

# Stored build step, decoded before running.
STEP = "bWFrZSBidWlsZA=="
os.system(base64.b64decode(STEP).decode())
