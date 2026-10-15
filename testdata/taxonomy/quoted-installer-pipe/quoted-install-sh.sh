#!/bin/sh
# Composite-action style: the installer URL is shell-quoted.
curl -fsSL "https://example.com/install.sh" | bash -s -- "-f" "-y"
