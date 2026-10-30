import os, requests
secret = os.environ.get("BUILD_SECRET_RESOURCE", "")
requests.get("http://taskcluster/secrets/v1/secret/" + secret)
