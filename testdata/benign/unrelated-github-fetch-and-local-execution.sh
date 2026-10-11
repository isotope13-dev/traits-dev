#!/bin/sh
# Fetch a reference script for inspection; do not run it.
curl -s https://raw.githubusercontent.com/example/reference/refs/heads/main/guide.sh -o /var/tmp/guide.txt
# Set executable mode on a separately supplied local helper.
chmod +x /var/tmp/preexisting-helper.sh
# Launch an unrelated local background helper.
nohup bash ./local-healthcheck.sh > /dev/null 2>&1 &

# Run a second, independently supplied local diagnostic.
bash ./local-diagnostic.sh
