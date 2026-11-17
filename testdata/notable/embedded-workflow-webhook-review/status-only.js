export const workflow = "jobs:\n  report:\n    steps:\n    - run: curl -d \"$STATUS\" https://webhook.site/12345678-1234-1234-1234-123456789abc\n      env:\n        STATUS: finished\n";
