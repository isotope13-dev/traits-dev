#!/bin/sh
# Compile static test inputs. Never run the resulting scripts.
set -eu
cd "$(dirname "$0")"
for source in ./*.applescript; do
    osacompile -o "${source%.applescript}.scpt" "$source"
done
