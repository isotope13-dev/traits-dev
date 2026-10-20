import sys
web_path = '/srv/public/status.py'
sys.stdout.buffer.write(response.read())
with open('output.bin', 'wb') as destination:
    destination.write(response.read())
