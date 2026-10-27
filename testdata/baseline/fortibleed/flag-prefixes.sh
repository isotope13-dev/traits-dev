#!/bin/sh
nxc smb "$1" --ntds-cache
openconnect --protocol=fortinet-unknown "$2"
