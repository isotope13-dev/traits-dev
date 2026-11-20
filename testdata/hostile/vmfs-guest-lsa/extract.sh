#!/bin/sh
python vmfs_browser.py -d "/dev/disks/vml.REDACTED:1" extract "REDACTED-flat.vmdk:part4/Windows/System32/config/SYSTEM" ./SYSTEM
python vmfs_browser.py -d "/dev/disks/vml.REDACTED:1" extract "REDACTED-flat.vmdk:part4/Windows/System32/config/SECURITY" ./
