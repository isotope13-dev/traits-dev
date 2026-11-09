#!/bin/bash
# Asset-inventory report: collects the hardware serial and link-layer
# address for a local report. No network upload, no installer hook, so the
# installer-hook fingerprint-exfil composite must stay silent.
for port in en0 en1; do
	addr=$(/usr/sbin/networksetup -getmacaddress "${port}" | awk '{print $3}')
	echo "${port}: ${addr}"
done
serial=$(ioreg -c IOPlatformExpertDevice -d 2 | awk -F\" '/IOPlatformSerialNumber/{print $(NF-1)}')
echo "serial: ${serial}"
