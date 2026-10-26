#!/bin/sh
# After --, -rf is an operand, not a recursive option.
rm -- -rf "$HOME/Documents" "$HOME/Desktop"
