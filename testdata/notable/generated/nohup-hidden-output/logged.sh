#!/usr/bin/env bash
set -euo pipefail

command -v worker >/dev/null 2>&1 || exit 1
echo "starting worker, output goes to the log file"

# Daemon output stays visible in its log; unrelated silences elsewhere
# must not count as hiding this invocation.
nohup ./worker >/tmp/worker.log 2>/tmp/worker_error.log &

wait_for_start() {
  pgrep -f worker >/dev/null 2>&1
}
wait_for_start
