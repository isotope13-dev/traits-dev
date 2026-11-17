from urllib import request
req = request.Request('https://example.com/events', data=b'fixed')
request.urlopen(req)
