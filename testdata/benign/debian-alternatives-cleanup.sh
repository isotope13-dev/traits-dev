#!/bin/sh
# Debian maintainer-script cleanup: unregisters stale tool binaries. Names
# pattern_create/pattern_offset to forget them, not to use offset tooling.
set -e
OLD_BINS="metasm_shell nasm_shell pattern_create pattern_offset exe2vba"

if [ "$1" = "upgrade" ]; then
  for OLD_BIN in $OLD_BINS; do
    update-alternatives --quiet --remove $OLD_BIN /usr/share/metasploit-framework/$OLD_BIN
  done
fi
exit 0
