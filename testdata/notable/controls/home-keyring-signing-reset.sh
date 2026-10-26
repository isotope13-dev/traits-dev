#!/bin/sh
set -eu
rm -rf "$HOME/.gnupg"
gpg --batch --import signing-key.asc
gpg --batch --detach-sign dist/artifact
