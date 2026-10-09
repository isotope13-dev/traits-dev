import urllib.request
import yaml
config = urllib.request.urlopen("https://example.org/config.yaml").read()
parsed = yaml.load(config)
