#!/bin/sh
# Shut down the local Tor daemon; this script never starts it.
sudo systemctl stop tor
echo "tor stopped"
