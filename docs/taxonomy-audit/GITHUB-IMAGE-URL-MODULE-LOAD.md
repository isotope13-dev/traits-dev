# GitHub image-suffix URL and module-load classification

## Finding and placement

`raw.githubusercontent.com/...png` is URL text. The suffix alone does not
establish that the response contains an image, that image bytes conceal code,
or that encryption occurred. The atomic `raw-githubusercontent-image-suffix`
clue therefore belongs in the neutral
`micro-behaviors/communications/http/url/github` directory. Its scope now
inherits that directory's language-neutral URL scope; it retains notable
criticality, confidence, matcher and icon URL exclusions. Its effective
mappings now follow the neutral HTTP URL defaults (`T1071.001` / `C0002`)
rather than the former encrypted-dropper defaults.

The two composites require a runtime assembly loader, so their canonical
objective home is `dropper/module-load`. They reference the neutral URL clue;
the second also requires the PowerShell RC4 state-table observation. Their
existing descriptions, severity, confidence, mappings, Windows/PowerShell
defaults, matcher legs and 4 KiB `near_bytes` window remain unchanged. The
encrypted-staging leaf is therefore reduced by three rules and the module-load
leaf gains two.

This placement follows the required activation sink rather than the URL's
filename or presumed encryption. The evidence supports a probable remote
assembly-load chain; it does not prove the URL response is the exact byte array
passed to `Assembly.Load`. The short proximity bound is retained as the rule's
heuristic, so this chain-level inference remains a candidate for future
dataflow-aware matching.

## Verification and cap impact

Two synthetic PowerShell samples were checked with cleave `test-rules`. The
image-suffix URL plus `WebClient.DownloadData` and `[Reflection.Assembly]::Load`
matched the first composite with all three legs within 4 KiB. Adding a 0..255
state-table expression matched the RC4 composite. The URL atom also matched a
C# source sample, confirming it is no longer tied to PowerShell file type.

The current 100-rule audit reports `dropper/staging/encrypted` at **188**
(37 atomic, 151 composite), still **88** over cap; `dropper/module-load` is
**20**, within cap. Catalog-wide counts remain **79** violating directories,
with **1,988** excess rules. See the refreshed current snapshot for full
directory and overlap measurements. The latest soft validation reports 83
issues in 10 locations, including the 79 cap violations, and exits nonzero on
existing unrelated checks and the known benign archive fixture findings. It
reports no unresolved references for these moves.
