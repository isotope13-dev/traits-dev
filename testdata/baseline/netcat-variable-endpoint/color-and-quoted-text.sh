#!/bin/sh
nc='\033[0m'
printf '%s%s%s\n' "$nc" "$title" "$nc"
# nc "$HOST" "$PORT"
printf '%s\n' 'nc "$HOST" "$PORT"'
