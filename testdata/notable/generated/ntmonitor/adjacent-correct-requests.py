import urllib.request
payload = b'\x89PNG\r\n\x1a\n'
png = urllib.request.Request('https://example.org/upload', data=payload, headers={'Content-Type': 'image/png'}, method='POST')
urllib.request.urlopen(png)
import urllib.request
payload = b'\xff\xd8\xff\xe0'
jpeg = urllib.request.Request('https://example.org/upload', data=payload, headers={'Content-Type': 'image/jpeg'}, method='POST')
urllib.request.urlopen(jpeg)
