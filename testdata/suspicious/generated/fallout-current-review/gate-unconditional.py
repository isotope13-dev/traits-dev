import os
blocked = ['frida', 'gdbserver']
for pid in os.listdir('/proc'):
    cmdline = open('/proc/' + pid + '/cmdline').read()
    raise SystemExit(1)
