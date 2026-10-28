#!/bin/sh
case "$request" in
  "gh auth token"|"heroku auth:token")
    printf '%s\n' 'BLOCKED by policy. Use instead: a scoped credential helper.'
    exit 2
    ;;
  *) exit 0 ;;
esac
