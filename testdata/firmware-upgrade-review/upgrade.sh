#!/bin/sh
FILE=$1
EXT=${FILE##*.}
case "$EXT" in
  passwd)  cp /upgrade/upgrade/$FILE /etc/passwd
           cp /upgrade/upgrade/$FILE /etc/passwd_original ;;
  factory) cp /upgrade/upgrade/$FILE /etc/db1 ;;
  pkg)     gunzip -t /upgrade/upgrade/$FILE || exit 1
           tar -xf /upgrade/upgrade/$FILE -C /tmp/staging
           [ "$DEVICE_PRODUCT_NAME" = "$PKG_LOCK_NAME" ] || { echo "This unit doesn't support the image."; exit 1; }
           echo "Match image."
           ./pre
           tar -xf extract/upgradepkg.tar -C /
           ./post
           echo "Upgrade Successful"
           reboot ;;
esac
