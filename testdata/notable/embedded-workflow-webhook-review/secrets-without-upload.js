export const workflow = "jobs:\n  deploy:\n    steps:\n    - run: ./configure-local.sh\n      env:\n        SETTINGS: ${{ toJSON(secrets) }}\n";
