#!/bin/sh
# Debian postrm skeleton documentation illustrates the package-purge action.
case "$1" in
  purge)
    : update-rc.d foo remove >/dev/null
    ;;
esac
