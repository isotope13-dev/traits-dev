#!/bin/sh
grep -q ready /tmp/state 2>/dev/null || \
  printf '%s' body \
    > /tmp/session-helper
