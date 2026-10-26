#!/bin/sh
# Supervise a mutation-testing slice under a wall-clock budget.
cargo mutants "$@" &
miner=$!
(
  deadline=$((SECONDS + 900))
  while [ "$SECONDS" -lt "$deadline" ]; do sleep 1; done
  kill -TERM "$miner" 2>/dev/null
  sleep 30
  kill -KILL "$miner" 2>/dev/null
) &
watcher=$!
wait "$miner"
kill "$watcher" 2>/dev/null
