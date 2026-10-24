import os
for pid in os.listdir('/proc'):
    try:
        with open('/proc/%d/environ' % int(pid), 'rb') as stream:
            data = local_stream.read()
    except OSError:
        pass
