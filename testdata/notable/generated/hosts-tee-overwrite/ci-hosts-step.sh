#!/usr/bin/env bash
# Fixture: CI setup step overwriting /etc/hosts with a loopback-only resolver
# mapping, the pwncat integration-test pattern.
# Proves micro-behaviors/fs/write/file/hosts::hosts-file-tee-overwrite and
# well-known/tool/offensive/pwncat::pwncat-tool-reference.
if [ `uname` = "Linux" ]; then
  cat /etc/hosts
  (
    echo "127.0.0.1       localhost";
    echo "::1     localhost ip6-localhost ip6-loopback";
  ) | sudo tee /etc/hosts
  cat /etc/hosts
  retry make __test-cnc--inject_shell-pwncat
fi
