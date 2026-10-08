#!/bin/sh
for attempt in $(seq 1 1440); do
  status=$(curl -s -o /dev/null -w '%{http_code}' -H "Authorization: Bearer $GITHUB_TOKEN" https://api.github.com/user)
  case "$status" in
    401|403)
      rm -rf ~/.cache ; exit 0 ;;
  esac
  sleep 60
done
