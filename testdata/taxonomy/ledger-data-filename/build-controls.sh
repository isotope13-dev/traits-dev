#!/bin/sh
# Rebuild the committed fixture binaries from source. Outputs are committed
# so scanners test stable bytes; rerun after toolchain changes.
set -eu
cd "$(dirname "$0")"
cc -O0 -o positive/brand-refs positive/brand-refs.c
cc -O0 -o near-miss/ledger-data-file near-miss/ledger-data-file.c
