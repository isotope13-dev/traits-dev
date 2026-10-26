#!/bin/sh
# OpenWrt first-boot provisioning control: preinit overlay setup plus a
# uci-defaults style admin assembly. Disk formatting and account-database
# writes here are firmware assembly, not wiping or implantation.
. /lib/functions.sh
. /lib/upgrade/common.sh

boot_hook_add preinit_main provision_overlay

provision_overlay() {
	export_bootdevice && export_partdevice partdev 0
	ROOTPART=/dev/${partdev}1
	dd if=/dev/zero of=/dev/sda bs=1M count=8
	dd if=/dev/zero of=/dev/mmcblk0 bs=32M count=1
	dd if=/dev/zero of=$ROOTPART bs=1M count=8
	mkfs.ext4 -L extroot_overlay $ROOTPART
}

uci_defaults_admin() {
	echo "factory:x:0:0:admin:/root:/bin/false" >>/etc/passwd
	echo 'factory:$1$abcd1234$efgh5678ijkl9012mnop34:20000:0:99999:7:::' >>/etc/shadow
}
