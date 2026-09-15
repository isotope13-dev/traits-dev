#!/bin/sh
# Static analysis only: never invoke a fixture or installer.
set -eu
ATOMSCAN=${ATOMSCAN:-atomscan}
report=$(mktemp /tmp/launchd-written-loader.XXXXXX)
status=0
CLEAVE_ANALYSIS_MEMO_MB=0 STNG_STRING_CACHE=0 FILEFACTS_CACHE=0 CLEAVE_SKIP_CACHE=1 \
  CLEAVE_TRAITS_DIR="${CLEAVE_TRAITS_DIR:-.}" \
  "$ATOMSCAN" path --no-update --mode slow --follow=none --format json \
  testdata/benign/launchd-loader-controls \
  testdata/hostile/supply-chain-corpus/macpkg/macpkg-tidecrestforge-postinstall-launchagent-macos.pkg \
  > "$report" || status=$?
case "$status" in
  0|1) ;;
  *) exit "$status" ;;
esac
jq -e -s '
  "micro-behaviors/os/service/launchagent::shell-load-written-autostart-fetch-pipe" as $behavior |
  "objectives/supply-chain/trojanized/app/remote-install::installer-launchagent-shell-loader" as $objective |
  map(.raw.files[0]) as $roots |
  ($roots | map(.path | split("/")[-1]) | sort) == [
    "commented-command.sh", "documentation.sh", "local-service.sh",
    "macpkg-tidecrestforge-postinstall-launchagent-macos.pkg", "overwritten.sh"
  ] and
  all(.[].raw.files[] | select(.path | contains("/launchd-loader-controls/"));
    all(.traits[]?; .crit < 4 and .id != $objective and .id != $behavior)) and
  all($roots[] | select(.path | endswith(".pkg"));
    ([.traits[]? | select(.crit == 5) | .id] == [$objective])) and
  any(.[].raw.files[];
    (.path | endswith(".pkg!!Scripts!!Scripts!!postinstall")) and
    any(.traits[]?; .id == $behavior and .crit == 3) and
    any(.traits[]?; .id == $objective and .crit == 5))
' "$report"
printf 'Static written LaunchAgent controls passed; report: %s\n' "$report"
