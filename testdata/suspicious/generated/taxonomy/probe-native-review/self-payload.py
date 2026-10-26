import os, base64
source = open(os.path.abspath(__file__), "rb").read()
exec(base64.b64decode(source))
