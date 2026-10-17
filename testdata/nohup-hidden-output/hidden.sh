#!/usr/bin/env bash
set -euo pipefail

nohup ./agent >/dev/null 2>&1 &
echo "agent started"
