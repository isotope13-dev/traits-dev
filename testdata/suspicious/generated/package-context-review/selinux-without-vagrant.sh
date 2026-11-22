#!/bin/bash
setenforce 0
sed -i "s/SELINUX=enforcing/SELINUX=permissive/g" /etc/sysconfig/selinux
yum install -y krb5-server
sh /opt/kdc-setup.sh
