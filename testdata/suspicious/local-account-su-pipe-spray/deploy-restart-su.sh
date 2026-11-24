#!/bin/sh
# Restart the app service as its service account.
printf '%s\n' "$APP_PASS" | su deploy -c "systemctl restart app"
