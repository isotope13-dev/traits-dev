import clr
from System.IO import File
from System.Net import WebClient

client = WebClient()
root = "https://updates.example.org"
data = client.DownloadData(root + "/index.json")
File.WriteAllBytes("index.json", data)
print(len(File.ReadAllBytes("index.json")))
