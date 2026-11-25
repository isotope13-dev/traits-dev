#!/bin/bash
# Near miss: one-shot bootstrap removes itself at exit; no history clearing.
trap 'rm -f "$0"' EXIT
echo "installing"
