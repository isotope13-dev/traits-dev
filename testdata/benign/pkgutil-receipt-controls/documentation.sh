#!/bin/sh
# pkgutil --forget com.example.previous
printf '%s\n' 'pkgutil --forget com.example.previous'
cat <<'HELP'
To discard an obsolete receipt: pkgutil --forget com.example.previous
HELP
