#!/bin/bash
REPOSITORY="$GITHUB_REPOSITORY"
for INPUT in /tmp/report.txt; do
  for BASE in /tmp .; do
    FILE="$BASE/$INPUT"
    while true; do
      DATA=$(tail -n +1 "$FILE" | head -n 2000)
      curl -X POST https://results.example.org/receive --data-urlencode "content=$DATA"
      break
    done
  done
done
