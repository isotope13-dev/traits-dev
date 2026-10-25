# Six stranded members: byte-level review

All six members are **MALICIOUS** from their own implemented behavior. The
three supplied archive convictions are retained without rejudgment. Exactly
one verdict marker was written beside each selected extracted member. The
marker notes are reproduced below and in `review.json`; the prepared commit
body is in the task scratch directory.

No specimen, destructive command, or remote payload was executed. Original
SHA-256 values were verified. Every member and original archive received
`atomscan --no-update --follow=none --analyze local --mode slow -f json` and
`cleave facts`. Scans use this checkout, disable report-cache reuse and clear
the upload destination. Raw reports/facts and independently decoded source
remain in `scratch/stranded-current` under the supplied task directory.

## Identities and execution evidence

* **Installer:** universal C++ Mach-O executing an encrypted AppleScript
  credential/wallet stealer. ARM64 entry `0x100000690` reaches `system` at
  `0x1000006b8`; x86-64 entry `0x100000630` reaches it at `0x10000065c`.
  The constructor decodes the buffer before passing its C string to that
  call. Independently applying state `0x11667`, byte XOR and the update
  `((state * 0x3785) & 0xffffffff) % 35999` to 37,077 bytes at file offsets
  `0x4c90` and `0x14de0` recovers identical NUL-terminated commands from both
  slices. The recovered command agrees with Cleave's decoded text.
  Its `osascript` invocation evaluates return-joined AppleScript. The main
  handler reads a cached password or requests it through a disguised
  Installation dialog and validates it with `dscl . authonly`. Reachable
  helpers copy Chromium/Gecko/Safari stores, browser-extension and desktop
  wallets, Keychains, Notes and selected Desktop/Documents files into a
  temporary tree. Recursive wallet copying uses `list folder ... without
  invisibles`, skips named caches and descends through its own helper.
  `ditto` creates a ZIP, curl posts it, and the script deletes staging.
  It downloads Ledger Live replacement content, kills/removes the original
  application and extracts the replacement. A further handler downloads
  command text and inserts it into a bash `-c` LaunchDaemon definition,
  installs/bootstrap-loads it using the captured password and `sudo -S`,
  and has a `nohup` fallback. The daemon specifies the current user's
  UserName; root payload execution is not inferred from privileged installation.
  Broad secret theft, credential deception and persistent command execution
  contradict the presented installation workflow and establish the verdict.
* **parser-session 1.1.9 writer.js:** snapshots all of `process.env`, package
  version, platform, hostname, username and external IPv4-interface MACs.
  Its hex-pair decoder reconstructs Axios, POST, an HTTPS endpoint, header
  keys/value and `then`. The export ignores its input arguments, posts that
  record, evaluates the response's `data` and swallows rejection. This concealed
  export and execution chain is inconsistent with the apparent session/logging
  library purpose. The source's relative package import resolves to a missing
  `src/package.json`; its entrypoint also references a missing writer path.
  Successful activation is therefore unestablished, without erasing the
  implemented theft and evaluation behavior.
* **osinthell 1.6.9 v.js:** the complete exported action calls Node's real
  `child_process.execSync` with forced, quiet, recursive deletion of
  `C:\Windows\System32\*.dll`. Shell execution, ignored streams and an empty
  catch accompany destructive OS-library deletion. It performs no elevation.
* **osinthell f.js:** opens `\\.\PhysicalDrive0` in `r+`, allocates 512 zero
  bytes, writes that buffer through the same handle at disk position zero,
  and closes it. A separate try runs `bootrec /fixmbr`. That command cannot
  restore the partition-table bytes destroyed by the preceding operation.
  Errors and child output are discarded. This is deliberate boot-sector
  destruction, including the partition table, rather than a coherent repair.
* **osinthell p.js:** enumerates C/D/E/F drive roots, joins each entry to its
  originating root, checks for a regular file and writes an empty string to
  that same path using default truncating mode. Nested empty catches continue
  after failures. This destroys arbitrary drive-root file contents; it does
  not recursively traverse subdirectories or securely erase file data.
* **osinthell t.js:** the export silently requests both bootstatuspolicy
  `ignoreallfailures` and `recoveryenabled No` using bcdedit. The first failure
  skips the second command. Fixed paired recovery sabotage, with no maintenance
  interface, establishes its malicious purpose independently of sibling files.

The osinthell entrypoint imports a-z actions and calls them from `sorgu`,
ignoring its argument. Import alone does not run the exports. An earlier
synchronous endless allocation loop in j.js means reaching p/t/v through that
entrypoint is not established. Each member's own implemented destructive effect
still tips its verdict. The deep alphabetic path does not encode its source.

Deployment, user consent, Windows privileges, protected-store access and server
responses are unknown. No runtime success, unseen payload behavior or guaranteed
TCC bypass is inferred. The Installer upload retry omits a handler argument;
successful retries must not be assumed.

## Changes and preservation checks

Add the notable `fs/directory/readdir::applescript-list-folder-assignment`
observation. It recognizes an assignment of Apple's `list folder` result in
source or quoted script lines, including recovered native text. It requires
neither the specimen's names nor its endpoint. It claims no recursion, secret
target, invisible-file listing or hostile intent. This covers a missing
directory-enumeration primitive in the Installer without duplicating an attack.

Correct the misplaced `readdir::cwd-call` observation to
`fs/directory/cwd::perl-cwd-word-reference`: its text-word matcher proves a
current-directory word reference, not a call or directory enumeration. Preserve
its exact matcher, effective Perl/Unix scope, baseline severity and confidence;
remove the unsupported inherited T1083/E1083 enumeration mappings. Update both
exact consumers with their boolean predicates unchanged. A structural comparison
verified that preservation. The sole direct readdir-directory consumer is a
C-only file-infector rule and cannot receive this Perl observation. Ancestor
filesystem selectors retain it under the same filesystem ancestor. No existing
Perl CWD positive fixture was found; new call-shaped and literal-reference
controls verify the retained observation and its intentionally limited claim.
The enumeration leaf remains at 100 rules, with no budget increase or artificial
taxonomy split.

`python3 testdata/stranded-folder-enumeration/check.py` passes nine assertions
across six source-only controls: ordinary/embedded listings, comment and similar
identifier near misses, and retained CWD references. The 22 existing cases in
`stranded-oct24-review/cases.json` pass all 43 assertions when scanned explicitly.
Its older directory-scanning harness also scans its own assertion source and
incorrectly interprets the literal phrase `validation failed` as an engine
failure; the explicit-fixture run avoids that harness problem. The native
credential-dialog suite retains its positive, three near misses and the original
encrypted Installer. Tests inspect bytes only.

## Before/after comparison

H/S are distinct hostile/suspicious IDs. Archive roots inherit member findings.
Classifier values below are calibrated alert levels: -1 is benign, nonnegative
values are flagged. Raw probabilities alone are not verdicts. The installed
model reports feature specification 18 while the engine expects 21.

| Artifact | H before → after | S before → after | Classifier level before → after |
| --- | ---: | ---: | ---: |
| Installer | 17 → 17 | 11 → 11 | 0 → 0 |
| writer.js | 6 → 6 | 6 → 6 | 1 → 1 |
| v.js | 1 → 1 | 3 → 3 | -1 → -1 |
| f.js | 1 → 1 | 1 → 1 | -1 → -1 |
| p.js | 2 → 2 | 1 → 1 | -1 → -1 |
| t.js | 1 → 1 | 3 → 3 | -1 → -1 |
| macOS archive | 17 → 17 | 12 → 12 | 0 → 0 |
| parser-session archive | 6 → 6 | 6 → 6 | 1 → 1 |
| osinthell archive | 5 → 5 | 10 → 10 | 25 → 25 |

Every analysis unit was compared by path and trait ID, including all archived
members. No existing finding was lost or changed. Only the new notable listing
appears, on the Installer and its containing archive layers. Full probabilities,
counts, hashes and deltas are in `review.json`.

The four tiny destructive modules remain classifier false negatives despite
their accurate hostile findings. Each implements one destructive outcome
(DLL deletion, boot-sector destruction, drive-root truncation or recovery
sabotage); p.js retains two overlapping accurate hostile traits. Investigation
of every statement and its call arguments found no additional stage, persistence,
theft or escalation to support three distinct hostile behaviors per member.
Their execution/I/O/error-suppression primitives are covered. No matcher
limitation prevents coverage of the evidenced outcomes; no duplicate or inflated
rule was added to meet the numeric goal.

The six marker lines, prepared verbatim for the commit body, are:

```text
Installer stealer: phishes and exports secrets; add folder listing
parser-session writer: concealed environment theft and reply eval
osinthell v.js: silently deletes Windows system DLLs
osinthell f.js: zeroes disk boot sector and partition table
osinthell p.js: truncates arbitrary drive-root files
osinthell t.js: silently disables Windows boot recovery
```
