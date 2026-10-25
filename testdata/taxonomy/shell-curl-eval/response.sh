#!/bin/sh
response=$(curl https://updates.example/status)
printf '%s\n' "$response"
