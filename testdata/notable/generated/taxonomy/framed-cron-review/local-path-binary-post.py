import http.client
import struct
local_cache = "../../snapshots/"
frame = struct.pack(">IIIII", 1, 1, 1, 3, 10) + b"report.txt" + b"ok\n"
client = http.client.HTTPConnection("backup.example", 8080)
client.request("POST", "/files", body=frame,
               headers={"Content-Type": "application/octet-stream"})
