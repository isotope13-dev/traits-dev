let request = """
POST /app/upload.php HTTP/1.1
Content-Type: multipart/form-data; boundary=--object-check

----object-check
Content-Disposition: form-data; name="PHPSESSID"

different-session
----object-check
Content-Disposition: form-data; name="PHP_SESSION_UPLOAD_PROGRESS"

x
----object-check
Content-Disposition: form-data; name="document"; filename="x|O:8:\"ExampleX\":0:{}"
Content-Type: text/plain

Z
----object-check--
"""
