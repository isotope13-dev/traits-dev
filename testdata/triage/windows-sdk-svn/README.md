# Windows SDK includes and Subversion property triage

All three supplied artifacts are **BENIGN**. Verdicts follow source and byte
analysis, independently of their external labels and atomscan probabilities.

## Identification and execution paths

* `b40889aa25a7/prsht.inl`: Microsoft Windows SDK isolation-aware property-sheet
  wrappers. The five wrappers resolve `CreatePropertySheetPageA/W`,
  `DestroyPropertySheetPage`, and `PropertySheetA/W` from `Comctl32.dll`, cache
  typed function pointers, and forward caller arguments. They activate an
  assembly context, adjust `PSP_USEFUSIONCONTEXT` and `hActCtx` where applicable,
  and restore the context and last-error value in `__finally` cleanup.
* `0fa18546d671/dpa_dsa.inl`: the corresponding SDK wrappers for dynamic
  structure arrays, dynamic pointer arrays, and `Str_SetPtrW`. Creation,
  deletion, item access, cloning, growth, comparison, merging, callback
  enumeration, and stream serialization are forwarded to common-controls
  exports. Callback and IStream parameters originate with the caller; the
  header supplies no payload, network endpoint, or automatic entry point.
  Lazy-resolution failures return defaults; some wrappers retain the
  activation context through the API call and others only through resolution.
* `3e8f073fcf77/gpl.txt.svn-base`: a complete 30-byte legacy Subversion
  serialized property hash, despite its license-like basename. `K 14` introduces
  the 14-byte key `svn:executable`; `V 1` introduces the one-byte value `*`;
  `END` terminates the hash. It declares a versioned permission property. It
  neither contains executable code nor performs a permission-changing call.

Both includes are guarded by `ISOLATION_AWARE_ENABLED` and can alternatively
use SDK static-library implementations. Their private identifiers use ROT13
and mixed case: for example, `zltRgCebPnQQeRff` becomes `mygEtProCaDDrEss`.
These are compile-time identifiers; there is no runtime string decoder,
encrypted payload, API hashing, or hidden command.

The common resolver is defined in the SDK's `winbase.inl`: the supplied module
configuration names `Comctl32.dll`; a cached module handle is populated through
the configured `LoadLibraryW` helper, followed by `GetProcAddress` using the
explicit, readable export name. Activation-context handling supports ordinary
side-by-side assembly selection. No remote process manipulation, persistence,
credential access, exfiltration, process launch, or destructive operation was
found in the supplied code.

## Upstream and dependency checks

Fetched Microsoft's [prsht.inl](https://raw.githubusercontent.com/microsoft/win32metadata/main/generation/WinSDK/RecompiledIdlHeaders/um/prsht.inl),
[dpa_dsa.inl](https://raw.githubusercontent.com/microsoft/win32metadata/main/generation/WinSDK/RecompiledIdlHeaders/um/dpa_dsa.inl),
and shared [winbase.inl](https://raw.githubusercontent.com/microsoft/win32metadata/main/generation/WinSDK/RecompiledIdlHeaders/um/winbase.inl).
After newline normalization, each supplied include differs from its upstream
counterpart only in the copyright end year (2023 versus 2026). The shared helper
was inspected to resolve the otherwise external calls. No URLs or downloadable
third-party dependencies occur in either supplied include. The named DLL is a
Windows platform component; no particular DLL binary accompanied these samples.

Apache Subversion's [hash implementation](https://raw.githubusercontent.com/apache/subversion/trunk/subversion/libsvn_subr/hash.c)
documents the K/V/END serialization, and its
[property definitions](https://raw.githubusercontent.com/apache/subversion/trunk/subversion/include/svn_props.h)
define the executable property and `*` boolean value. The entire small sample
parses as that property hash, with no trailing bytes.

These results support individual benign verdicts. An external source may have
propagated a malicious parent archive's label to SDK headers and VCS metadata,
or mistaken unusual names for obfuscation. The actual labeling reason is
unavailable; these explanations are hypotheses, not attribution findings.

## Trait corrections and scope audit

`cleave facts` and atomscan heuristically classify the `.inl` files as JavaScript;
`cleave test-rules` reports them as text. Their JavaScript flow facts include a
parse-error limitation and cannot establish source execution semantics. Source
review and upstream comparison therefore supply the behavioral interpretation.
No decoded payload strings or external references were reported by facts.

* Moved the unchanged identifier-assignment matcher from `metadata/lang/scripted`
  to `metadata/lang/source/syntax`, and renamed it to describe its language-neutral
  syntax. This expression also occurs in C and C++ and cannot identify JavaScript.
* Moved the unchanged `text.string_density <= 0.9`, minimum-4096-byte observation
  from `metadata/file/data-blob` to `metadata/file/profile/string-population`.
  The engine defines this metric as strings per code line, not byte density or
  an encoded blob. Its description now states the measured quantity.
* Preserved original file-type/platform scopes and criticalities for both moves.
  All other rules in the two source YAML files remain unchanged.
* Updated the string-blob consumer's exact reference. The three IoT parameter
  rules selecting `metadata/lang/scripted/` retain the moved assignment exclusion
  explicitly. The two syscall consumers of that directory target native ELF or
  Mach-O files; the moved JS/TS observation was never eligible for those inputs.
  No additional ancestor selector requires an update for either move.
  The existing `save-button-label.js` fixture expectation also follows the
  assignment trait's new ID in `testdata/expectations.toml`.
* Added notable SDK resolver-declaration and result-assigned export-lookup
  observations. The declaration belongs under source declarations rather than
  an upstream identity directory that would grant unrelated blanket exclusions.
  The lookup requires the actual SDK call with a result assignment because the
  incorrectly selected JS parser projects this site only as an identifier.
* Added a notable, line-framed Subversion executable-property declaration.
  Its name and description assert neither code execution nor a chmod operation.

No hostile or suspicious traits are justified. Final atomscan scans contain
two notable SDK observations for each include and one notable VCS property
observation for the property file, with zero suspicious and zero hostile traits.
Baseline source metrics may be omitted from rendered scan reports; the controls
trace their actual evaluation separately.

## Verification

`check.py` exercises 15 static fixtures: SDK declaration versus call versus
reference, LF/CRLF property records and malformed/mention-only controls,
assignment versus comparison, preservation of the IoT exclusion, and string
density/type-size boundaries. It copies inputs outside `testdata` before scans.

```sh
TRAIT_CONTROL_SCRATCH=/path/to/scratch python3 testdata/triage/windows-sdk-svn/check.py
```

All 15 controls passed. Each original sample was scanned with atomscan and inspected with `cleave facts`,
then rescanned with atomscan after the final YAML changes. The required final
repository check is `make validate`.
