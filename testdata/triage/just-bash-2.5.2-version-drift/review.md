just-bash 2.5.2: BENIGN

Artifact SHA-256: 9c225d819ad84cb352e8b682a50ac7e7f248e9aff766f51c230cb4002a66b7f5.
This is the TypeScript virtual-filesystem Bash implementation, including its
library, browser bundle, CLI, and interactive shell.

Release evidence

Fetched pkg:npm/just-bash@2.5.1 with forager, retaining its provenance in
scratch/version-drift/earlier. Its original npm archive has SHA-256
e618f6c7601ab903c1430f6f2734a93969b8827f30e84feb355d265a9c7b40cf.
Both archives have 500 members. No members were added or removed; 495 are
byte-identical. Only package.json and four entry bundles changed. The manifest
changes only version; dependencies, entrypoints and scripts are unchanged,
with no install lifecycle hook added.

The changed code implements multi-segment glob expansion: hasGlobChars detects
glob syntax, expandSimple separates the literal prefix, and expandSegments
walks matching directories through the supplied filesystem. It handles hidden
names, directory entries and filesystem implementations without typed readdir,
then returns sorted paths. It does not send the paths anywhere or execute them.
Token comparison of all four bundles is equal outside these three methods after
normalizing identifiers. This supports ordinary minifier renaming elsewhere.

The flagged jq chunks, including both bin copies, are byte-identical in 2.5.1.
Current rules reproduce the same suspicious finding on that earlier archive,
contrary to the queue's historical clean result. The queue history therefore
is not evidence that this release introduced the flagged behavior.

Behavior traced

The jq evaluator recursively dispatches its parsed AST. Its sub and gsub cases
consume the user's pattern, replacement and flags, construct RegExp objects,
and return the replaced input as data. These are two separate switch branches,
not an encoded-token recovery loop. No JavaScript eval consumes their output.
The encoded-string matcher reports zero decoded strings in the flagged chunk;
its Base64 encode/decode cases implement jq format operators, not a payload.

The entry library only creates its secure fetch wrapper and registers network
commands when configured with network options. Requests and redirect targets
are checked against configured URL prefixes and methods. The supplied CLI uses
a filesystem overlay, and command registration writes shebang stubs through
that filesystem interface. Those writes are legitimate observable behavior
and remain notable. No host shell launch is established by just-bash -c in help.

The scanner-followed node-liblzma@5.1.3 artifact is not newly introduced code in
this release: the optional dependency declaration is unchanged (^2.0.3), and the
unversioned dynamic import and installation-error text are unchanged too.
The inspected fetched package loads its native compression binding using
node-gyp-build; its build scripts acquire and build XZ. Its automatically
resolved version must not be attributed as an exact deployed dependency of the
supplied archive.

The balance of evidence supports BENIGN: a conventional glob fix, unchanged jq
implementation, and behavior consistent with the advertised interpreter.
Deployment scripts, caller-provided commands, custom filesystem implementations
and optional network configuration were not supplied. No deployment intent is
inferred from them. Static analysis reports local-flow limitations; the verdict
also rests on manual control-flow review and the archive diff.

Rule corrections and preservation

- Relocated repeated variable-pattern RegExp replacements to notable string
  replacement capability. Removed argument-name and file-wide sanitizer
  exclusions, which are inappropriate for that neutral observation.
- Added a replacement-result provenance atom at the direct eval sink. The new
  suspicious regex-substitution composite requires that result to reach eval;
  a separate evaluator elsewhere in a bundle is insufficient.
- Retained the parallel-array/flag token-substitution composite and its WSH
  consumer using the neutral replacement atom, so execution through WScript
  need not use JavaScript eval to remain covered.
- Consolidated js-eval-named-script-variable into the existing variable-argument
  evaluator. Source/script/module identifier suffixes do not add another
  capability. The retained evaluator additionally binds argument zero, avoiding
  the old match on a later, unevaluated argument. No exact consumer required the
  removed name; existing direct-argument and later-argument controls apply.
- Narrowed the /chunk route boundary to exclude chunk-*.js module imports.
  The native browser-theft and Aokigahara consumers still reference the same
  route atom; actual /chunk paths, query strings and suffix paths remain matched.
- Corrected the Bash command boundary so just-bash -c is not a Bash launch.
  The existing executable reverse-shell fixture still matches bash-exec.
- Moved the expect symbol observation out of package test-fixture metadata and
  updated both exact consumers. A parser method named expect proves no testing
  role. Removing that accidental test context exposes the accurate embedded
  shell-text writes; their description now also fits virtual filesystem writes.
- Removed the misplaced chunk-js-name duplicate and retained the canonical
  metadata/build/bundler/asset hash-basename observation. Its surviving exact
  consumer uses that canonical rule; the other reference was already subsumed
  by metadata/build/. The old basename language is a subset of the canonical
  matcher, and consumer type, platform and size restrictions remain.
- Moved the /proc/self/status reference from sandbox detection to the existing
  proc path leaf, tar append/extract text from collection/C2 to archive
  capabilities, and Google copyright attribution from product identity to
  license metadata. Matchers and effective scopes are preserved. All exact
  consumers were updated. No ancestor directory consumer selected the removed
  tar, sandbox or Google atoms; the broad obfuscation-string consumer is an
  ELF-only anti-debug composite, outside these JavaScript observations.

Retained controls include the pre-existing regexp-token-substitution-loop.js,
corpus-with-executable-reverse-shell.js, relay-eval-callee fixtures, and Google
loader/reference fixtures. New controls cover jq operations with an unrelated
eval, recovery beside a sanitizer, module imports versus real /chunk requests,
hyphenated command help, and the relocated archive/path/copyright observations.
The command-help near miss was also checked outside testdata so test-path
exclusions could not supply the result. Actual token recovery still matches,
including when a sanitizer elsewhere would previously have suppressed it.

Scan comparison

The supplied archive has hostile/suspicious counts 0/1 before and 0/0 after.
Each of the three flagged jq archive members changes from 0/1 to 0/0; there are
no remaining hostile or suspicious findings anywhere in the scanned tree,
including a separate rescan of the followed dependency. Its hostile/suspicious
counts remain 0/0. Notable behavior coverage is retained:
322 distinct archive-level notable traits before, 323 after. Trait moves retain
the supported procfs, archive and attribution observations under neutral IDs;
regex replacement and virtual shell-text writes remain detectable.

The static score changes from 123 to 83. Both calibrated model routes remain
class 0, with no calibrated suspicious level (lvl -1). The npm-route probability
changes from 0.048284072 to 0.00085169077; the aggregate probability changes from
0.8205476 to 0.68599147. Those uncalibrated values do not override the verdict.
The final automatic follow pass no longer includes node-liblzma@5.1.3, so the
aggregate probability comparison includes a changed fetched-artifact tree.
The same checksummed dependency was fetched and rescanned directly; its high
raw aggregate probability still has calibrated class 0.
The model advertises v18 features while the analyzer expects v21, a recorded
model-version limitation. No material attack coverage was removed, and there
is no remaining classifier/verdict disagreement.

Output-only coverage differences were investigated. The final archive report
omits two 20-byte members containing only a Node shebang. On one tar member,
three union wrappers (file writes, decompression, Web Compression Streams) are
no longer printed. Direct test-rules checks still match all three, and their
primitive operations and archive-level coverage remain. The debugger explicitly
labels these wrappers as low-value any/needs-one findings filtered from output.
No corresponding matcher was weakened. Other disappeared low-tier vocabulary,
loop and string-operation findings were not edited or given exclusions.
