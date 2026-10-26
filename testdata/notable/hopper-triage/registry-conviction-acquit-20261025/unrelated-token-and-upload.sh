echo "$NPM_TOKEN" >/dev/null
printf "build stats" | curl --data-binary @- https://example.invalid/stats
