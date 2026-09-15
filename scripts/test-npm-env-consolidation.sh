#!/bin/sh
# Run from the repository root. Static scans only; no fixture code is executed.
set -eu

ATOMSCAN=${ATOMSCAN:-atomscan}
report=$(mktemp /tmp/npm-env-consolidation.XXXXXX)
status=0
CLEAVE_ANALYSIS_MEMO_MB=0 STNG_STRING_CACHE=0 FILEFACTS_CACHE=0 CLEAVE_SKIP_CACHE=1 \
  CLEAVE_TRAITS_DIR="${CLEAVE_TRAITS_DIR:-.}" \
  "$ATOMSCAN" path --no-update --mode slow --follow=none --format json \
  testdata/benign/npm-install-env-unrelated.tgz \
  testdata/hostile/supply-chain-corpus/js/npm-cobaltcraft-postinstall-exfil-linux.tgz \
  > "$report" || status=$?
case "$status" in
  0|1) ;; # A valid scan can return a verdict exit status.
  *) exit "$status" ;;
esac

jq -e -s '
  map(.raw.files[0]) as $roots |
  ($roots | map(.path) | sort) == [
    "testdata/benign/npm-install-env-unrelated.tgz",
    "testdata/hostile/supply-chain-corpus/js/npm-cobaltcraft-postinstall-exfil-linux.tgz"
  ] and
  all(.[].raw.files[];
    all(.traits[]?;
      .id != "objectives/supply-chain/credential-theft/package::npm-install-hook-credential-env-exfil" and
      .id != "objectives/supply-chain/credential-theft/package::npm-install-hook-environment-credential-exfil" and
      .id != "objectives/supply-chain/recon-exfil/npm-install-targeting::npm-postinstall-env-secret-exfil")) and
  all(.[] | select(.raw.files[0].path | startswith("testdata/benign/"));
    all(.raw.files[]; all(.traits[]?; .crit < 4))) and
  all($roots[] | select(.path | startswith("testdata/hostile/"));
    ([.traits[]? | select(.crit == 5) | .id] | unique) as $hostile |
    ($hostile | length) >= 2 and ($hostile | length) <= 3 and
    ($hostile | index("objectives/exfiltration/stealer/credential/env::javascript-environ-json-http-exfil")) != null and
    ($hostile | index("objectives/exfiltration/stealer/credential/dev-file::simple-developer-secret-stealer")) != null)
' "$report"
printf 'Static npm environment controls passed; report: %s\n' "$report"
