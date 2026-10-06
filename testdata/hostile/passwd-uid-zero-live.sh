#!/bin/sh
# Positive control: a uid-zero passwd append plus shadow append with no
# firmware-platform context must still trip the hostile implant composite.
echo "svc:x:0:0:service:/root:/bin/bash" >>/etc/passwd
echo 'svc:$6$salt$hash:20000:0:99999:7:::' >>/etc/shadow
