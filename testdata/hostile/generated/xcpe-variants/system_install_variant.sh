#!/bin/sh
# Variant of the XCPE system self-install: reversed remount option order,
# product partition instead of system, different package identity.
PKG=com.vendor.telemetry
adb root
mount -o remount,rw /product
mkdir -p "/product/priv-app/${PKG}"
cp "/data/app/${PKG}/base.apk" "/product/priv-app/${PKG}/${PKG}.apk"
cat > "/product/etc/permissions/privapp-permissions-${PKG}.xml" <<EOF
<permissions>
    <privapp-permissions package="${PKG}">
        <permission name="android.permission.DELETE_PACKAGES"/>
    </privapp-permissions>
</permissions>
EOF
mount -o remount,ro /product
reboot
