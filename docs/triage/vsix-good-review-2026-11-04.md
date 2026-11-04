# VSIX mislabeled-good review, 2026-11-04

The initial pool contained 40 archives. A slow local Atomscan directory scan
finished with 40 JSON records at `/var/tmp/vsix-good-scan.jsonl` (exit 2,
indicating severe findings). It began before the rule changes below, so the
records are preliminary. Each archive and its contents still require endpoint-
based review and final classification.

* `72b2b5ac83ca`: Python autopep8 extension with five ZIP members. Its active
  handler concatenates the editor filename into a shell command without quoting.
  This is an ordinary formatter extension with a command-injection weakness.
  A linked-source-and-sink finding now reports that risk. The rescan reports
  this one suspicious finding; Hopper confirmed the good label (no-op).
* `20c6cba50f6e`: Lua Debug contains a macOS x64 executable whose bytes have
  a LuaJIT version banner, bytecode preload format, and LuaJIT command-line
  help. The generic AMOS cipher-variant heuristic falsely matched this member.
  A Mach-O LuaJIT CLI identity now guards that heuristic; the individual member
  rescan no longer reports it. The rest of the archive still needs review.
* `37970fc037c9`: Batchitt is a chat extension whose webview authenticates with
  a service-issued key and communicates with its own chat service. The key is
  inserted into the login URL path, an unusual security-relevant choice that can
  expose it in URL logs. The former finding inferred capture from unrelated
  co-occurring signals; it was replaced by neutral co-occurrence observations
  and a separate linked-input-to-URL finding. The full archive rescan reported
  that single suspicious finding. Endpoint ruling: good; Hopper confirmed the
  existing good label (no-op).
* `4331210f8b4d` and `6a289d3d93fc`: RTL Cursor versions 1.0.11 and 1.0.13
  patch the editor to enable right-to-left rendering. When enabled, they install
  a per-user Run-key watcher to reapply the local patch and remove it on disable.
  Their shipped code was inspected for network and command execution; the
  watcher is local. Both now report the Run-key write and one suspicious hidden
  PowerShell policy-bypass launch. The latter was previously missed in 1.0.11
  because whitespace exceeded the proximity limit. Ruling: good, with one
  unusual finding each; Hopper confirmed the existing labels (two no-ops).
* `5809dcfcdfcb`: terminal-failure sound extension. Its Windows playback path
  starts a hidden PowerShell process with execution-policy bypass and sends a
  Base64-encoded bundled WAV to a sound player; the encoding is audio data.
  Its shipped code has no observed remote transfer. The hidden-process rule
  now handles the bundler's `(0, x.spawn)` wrapper and `windowsHide: !0`; the
  archive rescan reports this one suspicious finding. Ruling: good; Hopper
  confirmed the existing label (no-op).

Five Vibrancy Continued versions (`c524af5a2ffb`, `37d206f0a8f8`,
`3628df0fcdcb`, `8476c183b87c`, and `89304290d276`) install visual changes
by modifying editor resources. Their uninstall hook launches a hidden
PowerShell cleanup script, explaining the existing suspicious finding. Their
HTML transform adds a named Trusted Types policy to the workbench CSP; a new
notable observation reports the CSP reference alongside the text replacement.
The extension code and native source were inspected, and both architectures
of the native binaries import only `KERNEL32.dll` directly. The 1.1.86 release
also creates a writable NixOS editor mirror and desktop entry. These are
provisional good rulings pending validation. Slow local Atomscan rescans with
reference following disabled report the CSP observation and one suspicious
hidden-PowerShell finding for each, with no hostile traits. The CSP observation
also matches all five actual transform files and rejects controls missing the
CSP reference or the trusted-types replacement. A current `make validate`
run fails on a duplicate reward-claim matcher in unrelated concurrent changes;
the five labels have not been recorded yet.
* `b2efc28a78a4`: Commit Defender installs a repository pre-commit hook, reads
  staged diffs and sends review content to a configured AI provider. Its hook
  installer asks before replacing an existing hook and stores its configuration
  with owner-only file mode. The new staged-diff helper finding complements
  existing hook and HTTP findings. The archive rescan has no suspicious or
  hostile findings. Endpoint ruling: good; Hopper confirmed the existing label
  (no-op).

The initial scan also flagged `d504a4d979ac` (Kombai) and `af55e4111d3d`
(CodeGPT) for several behaviors, including fingerprinting or browser/automation
clues. Kombai's entry point attaches the output of `getFootprintV2` to client
context sent to its own authenticated WebSocket and uses the same helper in an
HTTP header. Its lazily loaded runtime is heavily obfuscated and its full
fingerprint contents are not yet understood; no final endpoint ruling has been
made. A hostile exfiltration claim based only on fingerprint, lazy loading,
VS Code and socket/header references was relocated to capability observations
that state co-occurrence. Its main JavaScript rescan no longer reports that
hostile claim; the obfuscated runtime retains its suspicious finding. The scan
also fetched npm `optimize` and Google Chrome packages from referenced URLs
(`rel: fetched`); they are not necessarily bytes bundled in the VSIX and must
not be attributed to it without following the reference chain.

A total of 34 archives remain to be reviewed, including those two and Lua Debug;
the scan is not evidence that unflagged files are safe.

Both `bbb21a99269f` (Memory Vault) and `745bc96b9baf` (Quokka) contain the
same `tar-fs/test/fixtures/invalid.tar`: it has symlink `foo -> ../` and a
`foo/bar` file containing `hello`. The adjacent test code extracts it and
asserts an outside `bar` is not written. The JavaScript harness actively sends
the crafted archive to the extractor and checks the outside path, so it is an
executable path-traversal test under the requested PoC policy. Both containing
archives are provisionally bad; do not relabel until hostile findings in two
directories cover their actual content and the remaining members are reviewed.
Quokka additionally has findings in a fetched Twisted package. The scan's
parent chain runs from the bundled `pythonTestWorker.py` to a fetched pytest
wheel, then from its `_pytest/unittest.py` to the fetched Twisted wheel. The
Twisted test bytes are therefore not evidence of a file bundled in the VSIX.

The traversal fixture now has a structural hostile trait for a root symlink
pointing above extraction followed by a file below that link. A second hostile
trait requires the matching `invalid.tar` fixture and JavaScript extraction and
outside-path check within the same archive. A small ZIP containing the actual
bundled fixture and harness produces both findings; safe-link, missing-harness,
wrong-name, unrelated-child, and non-root-link controls do not. The harness
test also includes an earlier unrelated extraction call.

Normal archive scanning initially missed the inline YARA trait even though
`cleave test-rules` matched it. The archive analyzer now evaluates inline YARA
against the original archive bytes; a scanner unit test covers standalone and
nested containers and a YARA-disabled control. The focused traits test and
`make validate` pass. The Quokka scan before the harness-rule correction found
the structural payload; a final full scan and updated atomscan verification
are still needed. A full Memory Vault rescan ran out of memory during concurrent
builds. A retry grew beyond 75 GiB and was stopped to protect the shared
machine; its `RAYON_NUM_THREADS` setting did not limit this scanner, which uses
`CLEAVE_RAYON_THREADS`. A retry with the correct four-thread setting grew past
35 GiB during member analysis and was stopped; limiting concurrency alone did
not resolve the problem.
The updated atomscan build also encountered an unrelated rebase
in the neighboring scanner checkout; no rebase files were changed for this
review. Neither provisional classification has been moved.

Memory Vault also contains three byte-identical copies of the PyInstaller
executable `memory-vault-fixing.exe` (SHA-256 `e0476df0ef1d111bc7c99d16ce483ead493cde11abe937623213caa7d8922978`).
Its bundled Python 3.11 entry point was extracted and disassembled without
execution. It creates the local `.memoryVault` directory and SQLite note/code
tables, then displays a Windows message box; the entry point contains no network
or process-launch behavior. This does not by itself clear every bundled member.

`test-macho-luajit-identity.py` builds minimal Mach-O objects to verify that all
three runtime identity signals are required. The individual real member was
extracted to `/var/tmp/vsix-luajit-darwin.bin` for inspection and rescan.
The test and `make validate` passed after the guard was added.
`test-vsix-login-evidence.py` checks the independent observations and the
specific input-to-login-URL pattern, including missing-source and missing-sink
negatives. `make validate` passed after those changes.
`test-vscode-filename-shell.py` checks the formatter's filename-to-shell flow
and negative cases using a different source, a different argument, `execFile`,
or an escaped argument. `make validate` passed after that rule was added.
`test-vscode-fingerprint-context.py` checks fingerprint/header/socket evidence
and negatives, and verifies an independently supported concealed-enrollment
exfiltration fixture remains hostile. `make validate` passed after the migration.
`test-node-run-key-command.py` verifies Node `reg add` writes to Run keys and
rejects queries and unrelated keys. `test-node-hidden-powershell.py` binds the
two PowerShell switches to one call, including reversed order and negatives
where switches are split across calls. Both tests and `make validate` passed.
The PowerShell test also covers bundled calls and both `windowsHide: true` and
`windowsHide: !0`, with `!1` as a negative; the focused test and validation pass.
`test-node-staged-diff.py` checks the Git-helper staged-diff call and negative
cases; the focused test and `make validate` passed.
