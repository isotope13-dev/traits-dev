#!/bin/bash
API="https://api.github.com/repos/${REPOSITORY}"
curl -sS -X POST \
  "$API/statuses/$SHA" -H "Authorization: Bearer $GITHUB_TOKEN" \
  -d "{\"state\":\"success\",\"context\":\"$CHECK\"}"
