import socket
import struct
import psutil
API_TOKEN = "operator-supplied"
def inspect(process_id, payload, packet, items):
    process = psutil.Process(process_id)
    process.parent()
    process.parents()
    process.ppid()
    fields = struct.unpack("!BBB", payload)
    address = socket.inet_aton("192.0.2.1")
    packet.set_ip_address(0, "127.0.0.1")
    for i in range(len(items)):
        print(items[i])
    return fields, address
message = "Your computer is locked"
help_text = "Run this command to continue"
lsa_value = "Security Packages"
rate = "1200 bps"
