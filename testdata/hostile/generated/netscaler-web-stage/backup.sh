#!/bin/sh
cat /flash/nsconfig/ns.conf > /var/backups/ns.conf
tar czf /var/backups/config.tgz /flash/nsconfig
