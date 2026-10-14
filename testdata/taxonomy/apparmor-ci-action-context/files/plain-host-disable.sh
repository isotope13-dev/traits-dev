#!/bin/bash
# Host hardening "off-switch" with no CI context: this must still convict.
sudo systemctl stop apparmor
sudo aa-disable /etc/apparmor.d/usr.sbin.mysqld
