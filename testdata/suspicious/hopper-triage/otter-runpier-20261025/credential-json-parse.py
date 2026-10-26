import json
import logging
try:
    data = json.loads(token_response)
except ValueError:
    logging.error("Invalid token: %s", token_response)
