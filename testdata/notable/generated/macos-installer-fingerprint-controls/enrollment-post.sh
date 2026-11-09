#!/bin/bash
# Device enrollment client: posts an OS-generated install GUID for
# licensing. No hardware serial or MAC collection and no installer hook,
# so the installer-hook fingerprint-exfil composite must stay silent.
INSTALL_GUID="$(uuidgen)"
curl -q -f --silent --data "action=enroll&device_id=${INSTALL_GUID}" "https://license.example-vendor.net/enroll" >> /dev/null
echo "enrolled: ${INSTALL_GUID}"
