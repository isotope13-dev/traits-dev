#!/bin/sh
# MTProto proxy installer: publish the client share-link template.
IP=$(curl -s https://api.ipify.org)
echo "proxy ready: https://t.me/proxy?server=$IP&port=443&secret=dd0000000000"
