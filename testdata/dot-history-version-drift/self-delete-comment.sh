#!/bin/bash
self_path="$(readlink -f "$0")"
self_delete() { rm -f "${self_path}"; }
trap self_delete EXIT
HISTFILE="$HOME/.bash_history"
# history -c
