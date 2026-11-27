#!/bin/sh
# Wrapper refresh: installs the CLI at whatever dist-tag the environment names.
PACKAGE="@example/cli"
TAG="${CLI_DIST_TAG:-latest}"

install_package() {
  HOME=/home/user timeout -k 5s 30s npm install -g --prefix=/home/user/.local \
    --no-audit --no-fund --force \
    "$PACKAGE@$TAG" >/dev/null 2>"$ERRLOG"
}

install_package
exit 0
