# Builder review

PyInstaller spec-name matches and their freezer-install combinations are now
under PyInstaller, with their descriptions limited to the filenames and
commands observed. MSBuild references and related configuration clues are
under MSBuild; the owner/build ID and fake-code comments and a sleep call do
not themselves establish a dropper factory or exfiltration. The Luckyware
consumer still uses the same combination of match conditions.

Python g++ and Rust cargo workflows follow compiler invocation and their path,
header or wording evidence. Ordinary compiler use and a C header do not alone
establish malware. VBA auto-open, Base64 and stream clues retain a suspicious
reconstruction objective; ShellExecute text near a csproj does not establish
that MSBuild ran it, so the auto-open combination describes those clues.
Match conditions and exclusions were preserved; over-specific technique tags
and hostile severities were removed where they lacked support.

The C executable-writing pattern retains a suspicious builder objective, with
its `CreateFile`, `WriteFile`, random-buffer and UPX observations described
separately; the two WriteFile patterns can match the same call. The Go
staged-upload, stub and compiler names are observations, while their
combination with encryption and a TLS listener supports a likely crypter
builder. A related TLS builder profile was moved out of metadata because it
requires behavioral capabilities.

The dnlib import and module-load call are tool-specific. A string-opcode and
`BuildInfo` field combination indicates assembly inspection and configuration
clues, not necessarily an implant or an operand patch. Generic task-list and
control URL paths are not by themselves a malicious builder panel.

Adding dnlib exposed a 151-subdirectory development-library directory.
Existing parser libraries, Babel packages and TypeScript definition packages
were grouped by their actual product roles; their individual IDs and directory
selectors were updated. Broader development-library selectors remain
recursive. The parent now has 134 rule-bearing subdirectories, leaving room
for new families without changing the limit.

A CreateFile call naming an EXE can open it for reading, so that atom lives
with operation references instead of file-write API evidence.

The .NET builder review separated generic placeholder and UI strings from
RunPe method names, resource/compiler references, and unmap/process API-name
combinations. Neither an API name nor an `Encrypted` string establishes a
loader, actual injection, or encrypted data. The title matcher combines names
of multiple crypters and the unscoped binary strings are kept as observations
rather than attributed to a single tool. A combination of compilation,
resource, placeholder and crypter-specific UI/title clues remains a hostile
concealment-builder finding. The existing placeholder consumers retain the
same conditions, as do the resource rule's exclusions. The former broad
downgrade was removed: after reclassification it would reduce this concrete
resource-and-crypto observation to baseline, including on filename evidence.

The final legacy builder rules now distinguish Python source generation,
compilation, Base64 and marshal evidence from probable backdoor construction.
The old EXE-to-batch label required binary-read and batch/encoding clues but no
EXE filename or bound conversion, so the capability now describes those
clues. An npm C2-panel rule and its Solana consumer no longer claim a builder
solely from dependencies.

The neighboring compilation leaf was divided by operation: build-system
orchestration is in `generation/build`, and source compilation stays in
`generation/compile`. MSBuild-specific text moved with MSBuild or to a command
reference. An existing bot-construction objective moved out of the crowded
implant leaf; its header and filename observations moved to their subjects.
