Restore detection on these verified supply-chain compromise(s). Each one is a real, confirmed
attack that the current traits do not call hostile:
- /data/fixed/853e5169d938eb223929d7fc9509991319d29e4f40233ca57c0e3c5cc7ad6e8d/laravel-lang__laravel-lang-actions-1.12.2-RECONSTRUCTED.zip — hostile: 0, suspicious: 4, ml.lvl: 279
  - S objectives/anti-static/obfuscation/string/encoding::array-map-chr-codepoint-list — String decoded from a chr() code-point list
    members: /data/fixed/853e5169d938eb223929d7fc9509991319d29e4f40233ca57c0e3c5cc7ad6e8d/laravel-lang__laravel-lang-actions-1.12.2-RECONSTRUCTED.zip!!Laravel-Lang-actions-556d2b3/src/helpers.php
  - S objectives/evasion/process/hidden/execution::php-dual-platform-silent-launch — PHP launches a hidden child on both Windows and Unix
    members: /data/fixed/853e5169d938eb223929d7fc9509991319d29e4f40233ca57c0e3c5cc7ad6e8d/laravel-lang__laravel-lang-actions-1.12.2-RECONSTRUCTED.zip!!Laravel-Lang-actions-556d2b3/src/helpers.php
  - S objectives/execution/condition/host-marker::host-digest-temp-marker-gate — Host-name digest marker in temp gates execution
    members: /data/fixed/853e5169d938eb223929d7fc9509991319d29e4f40233ca57c0e3c5cc7ad6e8d/laravel-lang__laravel-lang-actions-1.12.2-RECONSTRUCTED.zip!!Laravel-Lang-actions-556d2b3/src/helpers.php
  - S objectives/supply-chain/install-hook/autoload::composer-autoload-fetch-and-spawn — Composer-autoloaded package fetches a URL and spawns a process
- /data/fixed/5dca3f4fc310f83a30dfdffc3b4ff7593f3d2b04b08c69d754576edf0b03a691/lottie-player__lottie-player-malware.js — hostile: 0, suspicious: 3, ml.lvl: -1
  - S objectives/anti-analysis/debugger-detect/check::js-devtools-getter-oracle — Detects DevTools by a logged getter
  - S objectives/anti-static/obfuscation/obfuscator/index-shift::custom-string-table-obfuscator — Custom string-table obfuscator output
  - S objectives/anti-static/obfuscation/obfuscator/index-shift::table-accessor-ternary-index-shift — String-table accessor shifts a ternary index

Success: at least 1 hostile finding on the sample itself — the root record, not only on a member
inside it. Every finding you add must accurately describe behavior you actually observed in the
sample, at the criticality it deserves.

Any findings listed above are the near misses: traits that fired below hostile on this sample are
usually where the missing detection belongs, and raising or extending one you can justify is
preferable to writing a new trait beside it. A sample with nothing listed needs the mechanism
identified first.

Identify what the sample actually does before changing any trait. Use `cleave facts` and
`cleave test-rules` on the extracted members; facts are faster and more reliable than text
searches. Extract archives once and group equivalent `src`/`dist`, `.js`/`.ts`, architecture, and
bundled-library variants. Name the concrete mechanism — the install hook, the network callback,
the exec, the encoded payload, the path it writes — and write the trait against that.

A second corpus of manually vetted BENIGN files gates this same tag, and every trait you touch is
measured against it in the same run. A trait broad enough to fire on ordinary software will be
caught there and sent back as a false positive, which spends another repair round and lands
nothing. Prefer a trait that names the attack's specific behavior over one that widens an existing
rule until it happens to cover this sample. Give traits specific IDs and descriptions that tell an
analyst what behavior was observed and why it matters.

Make all planned changes before measuring each sample:

  /data/rectifier/bin/cleave analyze <sample>

Run this at least once after editing and before finishing. Confirm the hostile finding is on the
sample's own record. Inspect findings at every criticality, not only the one that affects the QA
gate. If the success criteria are not met or any finding is misleading or inaccurate, make the next
complete set of changes before analyzing again.

Before finishing, you MUST run:

  make -C /data/rectifier/traits-dev validate CLEAVE=/data/rectifier/bin/cleave

Fix every error and rerun until it passes. Rectifier performs the authoritative rescan.
