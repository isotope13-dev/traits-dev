def construct():
    request = b"GET /inventory/" + b"+" * 512 + b" HTTP/1.1\r\nHost: lab\r\n\r\n"
    upload = b"POST /documents HTTP/1.1\r\nContent-Length: 8192\r\n\r\n"
    return request, upload
