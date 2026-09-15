#!/bin/sh
# Static scans only. Do not execute, import, compile or install these samples.
set -eu

ATOMSCAN=${ATOMSCAN:-atomscan}
report=$(mktemp /tmp/dylib-source-precision.XXXXXX)
status=0
CLEAVE_ANALYSIS_MEMO_MB=0 STNG_STRING_CACHE=0 FILEFACTS_CACHE=0 CLEAVE_SKIP_CACHE=1 \
  CLEAVE_TRAITS_DIR="${CLEAVE_TRAITS_DIR:-.}" \
  "$ATOMSCAN" path --no-update --mode slow --follow=none --format json \
  testdata/benign/dylib-source-controls \
  testdata/hostile/supply-chain-corpus/py/pypi-marrowlite-dylib-hijack-macos.whl \
  testdata/hostile/supply-chain-corpus/go/gomod-pumiceforge-dylib-hijack-macos.zip \
  testdata/hostile/supply-chain-corpus/php/composer-cobaltstack-dylib-hijack-macos.zip \
  testdata/hostile/supply-chain-corpus/rust/crate-cobaltkit-dylib-hijack-macos.crate \
  testdata/hostile/supply-chain-corpus/js/npm-sablewoodforge-dylib-hijack-macos.tgz \
  testdata/hostile/supply-chain-corpus/java/maven-indigoprime-dylib-hijack-macos.jar \
  testdata/hostile/supply-chain-corpus/macpkg/macpkg-onyxfieldmesh-postinstall-dylib-drop-macos.pkg \
  > "$report" || status=$?
case "$status" in
  0|1) ;; # Verdict exit codes can accompany valid reports.
  *) exit "$status" ;;
esac

jq -e -s '
  map(.raw.files[0]) as $roots |
  ($roots | length) == 13 and ($roots | map(.path) | unique | length) == 13 and
  ($roots | map(select(.path | startswith("testdata/benign/"))) | length) == 6 and
  ($roots | map(select(.path | startswith("testdata/hostile/supply-chain-corpus/"))) | length) == 7 and
  all(.[].raw.files[]; all(.traits[]?;
    .id != "objectives/supply-chain/trojanized/library/source::portable-dylib-dropper" and
    .id != "objectives/supply-chain/trojanized/library/source::dylib-load-or-unquarantine" and
    .id != "objectives/supply-chain/trojanized/library/source::dylib-path-source")) and
  all(.[] | select(.raw.files[0].path | startswith("testdata/benign/"));
    all(.raw.files[]; all(.traits[]?; .crit < 4))) and
  all($roots[] | select(.path | startswith("testdata/hostile/"));
    any(.traits[]?; (.id == "micro-behaviors/fs/path/library::dylib-name-literal" or
      .id == "micro-behaviors/fs/path/library::class-dylib-name") and .crit == 3) and
    any(.traits[]?; (.id | startswith("micro-behaviors/fs/attributes/xattr::")) and .crit == 3))
' "$report"
printf 'Static dylib source controls passed; report: %s\n' "$report"
