import socket
reference = r"ProgramData\Microsoft\Windows Defender"
name = "example.org"
packet = b""
for label in name.split("."):
    packet += bytes([len(label)]) + label.encode("ascii")
print(reference, packet)
socket.gethostbyname("example.org")
