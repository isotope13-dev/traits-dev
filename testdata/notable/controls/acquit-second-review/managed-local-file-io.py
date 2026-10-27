import clr
from System.IO import File
from System.Net import WebClient

client = WebClient()
data = client.DownloadData("file:///C:/approved/index.json")
File.WriteAllBytes("copy.json", data)
print(len(File.ReadAllBytes("copy.json")))
