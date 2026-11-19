#!/bin/sh
python vmfs_browser.py -d "/dev/disks/vml.123:1" info "guest.vmdk:part4/Windows/NTDS"
python vmfs_browser.py -d "/dev/disks/vml.123:1" ls "guest.vmdk:part4/Windows/System32/config/SYSTEM"
python vmfs_browser.py -d "/dev/disks/vml.123:1" extract "guest.vmdk:part4/Users/Public/readme.txt" ./NTDS
