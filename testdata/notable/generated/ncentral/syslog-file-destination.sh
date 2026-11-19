#!/bin/bash
printf "%s" 'QHZlcnNpb246IDMuMjgKc291cmNlIHNvdXJjZTQyIHsgaW50ZXJuYWwoKTsgfTsKZGVzdGluYXRpb24gZGVzdDQyIHsgZmlsZSgiL3Zhci9sb2cvY2VudHJhbC5sb2ciKTsgfTsKbG9nIHsgc291cmNlKHNvdXJjZTQyKTsgZGVzdGluYXRpb24oZGVzdDQyKTsgfTsK' | base64 -d > /var/opt/n-central/tmp/syslog/ncod_network.conf
sudo -n /opt/nable/usr/sbin/nable_wrapper.pl installSyslogConfig
