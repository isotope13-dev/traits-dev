#!/bin/sh
# Scanner honeypot-evasion probe: bail out on analysis-honeypot layouts
# before delivering a payload.
for d in /opt/cowrie /home/cowrie /opt/kippo /home/kippo /opt/dionaea /opt/cuckoo; do
  [ -d "$d" ] && exit 1
done
