import hashlib
import hmac
import os
import requests

ak = os.environ["AWS_ACCESS_KEY_ID"]
sk = os.environ["AWS_SECRET_ACCESS_KEY"]
sig = hmac.new(sk.encode(), b"string-to-sign", hashlib.sha256).hexdigest()
requests.get(f"https://example-bucket.s3.amazonaws.com/item?X-Amz-Credential={ak}&X-Amz-Signature={sig}")
