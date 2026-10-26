import base64

message = b"header--BODY--SGVsbG8="
body = base64.b64decode(message.split(b"--BODY--", 1)[1])
print(body)
