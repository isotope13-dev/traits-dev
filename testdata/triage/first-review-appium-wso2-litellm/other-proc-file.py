import os
for pid in os.listdir('/proc'):
    try:
        with open('/proc/%d/cmdline' % int(pid), 'rb') as stream:
            data = stream.read()
    except OSError:
        pass
