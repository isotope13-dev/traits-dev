#!/bin/sh
# Recursion belongs to the build cleanup, not the personal-folder operands.
rm -rf ./build-fixture
rm -f "$HOME/Documents" "$HOME/Desktop"
