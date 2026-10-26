#!/bin/sh
status=$(curl -o /dev/null -w "%{http_code}" -H "Authorization: Bearer $TOKEN" https://api.github.com/user)
if [ "$status" = 401 ]; then echo "Token expired"; fi
