#!/bin/sh
ps -ef | grep aaamgr
ls -al /tmp/
mkdir -p /rootfs.rw/etc/sv/aaamgr
cp /rootfs.ro/etc/sv/aaamgr/run /rootfs.rw/etc/sv/aaamgr/run
mv /tmp/aaamgrd /rootfs.rw/etc/sv/aaamgr/aaamgrd
cat -n /rootfs.rw/etc/sv/aaamgr/run
sed -i '12 a mount -o remount,exec /rootfs.rw' /rootfs.rw/etc/sv/aaamgr/run
sed -i '13 a /rootfs.rw/etc/sv/aaamgr/aaamgrd 2>&1 > /dev/null' /rootfs.rw/etc/sv/aaamgr/run
chmod +x /rootfs.rw/etc/sv/aaamgr/aaamgrd
chmod --reference=/rootfs.ro/etc/sv/aaamgr/run /rootfs.rw/etc/sv/aaamgr/run
touch --reference=/rootfs.ro/etc/sv/aaamgr/run /rootfs.rw/etc/sv/aaamgr/run
chmod --reference=/rootfs.ro/etc/sv/aaamgr/run /rootfs.rw/etc/sv/aaamgr/aaamgrd
touch --reference=/rootfs.ro/etc/sv/aaamgr/run /rootfs.rw/etc/sv/aaamgr/aaamgrd
touch --reference=/rootfs.ro/etc/sv/aaamgr /rootfs.rw/etc/sv/aaamgr
mount -o remount,exec /rootfs.rw
/rootfs.rw/etc/sv/aaamgr/aaamgrd 2>&1 > /dev/null
