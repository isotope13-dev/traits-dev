#!/bin/sh
# if [ -e "$HOME/.cache/pki/marker" ]; then
# for f in dist/*.tar.gz; do
if [ -e "$HOME/.config/tool/ready" ]; then
  for f in docs/*.txt; do
    : "$f"
  done
fi
