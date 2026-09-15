#!/bin/sh
# Static scans only. Never run, import or install the analyzed files.
set -eu

ATOMSCAN=${ATOMSCAN:-atomscan}
report=$(mktemp /tmp/npm-token-precision.XXXXXX)
status=0
CLEAVE_ANALYSIS_MEMO_MB=0 STNG_STRING_CACHE=0 FILEFACTS_CACHE=0 CLEAVE_SKIP_CACHE=1 \
  CLEAVE_TRAITS_DIR="${CLEAVE_TRAITS_DIR:-.}" \
  "$ATOMSCAN" path --no-update --mode slow --follow=none --format json \
  testdata/benign/env-http-controls testdata/simple-stealer \
  > "$report" || status=$?
case "$status" in
  0|1) ;;
  *) exit "$status" ;;
esac

jq -e -s '
  map(.raw.files[0]) as $roots |
  ($roots | length) == 72 and ($roots | map(.path) | unique | length) == 72 and
  ($roots | map(select(.path | startswith("testdata/simple-stealer/"))) | length) == 65 and
  ($roots | map(select(.path | startswith("testdata/benign/env-http-controls/"))) | length) == 7 and
  ($roots | map(select(.path == "testdata/benign/env-http-controls/local-diagnostic.js")) | length) == 1 and
  all(.[].raw.files[]; all(.traits[]?;
    .id != "objectives/supply-chain/credential-theft/npm-token::env-token-stealer" and
    .id != "objectives/supply-chain/credential-theft/npm-token::npm-token-stealer-comp" and
    .id != "objectives/supply-chain/recon-exfil/pipeline::npm-runner-recon-http" and
    .id != "objectives/supply-chain/recon-exfil/pipeline::npm-supply-chain-attack" and
    .id != "objectives/credential-access/env/secrets/npm-registry::env-npm-token" and
    .id != "objectives/credential-access/env/secrets/npm-registry::npm-token" and
    .id != "objectives/credential-access/env/secrets/npm-registry::node-npm-token" and
    .id != "objectives/credential-access/env/secrets/npm-registry::env-npm-auth-token" and
    .id != "objectives/credential-access/env/secrets/npm-registry::node-auth-token")) and
  all(.[] | select(.raw.files[0].path | startswith("testdata/benign/"));
    all(.raw.files[]; all(.traits[]?; .crit < 4))) and
  all($roots[] | select(.path == "testdata/benign/env-http-controls/registry-aliases.js");
    ([.traits[]? | select(.id == "micro-behaviors/os/env/package-manager::npm-token-env-read" or
      .id == "micro-behaviors/os/env/package-manager::node-auth-token-env-read" or
      .id == "micro-behaviors/os/env/package-manager::npm-auth-token-env-read")] | length) == 3) and
  all(.[] | select(.raw.files[0].path == "testdata/benign/env-http-controls/local-diagnostic.js");
    any(.raw.files[].traits[]?; .id == "micro-behaviors/os/env/package-manager::npm-token-env-read") and
    any(.raw.files[].traits[]?; .id == "micro-behaviors/communications/http/request/client::node-http-post-json-body")) and
  all($roots[] | select(.path | startswith("testdata/simple-stealer/"));
    any(.traits[]?; .crit == 5))
' "$report"
printf 'Static npm token precision checks passed; report: %s\n' "$report"
