# Supply-chain benchmark v1

This corpus originally contained 315 package-shaped static-analysis fixtures: 15 per
cleave-supported package-capable source language, split five each across Linux,
macOS, and Windows. Nine scenarios per language conceal their action specification.

Every activated path requires both the random environment-variable name and value
recorded in `manifest.jsonl`. Activation writes only the decoded specification to a
temporary canary file, starts only a harmless local child, and connects only to the
discard port on `127.0.0.1`. Realistic reserved `*.example` hostnames appear solely
in the loopback HTTP Host header. Named credential and persistence targets are never
opened or modified.

Triage on 2026-09-14 moved five confirmed non-hostile canaries unchanged to
`/tmp/triage/misplaced-good/supply-chain-benchmark-v1`: Python Pathweaver,
JavaScript Resourcecove, Elixir Fontstream, and Ruby/PowerShell Profileloom.
Triage on 2026-09-15 deleted the remaining 14 JavaScript packages after reviewing
their manifests, entrypoints and decoded resources. Their attack descriptions
were only data written to temporary files, never executed. These were not useful
hostile simulations and would require wholesale replacement, not a bounded fix.
The deleted archives were verified byte-identical to Git HEAD and are recoverable
from Git history. No JavaScript packages remain in this v1 hostile corpus.
The same static review then deleted all 15 TypeScript packages: they were the
same canary template with type annotations and also required wholesale
replacement. They are recoverable from Git history. No TypeScript packages
remain in this v1 hostile corpus.
The 15 C packages were also deleted after static review. Their CMake projects
declared executables but supplied no `main`, so they could not link; their
constructors otherwise repeated the canary-only behavior, and bundled PNGs were
never read. They are recoverable from Git history. No C packages remain here.
All 15 C# NuGet packages were then deleted for the same canary-only behavior.
Their MSBuild targets depended on the external `dotnet script` tool and their
attack descriptions were never executed. They are recoverable from Git history;
no C# packages remain here.
All 15 Go modules were also deleted. Six plain variants did not compile because
of unused imports; the nine compilable concealed variants still performed only
the canary behavior. They are recoverable from Git history; no Go packages
remain here.
All 15 Rust crates were deleted as well. Their real Cargo build-script hook only
performed the same temp-canary, harmless-child and loopback behavior, so fixing
them required wholesale behavioral replacement. They are recoverable from Git;
no Rust packages remain here.
The remaining 14 Python packages were deleted after the earlier Pathweaver move.
Their setup hooks executed only the same canary routine. They are recoverable
from Git history; no Python packages remain in this hostile corpus.

The original `manifest.jsonl`
and `SHA256SUMS` remain provenance records, not a current inventory. The remaining
207 packages still need individual disposition; canary-only behavior must not
be counted as demonstrated attack detection. See the root
[audit report](../../../SUPPLY_CHAIN_AUDIT.md) for hashes and review results.

Original counts: {"c": 15, "csharp": 15, "elixir": 15, "go": 15, "groovy": 15, "java": 15, "javascript": 15, "kotlin": 15, "lua": 15, "objectivec": 15, "perl": 15, "php": 15, "powershell": 15, "python": 15, "ruby": 15, "rust": 15, "scala": 15, "shell": 15, "swift": 15, "typescript": 15, "zig": 15}
