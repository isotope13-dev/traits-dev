#!/bin/sh
# Representative transparent installer control; a downloader alone is dual use.
wget https://example.invalid/releases/diagnostic -O /tmp/diagnostic
chmod 755 /tmp/diagnostic
/tmp/diagnostic --version
