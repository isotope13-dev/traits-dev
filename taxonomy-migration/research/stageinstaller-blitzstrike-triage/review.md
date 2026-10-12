# StageInstaller and Blitzstrike triage

The Kotlin and Java StageInstaller snippets implement the same operation: start
`sh -c pm disable com.android.vending`, wait, create a full PackageInstaller
session, stream the provided APK, fsync, and commit. The result callback runs
`pm enable com.android.vending`. There is no network acquisition, APK provenance,
installer impersonation, privilege acquisition, or family-specific identifier.
The malicious finding is targeted verification blinding during deployment,
not ordinary sideloading. Bitdefender independently documents this exact
sequence in Midnight Mimosa; the excerpts alone do not establish that family.

Source: https://www.bitdefender.com/en-us/blog/labs/midnight-mimosa-malware
Mapping: https://attack.mitre.org/techniques/T1629/003/

Blitzstrike 2.4.178 is an MIT-licensed MCP penetration-testing CLI. Its npm
manifest has no installation lifecycle hook. The readable Bun bundle dispatches
explicit CLI commands and registered MCP tools. Request-smuggling probes take
a caller-supplied target, send baseline and malformed requests, and compare
follow-up statuses. SQL delay probes carry true/false controls; OOB resolution
and listeners are assessment capabilities. There is no demonstrated covert
collection, autonomous exploitation, hidden backdoor, or credential export.
Its Markdown skills/manuals and declared detector corpus are documentation and
benchmark input. JSON chains and technique catalogs are data, including records
larger than the engine's JSON parser budget. Public provenance agrees:
https://github.com/shinthink/blitzstrike

## Trait corrections

- JVM ProcessBuilder source observations moved from spawn to subprocess;
  exact consumers were updated. Constructor, shell-start and APK commit
  observations stay notable. Shell command matching uses literal and parsed
  constructor facts because Kotlin live AST call matching is unavailable.
- Android objectives require a started disabling command, a full APK write/
  commit sequence, and disabling before the write. The evasion observation
  additionally requires the restoration command. Neither relies on class or
  sample filenames. Installer atoms no longer claim process injection (T1631).
- Root/mount/process co-occurrence moved into neutral mount capabilities;
  it establishes no sandbox escape. Local PTY promotion is no reverse shell;
  the canonical PTY observation remains notable.
- GET/POST fetch/open and GET-selected includes moved out of webshell/infection
  namespaces; exact consumers reference the supported observations. Variable
  eval stays notable and system(variable) uses its existing canonical atom.
- Telegram/process/OAST co-occurrence and its orphan component aggregates were
  removed: they prove neither Telegram-library identity nor substitution.
- Probe, fenced detector-case, authorized engagement guide and structured
  catalog exceptions use file-local content. No archive name, sample hash,
  package name, blanket tool identity, or dependent-package exemption was added.
  Repeated paired catalog fields also work above the JSON parser size limit.
- The plain word authoritative and ordinary sensitive-topic directives no
  longer imply prompt injection. Explicit deceptive authority or concealment
  remains required.

Directory selectors were audited alongside exact references. Neutral fetch/
include observations no longer serve as webshell or infection evidence through
old directory selectors. JVM wrappers leave the mechanism-specific spawn
selector intentionally; process/create ancestors and exact wrapper consumers
still select the supported capability. No taxonomy leaf was introduced.

## Verification

Initial atomscan runs followed the environment's optional references and also
fetched external tools, including LinPEAS. Final local-artifact scans unset
SCAN_FETCH to distinguish the supplied bytes from optional fetched references.
The supplied finding list contains no dependency-origin PURL; the corrected
findings are in Blitzstrike's own bundle, data, and documentation.

Cleave facts were captured for all three supplied samples and the alert-bearing
bundle/Markdown members. The supplied SHA-256 hashes were verified. Gzip decompression and tar inspection
confirmed 585 package files and conventional zero tar padding; binwalk was not
installed despite the task description. Source was read and traced statically; these are source
and archive artifacts, so native disassembly is not relevant. No sample was run.

control-findings.json records nine independently scanned controls outside any
test-named path. Ordinary install, other-package disable, missing commit,
commented commit and comment-only source have no hostile/suspicious findings.
Renaming the installer retains both hostile detections. A bare PHP callback
retains its webshell detections, while its declared fenced regression case has
none. Local Python PTY startup has no reverse-shell conviction.

Each final Android scan has two hostile findings in separate objective leaves.
All 578 local archive analysis units have zero hostile/suspicious findings.
The hostile composite precision scores exceed 3.5. Judgement markers are saved
beside the supplied samples; the final repository action is make validate.

Full validation caught four prompt-injection coverage regressions and an extra
benign-document score point. Explicit deceptive authority, user-unaware action,
undocumented injected calls, and blanket invalidation of vulnerability reports
retain coverage. Generic fence duplication was removed; meaningful fixture
declarations and manual/skill structure still drive the documentation exceptions.
