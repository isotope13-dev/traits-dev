#!/bin/sh
# Run from the repository root. This scans scripts and archives as data only.
set -eu

ATOMSCAN=${ATOMSCAN:-atomscan}
report=$(mktemp /tmp/pkgutil-receipts.XXXXXX)
status=0
CLEAVE_ANALYSIS_MEMO_MB=0 STNG_STRING_CACHE=0 FILEFACTS_CACHE=0 CLEAVE_SKIP_CACHE=1 \
  CLEAVE_TRAITS_DIR="${CLEAVE_TRAITS_DIR:-.}" \
  "$ATOMSCAN" path --no-update --mode slow --follow=none --format json \
  testdata/benign/pkgutil-receipt-controls \
  testdata/hostile/supply-chain-corpus/macpkg/macpkg-indigocore-receipt-manipulate-macos.pkg \
  > "$report" || status=$?
case "$status" in
  0|1) ;; # A valid report can be accompanied by a verdict exit status.
  *) exit "$status" ;;
esac

jq -e -s '
  map(.raw.files[0]) as $roots |
  ($roots | map(.path | split("/")[-1]) | sort) == [
    "absolute.sh", "disconnected.sh", "documentation.sh", "forget.sh",
    "macpkg-indigocore-receipt-manipulate-macos.pkg", "multiline.sh",
    "similar-name.sh"
  ] and
  all($roots[];
    (.path | split("/")[-1]) as $name |
    ($name == "absolute.sh" or $name == "forget.sh" or
     $name == "multiline.sh" or ($name | endswith(".pkg"))) as $invokes |
    (any(.traits[]?;
      .id == "micro-behaviors/os/package-manager/management::macos-pkg-forget-receipts" and
      .crit == 3)) == $invokes) and
  all(.[].raw.files[]; all(.traits[]?; .crit < 4)) and
  any(.[].raw.files[];
    (.path | endswith(".pkg!!Scripts!!Scripts!!postinstall")) and
    any(.traits[]?;
      .id == "micro-behaviors/os/package-manager/management::macos-pkg-forget-receipts"))
' "$report"
printf 'Static receipt controls passed; report: %s\n' "$report"
