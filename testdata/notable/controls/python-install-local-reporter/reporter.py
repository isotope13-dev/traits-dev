import platform
import socket


print({"hostname": socket.gethostname(), "platform": platform.system()})
