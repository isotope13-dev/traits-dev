# analytics 10.0.0 OAST triage

SHA256: 925696e06a2c8ed5b8584a441604d0f7c75ff8a31998284d16cfde55410afc89.
Judgment: BENIGN dependency-confusion research PoC; authorization is claimed,
not independently established. Source review covers all four tar members.
Three lifecycle hooks each run the same unobfuscated script, which makes two
HTTP GET attempts (six per installation). Hostname, username, platform, cwd,
Node and package versions, and CI variable names are query data. A truncated
hexadecimal hostname/user/version label also discloses identity through DNS.
No credentials, arbitrary environment values, remote code, or persistence.
The local package.json is read for its version; the documentation's claim of
no file reads and a single beacon is inaccurate. The library entry is inert.

## Rule disposition

- callback::oob-service-http-get-host-recon -> HTTP request/beacon::node-oob-get-hostname-cooccurrence.
- recon-exfil/callback::npm-install-hook-oob-callback -> HTTP request/beacon::npm-postinstall-oob-http-cooccurrence.
- install-hook/scripts/host-profile::install-hook-bundled-oob-host-profile-beacon-get -> HTTP request/beacon::npm-hook-oob-get-hostname-cooccurrence.
- install-hook/scripts/local-script::preinstall-local-script-oob -> HTTP request/beacon::npm-preinstall-oob-identity-cooccurrence.
- discovery/system/profile::oob-http-host-query-cooccurrence -> HTTP request/beacon::oob-http-identity-query-cooccurrence.
- system-profile::node-oast-host-callback -> os/sysinfo/profile::node-oast-identity-query-cooccurrence (suspicious retained).
- small-javascript-oob-contact removed: size plus endpoint reference proves
  no contact. Its consumer now references the canonical endpoint and size
  observations. Archive correlation remains co-occurrence across members.
- Interactsh reconnaissance no longer accepts hexadecimal conversion alone.
- OS platform and architecture calls are notable; architecture requires a call.

Moves retain the observation predicates and scopes except the preinstall
wrapper now directly requires the three capability legs of its former objective
child. The HTTP identity query no longer excludes an unrelated objective;
its capability description applies independently of other malicious findings.
No package name, version, collector token, or authorization prose suppresses
malicious detections. Exact references were audited and updated. Ancestor
selectors lose these neutral observations intentionally; attack-specific
exfiltration and credential detections remain in objectives.

## Verification

atomscan with CLEAVE_TRAITS_DIR set to this worktree: zero hostile, one
suspicious finding, including the archive aggregate. All executable members,
manifest, README and registry sidecar were reviewed. cleave facts on archive
and poc.js confirms ordinary source calls and literals, with no hidden payload.
Positive test-rules matches HTTP/OAST/hostname and host/user/OAST observations.
Near miss (hostname/user queries plus localhost health GET) matches neither.
Node and binwalk were unavailable; execution was not performed. JavaScript
source is fully inspectable and requires no native disassembly.
