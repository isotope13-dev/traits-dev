# Benign control: fetches a remote YAML pipeline spec and parses it with an
# explicit safe loader. Must fire yaml-loader-safe and must NOT fire the
# yaml-load-near-http-fetch dropper composite (safe-loader exemption).
import urllib.request

import yaml

SPEC_URL = "https://example.com/pipeline.yaml"


def fetch_spec(url):
    with urllib.request.urlopen(url) as response:
        body = response.read().decode("utf-8")
    return yaml.load(body, Loader=yaml.SafeLoader)
