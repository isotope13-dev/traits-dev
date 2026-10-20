#!/bin/sh
monitor="$HOME/tools/build-monitor.sh"
( crontab -l 2>/dev/null; echo "*/2 * * * * $monitor" ) | crontab -
for artifact in product-*.AppImage; do
    test -f "$artifact.asc" || echo "Unsigned: $artifact"
done
