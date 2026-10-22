# Three-sample reasoned review, 2026-10-22

## Judgments and execution paths

* **BENIGN — recovery-and-persistence.cpp**, SHA256
  `f0226c6a508e5eb1a23974ccc41ab1f9d3b332618f8c9f4d2153bf9f75475f31`.
  This is byte-identical to `../siriusqt-techniques/native-reconstruction.cpp`.
  Its existing provenance record, `../siriusqt-techniques/evidence.json`,
  identifies an analyst's representative source reconstruction, explicitly
  not original SiriusQT source or a recovered executable. Research provenance,
  an operator-supplied AES key, and explicit CLI activation tip the judgment
  toward a research demonstrator. An unauthorized deployment would change
  the context; no such deployment evidence is supplied. This is not a family
  identification from behavior or an assertion that the routines are harmless.
  All four hostile and four suspicious behavior findings remain detected.

  With a 64-character hex key, main reads Discord `.ldb`/`.log` files, locates
  the Discord encrypted-token prefix, Base64-decodes each record, extracts a
  12-byte nonce and 16-byte tag, and decrypts AES-GCM with CNG. It authenticates
  a GET to Discord's current-user endpoint and prints tokens receiving HTTP
  200. It does not recover the key or send tokens to an attacker endpoint.
  The `persist` argument writes a batch launcher and HKCU Environment's
  UserInitMprLogonScript, then loads the Default User hive and writes a Run
  value. The existing hive-load privilege must already be available; the code
  does not grant it. It neither copies the referenced svchost.exe nor supplies
  the required argument on subsequent launches. Short-circuit evaluation can
  prevent the second persistence operation if the first fails. These limits
  preclude claims of successful durable activation, not registry modification.

* **MALICIOUS — @sudobility/testomniac_client 0.0.131**, SHA256
  `eba7da4c1c6b3a22f0cb29ab569f750ce56dd8c62f528ae289df011c262443d8`.
  The manifest advertises a TanStack Query API client. The inspected dist code
  implements ordinary bearer-authenticated Testomniac requests and helpers.
  Its postinstall instead invokes `sh scripts/miner.sh`, automatically fetching
  a gzip carrier from a presigned S3 URL into hidden temporary files.
  Root runs its decompressed shell stage detached. A nonroot installer probes
  passwordless sudo and launches the same stage through sudo when permitted.
  Without elevation it decodes/extracts the embedded miner, writes a RandomX
  pool configuration with a fixed Monero payout and hostname-derived worker,
  copies the executable under a randomly selected daemon-like name, makes it
  executable, and starts it with discarded output. This unrelated resource
  abuse and identity concealment establish compromise, not honest monetization.
  The AWS access-key ID in a signed URL is not an AWS secret-key theft finding.

  Forager retrieved the current carrier, retaining its `.forage.json` under
  scratch/fallout-review/miner-stage. Decompressed stage SHA256:
  `30f0f50a670d5093b6210f20095f0509525a74273da0bfdc5b679b85962edb81`.
  Static extraction recovered five ELF binaries, names/descriptions tables,
  and SHA256SUMS; all seven checksums matched. This verifies container
  consistency, not trust in the attacker-supplied hashes. Rizin identified
  the miner as a stripped x86-64 ELF; its bytes contain RandomX and the hidden
  config path used by the launcher. The stage installs randomly named miner,
  policy and watchdog binaries; decodes agent/watchdog JSON; encodes their
  configurations and appends the miner configuration to its executable; and
  enables policy/watchdog systemd services. The shell shows those installation
  calls and dispatches `agent` to that installer. Its cron fallback writes
  `@reboot # helper cache <path>`, commenting out the command, so working cron
  persistence is not established. The separate `relay` mode includes Tor and
  pool forwarding, but `agent` does not invoke it; automatic Tor deployment is
  not claimed. No specimen was executed.

* **MALICIOUS — semveer 1.0.0**, SHA256
  `d89c112e948539fb785a670d4a585e9a52cea2cf1d0c98db9e21fc29580ef281`.
  The purported utility contains only a version stub. Evaluating setup.py,
  including metadata/build operations, constructs a temp path using the PID,
  downloads an unrelated extensionless Workers-hosted file to that path, and
  passes that same path to Popen. Both output streams go to DEVNULL, a new
  session is requested, and errors are swallowed. This is an undisclosed
  installer payload attempt unrelated to its declared functionality.
  The flow graph and source agree on the saved and launched path. There is
  no chmod: on ordinary POSIX filesystems the newly created file will lack
  executable permission. Successful execution is therefore not assumed.
  Forager received HTTP 404 for the payload, so its contents and eventual
  behavior remain unknown. Three existing hostile traits cover this one
  acquisition-to-execution outcome; they are not three independent malicious
  acts. There is insufficient evidence for a second distinct hostile outcome,
  and no extra conviction trait was invented to satisfy a count.

External corroboration, consulted after source inspection:

* https://github.com/advisories/GHSA-58jf-66x8-7q28
* https://github.com/advisories/GHSA-xh78-qp67-j6mg

The linked SiriusQT article was unavailable through the web reader; the exact
local fixture hash and its saved provenance establish reconstruction identity,
not attribution of this file to a live RAT deployment.

## Trait changes and shared-rule review

* Relocate native Run-key and UserInitMprLogonScript rules from the legacy
  Startup-folder branch to login/registry/run-key and login/registry/script.
  Preserve their predicates, scopes, exclusions and severities. Update the
  exact dual-persistence consumer, fixture expectations and native check IDs.
* Relocate setup acquisition/launch composites to execution/payload/file-exec.
  Their descriptions state the actual co-occurring facts, rather than claiming
  a data-flow relationship not enforced by their matchers. Remove unsupported
  User Execution mappings; package evaluation is not opening a malicious file.
  Add a required process-launch observation to download-execute-chain: its old
  executable-download alternative did not require execution at all. Downloads
  remain separately visible as suspicious. The original external positive
  setup-urlretrieve-exec fixture retains both hostile matches; all three
  existing vendor wheel/library/cache controls retain zero hostile/suspicious
  findings. The download-only control retains its executable-download finding
  without the unsupported launch claim.
* Relocate the postinstall Monero-miner composite from install-hook to its
  mining outcome. Retain every existing mining/masquerade detection, including
  the overlapping package-scope composites; none was removed to adjust counts.
* Move shuf single-item selection from masquerade to os/random/generator and
  make this complete capability notable. Preserve the masquerade consumer.
* Fix base64-decode-to-file: `2>/dev/null` is stderr suppression, not a decoded
  output file. Require stdout redirection, including explicit fd 1, append
  redirection and the common stderr-before-stdout form. Preserve the existing
  makeself decoder/gzip/hidden-execution fixture and its hostile composite.
  Raw Base64 decoding and stderr suppression findings remain on miner.sh.
* Add a structured shell-script launch observation for nohup/sudo -n/sh and a
  hostile elevation composite requiring the existing masqueraded-miner context.
  A normal maintenance launch remains notable; prose/comments do not match.
  The actual miner source passes both conditions, precision 6.3.

Exact and ancestor references were searched. Broad ancestor selectors occur in
Windsurf MCP injection (JavaScript), CrystalX exclusions (PE), and embedded
hosts sinkholes (PE/DLL). The moved setup/miner predicates have no eligible
same-file types in those consumers, so their effective memberships do not
change. They were left unchanged rather than broadening their selectors.
New target directories are existing admitted leaves; no taxonomy split,
package-name exception, IOC gate, signature exclusion or score-driven change
was introduced. See id-map.json for the explicit relocations.

## Verification and comparison

Atomscan used local rules, slow analysis, no updates, and no followed remote
references for consistent before/after comparisons, including every archive
member. Cleave facts was collected for all original artifacts and both package
entry scripts. Downloaded stages were inspected separately, without execution.
Full scans/facts/provenance are under scratch/fallout-review.

* Nine focused static controls pass (`python3 .../check.py`).
* Existing native registry/token checks pass 18 of 20 cases. The other two
  are pre-existing Rust/C# prefix expectations: the unchanged prefix rule's
  explicit for-list excludes those languages. No touched matcher caused them.
* Existing setup positive and three benign controls pass as described above.
* No supported attack finding was lost after mapping relocated IDs. The only
  lost finding is the incorrect Base64 file-output claim, on the npm archive
  and its miner.sh member. Root hostile counts: C++ 4 to 4; npm 3 to 4;
  semveer 3 to 3. Miner.sh hostile count increases from 1 to 2.
* Classifier remains HOSTILE on all three: C++ 0.99859166 unchanged; npm 0.99
  unchanged; semveer 0.99944645 to 0.9993452. The C++ disagreement is retained
  as a provenance-dependent model false positive; behavior traits are not
  suppressed to force agreement. Semveer's aggregate trait risk falls after
  relocation (245 to 130), with all three hostile matches preserved.
* Some package source flow queries report incomplete analysis; source tracing
  supplied the reviewed execution relationships. This is static review,
  not a claim of exhaustive runtime behavior.

Final required check: `make validate` after judgment markers are written.
