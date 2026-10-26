#!/bin/sh
# CI lint setup: the official gosec installer, as documented in the
# securego/gosec README. A toolchain bootstrap, not a dropper.
wget -O- -nv https://raw.githubusercontent.com/securego/gosec/master/install.sh | sh -s v2.13.1
./bin/gosec ./...
