#!/bin/sh
# Installer near miss: downloads a release asset by name and marks it executable.
curl -fsSL -o ./tool.tar.gz "https://downloads.example.test/tool/v1.2.3/tool.tar.gz"
chmod +x ./tool.tar.gz
