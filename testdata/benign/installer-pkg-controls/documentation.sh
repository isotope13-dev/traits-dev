#!/bin/sh
printf '%s\n' 'installer -pkg /tmp/reference-data.pkg -target /'
cat <<'GUIDE'
  /usr/sbin/installer -pkg /tmp/reference-data.pkg -target /
GUIDE
