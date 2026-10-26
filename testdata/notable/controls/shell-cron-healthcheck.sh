#!/bin/sh
# Maintain a periodic service health check; never execute the response body.
(crontab -l 2>/dev/null | grep -v example-health;
 echo '*/23 * * * * curl -fsSL https://health.example.invalid/status >/dev/null 2>&1 # example-health') | crontab -
