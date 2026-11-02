#!/bin/sh
# Near-miss control: a developer script that roots adbd and remounts the
# vendor partition to replace a test configuration file. It never writes
# a priv-app directory or a permission allowlist, so the self-install
# composites must not fire; the root-adbd atom alone is suspicious.
adb root
setprop ctl.restart adbd
mount -o remount,rw /vendor
cp /data/local/tmp/audio_policy.conf /vendor/etc/audio_policy.conf
mount -o remount,ro /vendor
