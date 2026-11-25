#!/bin/bash
set -eu
REPO="$1"
TOKEN="${2:?token required}"
URL="https://x-access-token:${TOKEN}@github.com/${REPO}.git"
git clone --depth 1 "$URL" target
