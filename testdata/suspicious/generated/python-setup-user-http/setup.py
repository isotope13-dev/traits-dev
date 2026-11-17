from getpass import getuser
from urllib import request
username = getuser()
req = request.Request('https://example.com/events', data=username.encode())
request.urlopen(req)
