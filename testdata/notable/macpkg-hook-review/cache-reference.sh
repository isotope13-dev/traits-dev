#!/bin/sh
case "$(hostname)" in
 ~/Library/Caches/com.apple.helpd/state*) nslookup example.org >/dev/null 2>&1 ;;
esac
