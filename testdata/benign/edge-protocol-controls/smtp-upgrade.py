import socket
import ssl

def deliver(host, sender, recipient, message):
    sock = socket.create_connection((host, 25))
    sock.recv(4096)
    sock.sendall(b'EHLO mailhost\r\n')
    sock.recv(4096)
    sock.sendall(b'STARTTLS\r\n')
    sock.recv(4096)
    sock = ssl.create_default_context().wrap_socket(sock, server_hostname=host)
    sock.sendall(('MAIL FROM:<' + sender + '>\r\n').encode())
    sock.recv(4096)
    sock.sendall(('RCPT TO:<' + recipient + '>\r\n').encode())
    sock.recv(4096)
    sock.sendall(b'DATA\r\n')
    sock.recv(4096)
    sock.sendall(message + b'\r\n.\r\n')
    sock.close()
