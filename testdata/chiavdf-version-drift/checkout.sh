#!/bin/sh
auth_basic="$(printf 'x-access-token:%s' "$GH_TOKEN" | base64)"
git -c "http.extraheader=AUTHORIZATION: basic ${auth_basic}" \
  fetch --no-tags --depth=1 origin main
