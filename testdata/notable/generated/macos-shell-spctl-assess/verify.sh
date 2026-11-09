#!/bin/bash
# Admin verification helper: assesses a staged installer package with
# Gatekeeper before approving it. No download, no fingerprinting.
PKG="$1"
spctl --assess --type install "${PKG}"
echo "assess exit: $?"
