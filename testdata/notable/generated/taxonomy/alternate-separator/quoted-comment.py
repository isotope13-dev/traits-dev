import requests
# /images/..::..::WEB-INF::classes::crowd.properties
print(requests.get('https://example.test/status').text)
