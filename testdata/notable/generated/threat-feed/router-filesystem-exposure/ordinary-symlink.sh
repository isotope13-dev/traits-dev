#!/bin/sh
ln -s /opt/public public
curl --fail "http://router:8052/sda1/public/readme.txt" -o readme.txt
