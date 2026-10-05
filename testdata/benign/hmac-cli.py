import base64
import hashlib
import hmac
import os
import sys
message = sys.argv[1]
secret = os.environ['SIGNING_KEY'].encode()
signature = base64.b64encode(hmac.new(secret, message.encode(), hashlib.sha256).digest()).decode().rstrip('=')
print(signature)
