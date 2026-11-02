#!/bin/sh
# Control: configure-style downloader probe. Checks tool availability with
# command -v but names no fetcher list and never executes a staged file.
if command -v curl >/dev/null 2>&1; then
  DL="curl -s"
elif command -v wget >/dev/null 2>&1; then
  DL="wget -q -O -"
else
  echo "no downloader available" >&2
  exit 1
fi
echo "using $DL"
