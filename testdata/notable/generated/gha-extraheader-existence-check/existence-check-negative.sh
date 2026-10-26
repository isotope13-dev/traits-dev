#!/bin/sh
# Negative: existence check only uses the exit status; the token value is
# never read. Mirrors release CI that falls back to minting its own token.
if git config --get-all http.https://github.com/.extraheader >/dev/null; then
  git fetch origin
fi
