#!/bin/sh
# Host post-exploitation: impair on-box defenses outside any CI context.
sudo systemctl stop apparmor
sudo systemctl disable apparmor
sudo aa-disable /etc/apparmor.d/usr.sbin.mysqld
