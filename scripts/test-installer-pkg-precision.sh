#!/bin/sh
# Static scanning only; do not run any installer or fixture.
set -eu
ATOMSCAN=${ATOMSCAN:-atomscan}
report=$(mktemp /tmp/installer-pkg-precision.XXXXXX)
status=0
CLEAVE_ANALYSIS_MEMO_MB=0 STNG_STRING_CACHE=0 FILEFACTS_CACHE=0 CLEAVE_SKIP_CACHE=1 \
  CLEAVE_TRAITS_DIR="${CLEAVE_TRAITS_DIR:-.}" \
  "$ATOMSCAN" path --no-update --mode slow --follow=none --format json \
  testdata/benign/installer-pkg-controls \
  testdata/hostile/supply-chain-corpus/macpkg/macpkg-clovermarksync-nested-pkg-plugin-macos.pkg \
  > "$report" || status=$?
case "$status" in
  0|1) ;;
  *) exit "$status" ;;
esac
jq -e -s '
  "micro-behaviors/os/package-manager/sideload::macos-installer-pkg" as $call |
  "micro-behaviors/os/package-manager/sideload::macos-installer-pkg-command-reference" as $reference |
  "micro-behaviors/process/create/installer::macos-pkg-root-command-reference" as $root_reference |
  map(.raw.files[0]) as $roots |
  ($roots | map(.path | split("/")[-1]) | sort) == [
    "absolute.sh", "bare.sh", "command-reference.c", "disconnected.sh",
    "documentation.sh", "macpkg-clovermarksync-nested-pkg-plugin-macos.pkg",
    "multiline.sh", "root-command-reference.m", "similar-tool.sh"
  ] and
  all($roots[];
    (.path | split("/")[-1]) as $name |
    ($name == "bare.sh" or $name == "absolute.sh" or $name == "multiline.sh" or
     ($name | endswith(".pkg"))) == any(.traits[]?; .id == $call and .crit == 3)) and
  all($roots[];
    (.path | endswith(".c") or endswith(".m")) ==
    any(.traits[]?; .id == $reference and .crit == 3)) and
  all($roots[];
    (.path | endswith(".m")) == any(.traits[]?; .id == $root_reference and .crit == 3)) and
  all(.[].raw.files[] | select(.path | contains("/installer-pkg-controls/"));
    all(.traits[]?; .crit < 4)) and
  any(.[].raw.files[];
    (.path | endswith(".pkg!!Scripts!!Scripts!!postinstall")) and
    any(.traits[]?; .id == $call and .crit == 3))
' "$report"
printf 'Static installer invocation controls passed; report: %s\n' "$report"
