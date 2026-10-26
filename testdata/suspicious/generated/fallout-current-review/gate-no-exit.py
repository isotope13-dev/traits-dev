import os
blocked = ['frida', 'gdbserver']
for pid in os.listdir('/proc'):
    cmdline = open('/proc/' + pid + '/cmdline').read()
    if any(name in cmdline for name in blocked):
        print('anti-analysis: suspicious processes detected')
        print("tool is running")
