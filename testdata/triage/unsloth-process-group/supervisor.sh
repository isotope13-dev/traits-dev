#!/bin/sh
exec 3<&0
setsid "$@" </dev/null &
child=$!
trap 'kill -TERM -$child 2>/dev/null' TERM INT HUP
(cat <&3 >/dev/null; kill -TERM -$child 2>/dev/null; sleep 10; kill -KILL -$child 2>/dev/null) &
watcher=$!
exec 3<&-
wait $child
status=$?
kill $watcher 2>/dev/null
# Workers the engine forked outlive a crashed leader and would hold GPU memory.
if kill -0 -$child 2>/dev/null; then
  kill -TERM -$child 2>/dev/null; sleep 5; kill -KILL -$child 2>/dev/null
fi
exit $status
