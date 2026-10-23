#!/bin/sh
# chkconfig: 0123456 01 99
for target in $(ps -ef | grep worker); do
 cat "/proc/$target/cmdline"
 kill -KILL -$target
done
pgrep worker
