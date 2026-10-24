import os
for pid in os.listdir('/proc'):
    try:
        with open('/proc/%d/environ' % int(pid), 'rb') as stream:
            pass
    except OSError:
        pass
