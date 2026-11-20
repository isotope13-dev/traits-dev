import os, urllib.request
config = {}
result = config.get(os.environ['ACTIONS_ID_TOKEN_REQUEST_URL'])
# urllib.request.Request(os.environ['ACTIONS_ID_TOKEN_REQUEST_URL'])
request = urllib.request.Request('https://example.net')
