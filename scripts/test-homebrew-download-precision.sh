#!/bin/sh
# Run from the repository root. Analyze Ruby files as data, never install them.
set -eu

ATOMSCAN=${ATOMSCAN:-atomscan}
report=$(mktemp /tmp/homebrew-download-precision.XXXXXX)
status=0
CLEAVE_ANALYSIS_MEMO_MB=0 STNG_STRING_CACHE=0 FILEFACTS_CACHE=0 CLEAVE_SKIP_CACHE=1 \
  CLEAVE_TRAITS_DIR="${CLEAVE_TRAITS_DIR:-.}" \
  "$ATOMSCAN" path --no-update --mode slow --follow=none --format json \
  testdata/benign/homebrew-download-controls \
  testdata/hostile/supply-chain-corpus/brew > "$report" || status=$?
case "$status" in
  0|1) ;; # A valid report may use a verdict exit status.
  *) exit "$status" ;;
esac

jq -e -s '
  map(.raw.files[0]) as $roots |
  ($roots | map(.path | split("/")[-1]) | sort) == [
    "brew-basaltstack-post-install-plist-macos.rb",
    "brew-brackenstack-livecheck-beacon-macos.rb",
    "brew-clovermarkstack-preinstall-exec-macos.rb",
    "brew-foxtailstack-pour-bottle-hook-macos.rb",
    "brew-gableguard-resource-typosquat-fetch-macos.rb",
    "brew-larkspurlite-on-macos-keychain-probe-macos.rb",
    "brew-onyxfieldlite-test-block-exec-macos.rb",
    "brew-quilltreebyte-patch-backdoor-macos.rb",
    "brew-riftwoodguard-caveats-curl-install-macos.rb",
    "brew-vermilionguard-audit-block-exfil-macos.rb",
    "data-download.rb", "quoted-install.rb"
  ] and
  all(.[].raw.files[]; all(.traits[]?;
    (.id | test("^objectives/supply-chain/credential-theft/registry::(formula-system-exec|cask-url-suspicious|formula-env-access|homebrew-formula-attack)$") | not))) and
  all($roots[] | select(.path | contains("/homebrew-download-controls/"));
    all(.traits[]?; .crit < 4) and
    any(.traits[]?; .id == "metadata/package/manager::homebrew-formula-class") and
    any(.traits[]?; .id == "micro-behaviors/communications/http/message::http-url-literal")) and
  all($roots[] | select(.path | contains("/homebrew-download-controls/"));
    (.path | endswith("/data-download.rb")) ==
    any(.traits[]?; .id == "micro-behaviors/process/create/system::system-process-call")) and
  ([$roots[] | select(any(.traits[]?; .crit == 5)) | .path | split("/")[-1]] | sort) == [
    "brew-basaltstack-post-install-plist-macos.rb",
    "brew-clovermarkstack-preinstall-exec-macos.rb",
    "brew-larkspurlite-on-macos-keychain-probe-macos.rb",
    "brew-onyxfieldlite-test-block-exec-macos.rb",
    "brew-quilltreebyte-patch-backdoor-macos.rb"
  ] and
  all($roots[]; ([.traits[]? | select(.crit == 5)] | length) <= 3)
' "$report"
printf 'Static Homebrew precision controls passed; report: %s\n' "$report"
