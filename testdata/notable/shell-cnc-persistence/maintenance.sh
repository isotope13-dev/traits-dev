#!/bin/sh
wget -qO package.tar https://example.org/package.tar
cp -f settings "$HOME/.settings"
echo "logger boot" >> "$HOME/rcS"
chmod 777 "$HOME/.settings"
