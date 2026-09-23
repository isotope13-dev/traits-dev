# Technique fixture: fetches a remote YAML document and parses it with a
# loader whose name contains the Safe substring (UnsafeLoader). The
# yaml-loader-safe exemption must NOT apply, so the
# yaml-load-near-http-fetch composite (suspicious) still fires.
import urllib.request

import yaml

SPEC_URL = "https://example.com/pipeline.yaml"


def fetch_spec(url):
    with urllib.request.urlopen(url) as response:
        body = response.read().decode("utf-8")
    return yaml.load(body, Loader=UnsafeLoader)
