#!/bin/sh
openconnect --protocol=fortinet --user "$USER" "$1"
nxc smb "$2" -u "$USER" --shares
