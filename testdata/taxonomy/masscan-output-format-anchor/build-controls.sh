#!/bin/sh
# Rebuild the committed fixture binaries from source. Outputs are committed
# so scanners test stable bytes; rerun after toolchain changes.
set -eu
cd "$(dirname "$0")"
cc -O0 -o positive/flag-context positive/flag-context.c
cc -O0 -o near-miss/bare-flag near-miss/bare-flag.c
