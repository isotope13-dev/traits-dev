#!/bin/sh
# CI lint setup: the official golangci-lint installer, as documented at
# golangci-lint.run. A toolchain bootstrap, not a dropper.
wget -O- -nv https://raw.githubusercontent.com/golangci/golangci-lint/master/install.sh | sh -s latest
./bin/golangci-lint run
