// Embedded workflow syntax still needs detection in source files.
const workflow = `name: checks
on: [push, pull_request]
jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - run: npm test
`;
