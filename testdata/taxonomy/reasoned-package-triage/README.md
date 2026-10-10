# Reasoned package triage

Samples reviewed: passwordcrackv2 1.1.1 (ae1e18b92d79), KNSoft.NDK
1.2.76-beta (fa1811ff81b4), agentic-qe 3.15.0 (8de2604b9112).

## Judgements and behavior

* MALICIOUS: passwordcrackv2 presents a Discord MFA client but cache.js
  executes module['require']('node-net-pool'). The mutable GitHub dependency
  fetched in isolation has SHA256
  163fd559733da0edac2341acb94f9f5aa0aadadb038b051989d627bea03c7808.
  Its index.js downloads an attachment-hosted JavaScript payload, writes it
  under APPDATA/LOCALAPPDATA or TEMP with system-like names, and runs it hidden.
  Generated VBScript installs Run, RunOnce, UserInitMprLogonScript and Startup
  shortcut entries, sets hidden/system attributes, and deletes the installer.
  It periodically checks payload content-length and replaces/relaunches it.
  This concealed persistence is unrelated to connection pooling or MFA.
  No external malware report was found; conviction rests on these bytes.
* BENIGN: KNSoft.NDK is Windows NT declarations and import libraries.
  Hotpatching.h declares structures, information classes and NtManageHotPatch,
  without calling it or removing hooks. MSBuild targets set include/library
  paths and link ntdll.lib. WinAPI.lib contains 414 COFF short import objects;
  no launcher, install payload or malicious implementation was found.
  Identity corroboration: https://github.com/KNSoft/KNSoft.NDK
* BENIGN: agentic-qe is bundled quality-engineering CLI/MCP tooling.
  Preinstall checks previous global versions and only removes them in explicit
  migration mode; postinstall is a no-op. Bundles invoke test runners and
  configured LLM providers, write test/coverage artifacts and manage agents.
  Its optional guidance integration compiles policy documents and supplies
  enforcement gates, local ledgers and headless agent execution.
  @claude-flow/guidance 3.0.0 was fetched/scanned separately before and after
  edits; no hostile or suspicious findings. No theft or covert control found.
  Identity corroboration: https://github.com/proffesor-for-testing/agentic-qe

## Trait corrections and placement review

* Move NtManageHotPatch to kernel/control, notable, without anti-AV mapping.
  The API reference is a kernel facility, not ntdll unhooking. Word matching
  excludes identifiers that merely contain the API name.
* Move Discord vanity/MFA authorization endpoint co-occurrence to HTTP OAuth,
  notable; remove credential-theft mappings. User-provided authentication is
  not token theft.
* Retire phantom URL dependency conviction composites. Unresolved imports,
  mutable URLs and bracket require do not establish hostile behavior.
  Retain underlying dependency/import observations and describe the single
  unresolved-count fact accurately. The engine misses this bracket require.
* Retire conditional-cleanup inference: FileExists on a version file and
  DeleteFile on ScriptFullName do not establish a conditional self-delete.
  Consumers use the direct self-deletion pattern; the HTA consumer retains
  its original file-check requirement separately.
* Relocate the remote WSH dropper to execution/payload/file-exec and update
  both exact consumers. Remove inherited B0024/F0011 mappings: these
  conditions do not establish a single-instance mechanism.
* Relocate generic variable-program/variable-argument spawn out of the Python
  dropper directory; its matcher proves neither Python nor a staged path.
* Relocate nearby CreateShortcut/Startup vocabulary to autorun/login-items.
  Retain the original matcher and gate the hostile stager consumer on it.
* Remove generic Run-key findings labeled AgentHub/systemd. Reuse the neutral
  Run-key path and WSH executable observations in autorun/login-items; update
  the AgentHub consumer. The neutral path recognizer also accepts RunOnce,
  escaped separators and case variants. No AgentHub identity is inferred.

Exact references and ancestor selectors were searched. No broad detached
dropper leaf selector required amendment. Kernel/control has an existing
SIM-command consumer requiring separate SIM channel/command evidence; an
ordinary hotpatch declaration alone cannot meet those conditions. HTTP OAuth
remains neutral. Other service-template traits in the AgentHub file were
outside these samples' firing population and were not changed.

## Verification

Ran atomscan and cleave facts on all three archives and inspected source
and discovered literals/calls. Scanned the GitHub dependency separately and
verified the downloaded hash matches the dependency folded into the parent.
Rizin did not identify code in WinAPI.lib; direct COFF archive inspection
confirmed import-object structure. Used binwalk for archive inspection.

Positive and near-miss fixtures cover hotpatch API declarations, MFA endpoint
co-occurrence, variable spawn, Startup references and WSH/Run-key co-occurrence.
The dropper's test-rules precision was 9.3 (required authoring minimum 3.5).
Both independent hostile dependency composites remain matched after correction.

KNSoft: zero hostile/suspicious YAML findings. Agentic QE: zero
hostile/suspicious YAML findings (1482 notable observations). Its ML score
remains elevated (~0.77); no arbitrary suppression was added to force a model
verdict. Static flow analysis reports limitations on large bundles; this is
not a claim of exhaustive dynamic execution. This atomscan build rejects
--explain; structured JSON and cleave test-rules supplied the match evidence.
