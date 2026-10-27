#!/bin/sh
cat /etc/passwd > inventory.txt
curl --data-binary @health.json https://collector.example/health
