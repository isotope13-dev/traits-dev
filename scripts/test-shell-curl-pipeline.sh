#!/bin/sh
# Run from the repository root. Only scans fixtures; never executes their code.
# validate's hierarchy assertions intentionally do not accept individual IDs.
set -eu

ATOMSCAN=${ATOMSCAN:-atomscan}
report=$(mktemp /tmp/shell-curl-pipeline.XXXXXX)
status=0
CLEAVE_ANALYSIS_MEMO_MB=0 STNG_STRING_CACHE=0 FILEFACTS_CACHE=0 CLEAVE_SKIP_CACHE=1 \
  CLEAVE_TRAITS_DIR="${CLEAVE_TRAITS_DIR:-.}" \
  "$ATOMSCAN" path --no-update --mode slow --follow=none --format json \
  testdata/benign/shell-curl-pipe-controls > "$report" || status=$?
case "$status" in
  0|1) ;; # atomscan may return its verdict status with a valid report.
  *) exit "$status" ;;
esac

jq -e -s '
  map(.raw.files[0]) as $files |
  ($files | length) == 5 and
  ($files | map(.path | split("/")[-1]) | sort) ==
    ["bootstrap.sh", "disconnected.sh", "explicit-command.sh",
     "redirected-input.sh", "syntax-check.sh"] and
  all($files[];
    (.path | endswith("/bootstrap.sh")) as $executes |
    ([.traits[]? | select(.id ==
      "micro-behaviors/process/create/shell/pipeline::curl-response-shell-stdin")]
      | length > 0) == $executes and
    all(.traits[]?; .crit < 4))
' "$report"
printf 'Static pipeline controls passed; report: %s\n' "$report"
