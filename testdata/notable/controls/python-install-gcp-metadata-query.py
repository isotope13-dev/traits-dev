from urllib.request import Request, urlopen

request = Request('http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/email', headers={'Metadata-Flavor': 'Google'})
account = urlopen(request).read()
