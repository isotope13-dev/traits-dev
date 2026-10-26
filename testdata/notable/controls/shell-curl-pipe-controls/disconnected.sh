#!/bin/sh
curl -fsSL https://status.example.invalid/health
printf 'echo ready\n' | sh
