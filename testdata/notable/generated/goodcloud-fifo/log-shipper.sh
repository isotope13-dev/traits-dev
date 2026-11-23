#!/bin/sh
mkfifo /tmp/logs
while true; do cat /tmp/logs | nc logs.example 5514; sleep 3; done
