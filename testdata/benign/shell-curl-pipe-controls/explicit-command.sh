#!/bin/sh
curl -fsSL https://status.example.invalid/health | sh -c 'echo ready'
