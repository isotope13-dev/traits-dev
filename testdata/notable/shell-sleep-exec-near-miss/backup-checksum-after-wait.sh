#!/bin/sh
# Nightly checksum after the backup window closes
sleep 3600; shasum -a 256 /var/backups/db.tar > /var/backups/db.tar.sha256
