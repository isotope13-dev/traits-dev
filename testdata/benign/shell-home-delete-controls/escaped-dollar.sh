#!/bin/sh
# Double quotes do not expand an escaped dollar sign.
rm -rf "\$HOME/Documents" "\$HOME/Desktop" "\$HOME/Pictures"
