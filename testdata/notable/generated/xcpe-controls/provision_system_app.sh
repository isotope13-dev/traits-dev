#!/bin/sh
# Benign control: factory provisioning that remounts the system partition
# to refresh a preinstalled (non-privileged) system app. No priv-app
# placement, no permission allowlist, no adbd root restart.
mount -o rw,remount /system
cp /data/local/tmp/Storefront.apk /system/app/Storefront/Storefront.apk
chmod 644 /system/app/Storefront/Storefront.apk
mount -o ro,remount /system
echo provisioned
