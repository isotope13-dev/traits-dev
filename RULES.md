# cleave Rule Writing Guide

## Quick Overview

**Traits** = atomic observations (single pattern)
**Composites** = traits combined via boolean logic
**Criticality** = independent from confidence

**Tier hierarchy:**
- `micro-behaviors/*` - Observable capabilities (what code can do)
- `objectives/*` - Attacker objectives (intent signals)
- `well-known/*` - Specific malware/tool signatures (family-unique only)
- `metadata/*` - Informational file properties

See [TAXONOMY.md](./TAXONOMY.md) for complete tier structure.

**Tier dependencies:**
- `micro-behaviors/` → can reference `micro-behaviors/`, `metadata/`, and `well-known/{tool,app,lib,game}/` for false-positive exclusions only
- `objectives/` → can reference `micro-behaviors/`, `objectives/`, `metadata/`, and `well-known/{tool,app,lib,game}/` for false-positive exclusions only
- `well-known/` → can reference `micro-behaviors/`, `objectives/`, `well-known/`, and `metadata/`
- `metadata/` → typically references `metadata/`; may reference `well-known/{tool,app,lib,game}/` for benign context

**Critical rules:**
- `micro-behaviors/` must NOT reference `objectives/` (capabilities are atomic, objectives infer intent)
- `micro-behaviors/` must NOT use `crit: hostile` (hostile requires intent inference, belongs in `objectives/`)

## Tier Placement Litmus Test

Before placing a trait in `objectives/` or `well-known/`, ask: **would this fire on `/bin/ls`, `/bin/sh`, or `/usr/bin/curl`?** If yes, it's too broad for an intent-inferring tier.

**Common mistakes:**

| Pattern | Wrong Tier | Correct Tier | Why |
|---------|-----------|--------------|-----|
| Binary has many exports | `objectives/evasion/` | `metadata/binary/symbols/` | Neutral structural property |
| Binary has high entropy | `objectives/anti-static/` | `metadata/binary/metrics/` | Neutral measurement |
| Binary has low complexity | `objectives/anti-static/` | `metadata/binary/metrics/` | Normal for most binaries |
| ELF64 class marker | `objectives/anti-static/pack/` | `metadata/binary/metrics/` | Every 64-bit ELF has this |
| CLI help/usage text | `objectives/anti-static/` | `metadata/binary/metrics/` | Normal binary property |
| HTTP Content-Type header | `objectives/c2/` | `micro-behaviors/communications/http/` | Neutral protocol element |
| SOCKS protocol string | `objectives/c2/backdoor/` | `micro-behaviors/communications/proxy/` | Neutral protocol |
| `$HOME` env var | `objectives/discovery/` | `micro-behaviors/os/env/` | Universal env var |
| `execve` symbol | `well-known/tool/offensive/` | `micro-behaviors/process/create/` | Standard syscall |
| `umask` syscall | `objectives/persistence/` | `micro-behaviors/process/daemonize/` | Standard POSIX call |
| SELinux xattr | `objectives/evasion/anti-av/` | `micro-behaviors/fs/attributes/xattr/` | Normal on Linux |
| `readdir` export | `objectives/evasion/kernel-hide/` | Needs `unless:` for PIE executables | PIE ELFs are ET_DYN like .so |

**The rule:** A single API call, syscall, string literal, or structural measurement is **never** an objective. It becomes one only when combined with other signals in a composite rule. Place the atom in `micro-behaviors/` or `metadata/`, and let composites in `objectives/` reference it.

**Component traits in `objectives/`:** Only allowed when the fragment is attack-context-specific with no meaning outside that context (e.g., Nemucod-specific string pieces, C2 domain patterns). Generic protocol strings, syscalls, and binary metrics always belong in neutral tiers even when used as composite building blocks.

## Trait Placement & IDs

- IDs auto-prefixed by directory path (e.g., `traits/micro-behaviors/process/create/shell/` → prefix `micro-behaviors/process/create/shell`)
- **Filenames are NEVER part of trait IDs** - only the directory path is used for prefixing
  - A trait `foo` in `traits/micro-behaviors/process/create/shell/python.yaml` has ID `micro-behaviors/process/create/shell::foo`
  - NOT `micro-behaviors/process/create/shell/python::foo` or `micro-behaviors/process/create/shell/python/foo`
- Cross-tier references use full paths: `micro-behaviors/process/create/shell::subprocess`
- Directory match: `micro-behaviors/process/create/shell/` matches all traits in that directory
- Do not add junk subdirectory names like "operations/" or "commands/"; add subdirectories for the exact operation like "move" instead to provide maximum signal to our ML pipeline, which only sees directory names
- Generic capabilities NEVER go in `well-known/`

## Criticality Levels

| Level | Use When |
|-------|----------|
| `component` | Building blocks that make no sense individually (string fragments like `&cc=`) |
| `baseline` | Common functionality that nearly every program has (`mmap`, `stdio`, `read`) |
| `notable` | Defines program purpose and behavior (`socket`, `exec`, `eval`, `sysctl`) |
| `suspicious` | Hides intent/crosses boundaries (VM detection, obfuscation) |
| `hostile` | Attack patterns, no legitimate use (reverse shell, ransomware) |

Both `component` and `baseline` are allowed in any tier.

**Component traits** are filtered from terminal output unless a composite rule that references them fires. JSON output always includes all components for ML signal.

**HOSTILE composites require precision ≥ 3.5**, else downgraded. See [PRECISION.md](./PRECISION.md) for the calculation algorithm and authoring guidelines.

## Trait Definition

```yaml
# File-level defaults (apply to all traits/composites in file unless overridden)
defaults:
  for: [python]
  crit: notable
  conf: 0.85

traits:
  - id: execution/terminate          # ID relative to directory
    desc: Process termination API call   # 4-6 words, what was detected
    crit: suspicious                     # baseline|notable|suspicious|hostile
    conf: 0.95                           # 0.0-1.0
    mbc: "E1562"                         # Optional MBC code (B0001 behavior, C0015 micro, E1234 ATT&CK+MBC)
    attack: "T1562"                      # Optional ATT&CK code (T1234 or T1234.001)
    for: [csharp]                        # File types (see below)
    platforms: [linux, macos, windows]   # Optional platform filter
    arch: [x86-64]                       # Optional architecture filter (clamps search in fat binaries)
    size_min: 1000                       # Optional min file size (bytes)
    size_max: 10485760                   # Optional max file size
    entropy_min: 4.5                     # Optional min file entropy (0.0-8.0; section entropy handled via type: section)
    entropy_max: 7.5                     # Optional max file entropy
    if:                                  # Condition (see below)
      type: text
      substr: ".Kill("
```

**Field override:** List fields (`for`, `platforms`) can be set to `[none]` to unset file-level defaults. Example: `for: [none]` removes file type filtering even if defaults specify types. Scalar fields (`conf`, `crit`) do not support `none`.

**File types:** `elf`, `macho`, `pe`, `dll`, `so`, `dylib`, `pyc`, `shell`, `batch`, `python`, `javascript`, `typescript`, `rust`, `java`, `class`, `ruby`, `c`, `cpp`, `go`, `csharp`, `php`, `perl`, `powershell`, `lua`, `swift`, `objectivec`, `groovy`, `kotlin`, `scala`, `zig`, `elixir`, `vbs`, `html`, `applescript`, `package.json`, `chrome-manifest`, `vsix-manifest`, `cargo.toml`, `pyproject.toml`, `github-actions`, `composer.json`, `plist`, `ipa`, `rtf`, `lnk`, `jpeg`, `png`, `pkginfo`, `pickle`, `pdf`, `oledoc`, `ooxml`, `systemd-service`, `desktop-entry`.

**Aliases** (resolved to the canonical type):

| Alias | Resolves to | Format |
|-------|-------------|--------|
| `doc`, `xls`, `ppt`, `msg`, `ole` | `oledoc` | Legacy Microsoft Office (OLE2/CFBF) |
| `docx`, `xlsx`, `pptx`, `docm`, `xlsm`, `pptm` | `ooxml` | Modern Microsoft Office (OOXML/ZIP) |

**Platforms:** `linux`, `macos`, `windows`, `unix`, `android`, `ios`, `all`.

**Architectures:** `x86`, `x86-64`, `aarch64`, `arm`, `riscv`, `mips`, `powerpc`, `powerpc64`, `sparc`, `m68k`, `superh`, `all`. Omitting `arch` is equivalent to `arch: [all]`. Architecture is derived from the analyzed file, never the runtime host. For fat/universal Mach-O binaries, `arch` also clamps pattern searches (hex, raw, encoded) to the byte range of the matching slice, preventing cross-slice false positives.

**Named groups** (preferred over listing individual types):

| Group | Members |
|-------|---------|
| `binaries` | `elf`, `macho`, `pe`, `dylib`, `so`, `dll`, `class`, `pyc` |
| `scripts` | `shell`, `batch`, `python`, `javascript`, `ruby`, `php`, `perl`, `lua`, `powershell`, `applescript`, `vbs` |
| `source` | `typescript`, `rust`, `java`, `c`, `cpp`, `go`, `csharp`, `swift`, `objectivec`, `groovy`, `kotlin`, `scala`, `zig`, `elixir` |
| `manifests` | `package.json`, `chrome-manifest`, `vsix-manifest`, `cargo.toml`, `pyproject.toml`, `github-actions`, `composer.json`, `pkginfo`, `plist`, `lnk`, `systemd-service`, `desktop-entry` |
| `documents` | `pdf`, `rtf`, `html`, `oledoc`, `ooxml` |
| `media` | `jpeg`, `png` |
| `data` | `ipa` |

Use groups instead of listing 7 or more individual types. `for: [all]` is no longer valid — combine groups explicitly (e.g., `for: [binaries, scripts]`) or use specific types.

### Platform Auto-Filtering

When you use **group names** (`binaries`, `scripts`, etc.), cleave automatically filters the expanded types against the rule's `platforms:` field. This means you can write broad `for:` declarations without worrying about platform-incompatible types:

```yaml
defaults:
  platforms: [macos]
  for: [scripts, binaries]
  # Auto-filtered at load time to: [shell, python, javascript, ruby, php, perl,
  #   lua, applescript, macho, dylib, go, objc, class, pyc]
  # PE, DLL, ELF, SO, Batch, VBS, PowerShell are silently dropped (not macOS)
```

This eliminates the most common trait authoring mistake: forgetting to include `macho` when listing `[shell, python, javascript, powershell, pe, elf]`.

**When you use explicit type names** (not groups), platform conflicts remain a validation error:

```yaml
# ❌ ERROR: PE requires windows, but platforms is macos-only
defaults:
  platforms: [macos]
  for: [pe, macho]

# ✅ OK: Groups auto-filter, so this just works
defaults:
  platforms: [macos]
  for: [binaries]
```

**Best practice:** Use `for: [scripts, binaries]` for most traits. Only use explicit types when you genuinely need to restrict to a specific format (e.g., `for: [macho]` for Mach-O-specific structural analysis).

**Exclusions:** Prefix with `-` (e.g., `-php`, `scripts,-python`).
**Unset field:** Use `none` anywhere in the list to unset the field entirely, ignoring defaults.

## Condition Types

### Pattern Matching

| Type | Purpose | Matchers | Modifiers |
|------|---------|----------|-----------|
| `text` | Byte-scan extracted runs (binaries) or raw text (source) | `exact`, `substr`, `regex`, `word` | count, density, location, `case_insensitive`, `is` |
| `literal` | Parser-extracted constants — strings and numbers | `exact`, `substr`, `regex`, `word`, `value`, `radix` | `kind: string\|number`, count, density, location, `case_insensitive`, `is` |
| `raw` | Raw file bytes | `exact`, `substr`, `regex`, `word` | count, density, location, `case_insensitive`, `is` |
| `symbol` | Imports/exports/forwards/functions/calls | `exact`, `substr`, `regex` | `platforms`, `is`, `kind`, `arg` (call only) |
| `import` | Imported symbols / source import calls | `exact`, `substr`, `regex` | `platforms`, `is` |
| `export` | Exported symbols | `exact`, `substr`, `regex` | `platforms`, `is` |
| `function` | Internal functions / source call targets | `exact`, `substr`, `regex` | `platforms`, `is` |
| `hex` | Byte patterns (wildcards always extracted) | pattern string | count, density, `offset`, `offset_range`, `arch` clamped in fat binaries |
| `encoded` | **All decoded strings** | `exact`, `substr`, `regex`, `word` | count, density, location, `encoding`, `case_insensitive`, `is` |
| `value` | Residual structured values / manifest data | `exact`, `substr`, `regex` | `path`, `exists`, `size_min`, `size_max`, `case_insensitive` |
| `basename` | Filename | `exact`, `substr`, `regex` | `case_insensitive` |
| ~~`string_literal`~~ | *(renamed — use `literal`; old spelling kept as serde alias)* | | |
| ~~`ast`~~ | *(renamed — use `tree-sitter`; old spelling kept as serde alias)* | | |
| ~~`base64`~~, ~~`xor`~~ | *(removed — use `encoded`)* | | |
| ~~`string_value`~~ | *(removed — use `text`)* | | |
| ~~`string_count` / `string_value_count`~~ | *(removed — use `metrics: binary.string_count` or a `type: text` trait with `count_min`)* | | |
| ~~`exports_count`~~ | *(removed — use `metrics: binary.export_count`)* | | |
| ~~`import_combination`~~ | *(removed — use `type: import` plus composite `all`/`any`/`needs`)* | | |
| ~~`structure`~~ | *(removed — express file-format and arch gates via trait-level `for:`/`arch:`, or check `elf.e_machine`/`macho.cpu_type`/`pe.machine` via `metrics`)* | | |

**Matcher notes:**
- `word` - Word boundary match (equivalent to `\b{value}\b`). Available on `text`, `literal`, `raw`, `section`, `encoded`. NOT available on `symbol`, `basename`, `hex`.
- `is` - High-fidelity validator for common data patterns. Supported values:
  - `external_ip`: Only match if evidence contains a valid external IPv4 (rejects RFC1918, loopback, reserved).
  - `bitcoin_addr`: Only match if evidence contains a valid Bitcoin address (P2PKH, P2SH, or SegWit) with a valid checksum.
- **Symbol normalization:** Leading underscores are stripped from both loaded symbols and `exact`/`substr` patterns for cross-platform portability (macOS `_malloc`, glibc `__libc_start_main` both match `exact: "malloc"` / `exact: "libc_start_main"`). Regex patterns are not normalized.
- **Symbol family shortcuts:** use `type: import`, `type: export`, or `type: function` when you know the family. They are clearer spellings for `type: symbol` with `kind: import/export/function`. Keep `type: symbol` for cross-family searches or `kind: forward` PE re-export rules. When `kind: forward`, the pattern is tested against both the export name *and* the forward target (`KERNEL32.LoadLibraryA`).

**Which one should I use?**

Speed and accuracy run together. From best to worst:

1. **`symbol` / `import` / `export` / `function` / `literal`** — index lookups
   against precomputed facts. No re-parse, no scan. Sharpest signal: the
   walker already split code from comments and string contents, so these
   never fire on a stray mention in a comment or unrelated string.
2. **`text`** — substring/regex over extracted strings. Fast enough; less
   precise than symbol/literal because the corpus includes everything the
   string extractor recovered.
3. **`raw`** — substring/regex over the full file bytes. Catches what the
   string extractor missed (comments, byte sequences across boundaries),
   pays for it in false positives and wall-clock.
4. **`tree-sitter`** — live query against the parse tree. Slowest by a wide
   margin (one walk per rule). Reach for it only when behavior depends on
   tree shape the symbol projections can't express.

Pick the highest tier that answers your question:

- `symbol` for "is this called / imported / exported anywhere?" — and with
  `kind: call, arg: ...` for "this specific call site with this specific
  arg" (see the call-matching section below).
- `literal` for language-level constants — quoted strings or numeric
  literals recovered from the parse. `kind: number` is the only way to
  match numbers by value and radix.
- `text` for human-readable content that isn't tagged by the parser as
  string or symbol — error messages, log strings, embedded config.
- `raw` for comments, byte-precise offsets, or matches that cross string
  boundaries.
- `tree-sitter` only when nothing above works.

Before reaching for `tree-sitter`, check `cleave facts <file>` —
the call, member, bind, or literal you need is usually already a
structured fact.


### Structural

| Type | Purpose | Fields |
|------|---------|--------|
| `tree-sitter` | Live tree-sitter query (escape hatch) | `kind`/`node`, `exact`/`substr`/`regex`/`query` (S-expression). `ast` is a serde alias. |
| `syscall` | Direct syscalls | `name`, `number`, `arch` (all optional, OR within field, AND across fields) |
| `section` | Binary sections | `exact`, `substr`, `regex`, `word`, `case_insensitive`, `length_min`, `length_max`, `entropy_min`, `entropy_max`, `readable`, `writable`, `executable`, `compare_to` (reference section for both ratio checks; default: "total" for size), `size_ratio_min`, `size_ratio_max`, `entropy_ratio_min`, `entropy_ratio_max` |
| `metrics` | Code metrics | `field` (e.g., `identifiers.avg_entropy`, `binary.text_to_file_ratio`, `binary.string_count`, `elf.e_machine`, `pe.dos_stub_zeroed`, `consistency.cert_org_pdb_mismatch`), `min`, `max`, `min_size`, `max_size` |
| `yara` | YARA rule | `source` |

> **Note**: File size filtering uses trait-level `size_min`/`size_max` fields, not a condition type.

### Syscall Matching

The `syscall` type filters are all optional. Within each field (name, number, arch), matching is OR (any value matches). Across fields, matching is AND (all specified fields must match).

```yaml
# Match by name (any of these)
- id: network-syscalls
  if:
    type: syscall
    name: ["socket", "connect", "bind"]

# Match by number on specific arch
- id: execve-x64
  if:
    type: syscall
    number: [59]
    arch: ["x86_64"]
```

### Structural Condition Examples

File-format and architecture gates are expressed at the trait level with `for:`
and `arch:` rather than a condition type. To identify a specific architecture or
format, use a `metrics` check against the numeric header field:

```yaml
# Fire only on x86-64 ELF binaries
- id: arm64-elf
  for: [elf]
  arch: [aarch64]
  if:
    type: metrics
    field: elf.e_machine
    min: 183
    max: 183

# Detect binaries with suspiciously few exports
- id: minimal-exports
  if:
    type: metrics
    field: binary.export_count
    max: 5

# Detect string obfuscation (very few visible strings).
# stng already applies min_length=4 during extraction, so binary.string_count
# reflects strings of length >= 4 — no separate filter needed.
- id: few-strings
  if:
    type: metrics
    field: binary.string_count
    max: 20

# Detect obfuscated identifiers via entropy
- id: high-entropy-identifiers
  if:
    type: metrics
    field: "identifiers.avg_entropy"
    min: 4.5
    min_size: 10000  # Only check files >10KB

# PE: DOS stub erased (bytes 0x40..e_lfanew all zeroed)
# Standard "This program cannot be run in DOS mode" message removed
- id: dos-stub-zeroed
  for: [pe, dll]
  if:
    type: metrics
    field: pe.dos_stub_zeroed
    min: 1

# PE: security directory file offset exceeds file length (header tampering)
- id: security-dir-out-of-bounds
  for: [pe, dll]
  if:
    type: metrics
    field: pe.security_directory_out_of_bounds
    min: 1

# Consistency: no word from cert signer org appears in PDB path (supply-chain swap)
- id: cert-org-pdb-mismatch
  for: [pe, dll]
  if:
    type: metrics
    field: consistency.cert_org_pdb_mismatch
    min: 1
```

**Available `pe.*` metric fields (boolean, 0/1):**
- `pe.dos_stub_zeroed` — every byte in the DOS stub region (0x40..e_lfanew) is 0x00; standard "This program cannot be run in DOS mode" message erased
- `pe.security_directory_out_of_bounds` — security directory file offset exceeds actual file length; indicates header tampering

**Available `consistency.*` metric fields (boolean, 0/1):**
- `consistency.cert_org_pdb_mismatch` — no word from the cert signer organization appears in the PDB path; supply-chain swap signal
- `consistency.bundle_identifier_mismatch` — bundle identifier in Info.plist differs from signing identity
- `consistency.manifest_product_version_mismatch` — product version in PE manifest differs from version info resource
- `consistency.cert_issued_after_build` — authenticode cert `not_before` timestamp is later than the PE link timestamp

### Hex Pattern Syntax

| Token | Description | Example |
|-------|-------------|---------|
| `XX` | Literal byte (hex) | `7F 45 4C 46` |
| `??` | Any single byte (wildcard) | `31 ?? 48` |
| `X?` | High nibble fixed, low nibble wild | `4?` matches 0x40-0x4F |
| `?X` | Low nibble fixed, high nibble wild | `?A` matches any byte ending in A |
| `[N]` | Skip exactly N bytes | `00 [4] FF` |
| `[N-M]` | Skip N to M bytes | `00 [2-8] FF` |
| `(XX\|YY)` | Byte alternation (match any) | `(00\|80)` matches 0x00 or 0x80 |

**Examples:**

```yaml
# ELF magic
if:
  type: hex
  pattern: "7F 45 4C 46"

# XOR loop detection (nibble wildcards for register variants)
if:
  type: hex
  pattern: "31 ?? 88 ?? 4? 83 ?? ?? 7?"

# LZMA header with size byte options
if:
  type: hex
  pattern: "5D 00 00 (00|80) 00 (01|02|03|04) [7] ??"
```

### Tree-sitter Kinds

Used with `type: tree-sitter` (the escape hatch). Available kinds:
`call`, `function`, `class`, `import`, `string`, `comment`, `assignment`,
`return`, `binary_op`, `identifier`, `attribute`, `subscript`, `member`,
`conditional`, `loop`.

Each abstract kind maps to one or more tree-sitter node types per language
(see `composite_rules/ast_kinds.rs`). The matcher walks the parse tree and
for every node of a matching type compares your pattern against the node's
text.

**The node text rule:** for most kinds, the text is what you'd expect — a
`string` node is the string literal, a `comment` node is the comment body.
The exception is `call`:

- `kind: call` matches `function_call_expression` (PHP), `call_expression`
  (JS/TS/Go/Rust/C/…), `call` (Python/Elixir), `method_invocation` (Java).
- The node text is the **full call expression** including arguments and
  parens: `curl_exec($ch)`, `aes.NewCipher(key)`, `eval("x")`.
- For `exact:`, cleave checks two surfaces: the full text (`name(args)`)
  and the extracted name (`name`) as a fallback — so `exact: curl_exec`
  matches `curl_exec($ch)`.

**`member` matches dotted access including normalized subscripts.** Tree-sitter
emits `obj.foo` and `obj["foo"]` as different node types. The walker folds
string-subscript access into the member chain, so `obj["constructor"]`
matches `kind: member, substr: obj.constructor` — the JS sandbox-escape
pattern is a normal member-chain rule, not a tree-sitter query.

For straightforward call matching, `type: symbol, kind: call` is faster and
clearer than `type: tree-sitter, kind: call`. Use tree-sitter only when the
behavior depends on tree shape the symbol projections can't express.

### Matching calls — recipe table

Each call site is a structured fact: target name plus per-argument shape and
value. Reach for `type: symbol, kind: call` first. Drop to `tree-sitter` only
when the projection genuinely doesn't carry what you need.

| Goal | Best form | Notes |
|------|-----------|-------|
| Match a function called anywhere by exact name | `type: symbol exact: <name>` | Fastest. Walks the symbol table — imports, exports, functions, calls. |
| Match a specific call site (`chmod(_, 0o777)`) by name + arg value | `type: symbol kind: call substr: <name> arg: { kind: number, value: 511, radix: 8 }` | Args carry shape + literal value. Joins on the same call site, not file-wide coincidence. |
| Match a call with a literal string argument | `type: symbol kind: call substr: <name> arg: { kind: string, substr: <part> }` | The arg filter narrows to calls whose argument list contains a matching arg. |
| Match a call whose arg is a specific identifier (e.g. `setTimeout(callback, ...)`) | `type: symbol kind: call substr: <name> arg: { kind: identifier, name: <ident> }` | Identifier-shaped args carry the bare name. |
| Detect any call from a known dangerous family | `type: symbol regex: '^(eval\|exec\|system\|assert)$'` | Symbol regex with anchors stays tight. |
| Match a structural shape the projection can't express (loop containing call inside try) | `type: tree-sitter kind: call query: "(call_expression ...)"` | Full S-expression query — [tree-sitter docs](https://tree-sitter.github.io/tree-sitter/using-parsers#pattern-matching-with-queries). |

**`arg:` filter shape** (used inside `type: symbol, kind: call`):

```yaml
arg:
  kind: number       # string | number | identifier | bool | template | <shape>
  value: 511         # numeric value (kind=number)
  radix: 8           # source-written radix: 2/8/10/16. With value, both must match.
  substr: "evil"     # substring on string/template values
  exact: "..."       # exact value match
  name: "BACKDOOR_PORT"  # identifier name (kind=identifier)
```

The filter matches if **at least one** arg in the call's arg list satisfies all
specified fields. `kind: number, value: 511, radix: 8` matches `chmod(_,
0o777)` but not `chmod(_, 511)` — the source-written radix discriminates
deliberate octal mode bits from incidentally-computed integers.

**Picking between `type: symbol` and `type: tree-sitter`:**

- `type: symbol` covers nearly every call-matching need. It runs against the
  precomputed symbol view — no live parse, no per-rule tree walk.
- `type: tree-sitter` is the escape hatch. Use it for patterns that depend on
  the surrounding tree shape: call inside a try/catch, assignment whose RHS is
  a call whose argument is itself a call, etc.

### Other AST kinds — what node text actually is

| Kind | Node text is… | Useful matcher forms |
|------|---------------|---------------------|
| `call` | full call expression `name(args)` (plus the extracted name as a fallback for `exact:`) | `exact:` (name), `substr: "name("`, `regex:`, `query:` |
| `function` / `class` | the whole definition body — usually thousands of bytes | `query:` or `substr:` on a definition keyword; `exact:` on the whole body is never useful |
| `string` | the string literal **including quotes** (so `exact: hello` won't match `"hello"`; use `substr: hello` or `exact: '"hello"'`) | `substr:`, `regex:` |
| `comment` | the comment body including comment delimiters | `substr:`, `regex:` |
| `import` | the import/use/require statement text | `substr:`, `regex:` |
| `assignment` | the full assignment `lhs = rhs` | `substr:`, `regex:` |
| `identifier` | a single identifier token | `exact:`, `substr:`, `regex:` |
| `attribute` / `subscript` | the attribute access or subscript expression | `substr:`, `regex:` |
| `return` / `binary_op` / `conditional` / `loop` | the full statement/expression text | `substr:`, `regex:`, `query:` |

If you're ever in doubt about what a node's text is, run `cleave test-match <file> --type ast --kind <kind> --pattern <something-permissive>` and inspect the captured evidence.

## Count & Density Constraints

These are **trait-level fields** (siblings of `if:`, not nested inside the condition):

| Field | Description |
|-------|-------------|
| `count_min` | Minimum matches required (default: 1) |
| `count_max` | Maximum matches allowed |
| `per_kb_min` | Minimum matches per KB |
| `per_kb_max` | Maximum matches per KB |

```yaml
- id: dense-chr-calls
  count_min: 10
  per_kb_min: 2.0
  if:
    type: raw
    regex: "chr\\s*\\("
```

## Location Constraints

Available on `text`, `literal`, `raw`, `encoded`. Hex supports `offset` and `offset_range`.

| Field | Description |
|-------|-------------|
| `section` | Restrict to named section (fuzzy: `text` → `.text`, `__text`) |
| `offset` | Exact file offset (negative = from end) |
| `offset_range` | `[start, end)` range (`null` = open-ended) |
| `section_offset` | Offset within section (requires `section`) |
| `section_offset_range` | Range within section (requires `section`) |

```yaml
# Last 1KB of file
- id: trailer-check
  if:
    type: text
    substr: "END"
    offset_range: [-1024, null]

# First 64 bytes (magic/header)
- id: magic-check
  if:
    type: hex
    pattern: "7F 45 4C 46"
    offset: 0

# Within .rodata section, first 256 bytes
- id: rodata-header
  if:
    type: text
    substr: "CONFIG"
    section: rodata
    section_offset_range: [0, 256]
```

## Section Constraints

### Size Constraints

The `section` condition type supports absolute size constraints to detect structural anomalies:

```yaml
# Detect abnormally small __cstring section (string obfuscation)
- id: tiny-cstring-absolute
  desc: Abnormally small __cstring section
  crit: suspicious
  conf: 0.85
  for: [macho]
  size_min: 100000  # Only check binaries >100KB
  if:
    type: section
    exact: "__TEXT.____cstring"
    length_max: 100  # Section must be ≤100 bytes

# Detect large __data section (encoded payload storage)
- id: large-data-payload
  desc: Large __DATA section (8KB+)
  crit: notable
  conf: 0.75
  for: [macho]
  if:
    type: section
    exact: "__DATA.____data"
    length_min: 8192  # Section must be ≥8KB

# Detect section in specific size range
- id: suspicious-section-size
  desc: Section with suspicious size
  crit: suspicious
  conf: 0.8
  if:
    type: section
    substr: ".data"
    length_min: 8192
    length_max: 16384  # Between 8KB and 16KB
```

**Size constraints:**
- `length_min` - Minimum section length in bytes
- `length_max` - Maximum section length in bytes
- Can be used alone or combined with name patterns
- Evidence includes section size in output

### Permission Constraints

Filter sections by permission flags (PE/ELF/Mach-O):

| Field | Match Behavior |
|-------|----------------|
| `readable: true` | Section contains 'r' in permissions string |
| `writable: true` | Section contains 'w' in permissions string |
| `executable: true` | Section contains 'x' in permissions string |

Adds +0.5 precision per constraint. Combinable with entropy/size/name filters.

```yaml
# Packing detection
type: section
executable: true
entropy_min: 7.0

# W^X violation
type: section
writable: true
executable: true

# Obfuscated writable data
type: section
regex: "^(\\.data|__data)"
writable: true
entropy_min: 6.5
```

### Ratio Constraints

Compare a section's size or entropy against another section (or the total file) using ratio fields. `compare_to` names the reference: `"total"` uses total file size as the denominator (default for size ratios), or any section name substring (e.g. `"text"` matches `.text` / `__TEXT.__text`).

```yaml
# Section size ratio: .rsrc must be ≥ 30% of total file size
- id: large-resource-section
  desc: Resource section unusually large relative to file
  type: section
  substr: rsrc
  compare_to: total
  size_ratio_min: 0.3

# Entropy ratio: .rsrc entropy must be ≥ 1.5× .text entropy
- id: high-entropy-resource-vs-code
  desc: Resource section much higher entropy than code
  type: section
  substr: rsrc
  compare_to: text
  entropy_ratio_min: 1.5
```

**Ratio fields:**
- `compare_to` — reference section name substring, or `"total"` for total file size (default for size ratios)
- `size_ratio_min` / `size_ratio_max` — section size as a fraction of the reference size
- `entropy_ratio_min` / `entropy_ratio_max` — section entropy divided by reference section entropy

## Encoded Strings

The `encoded` type searches decoded/encoded strings with optional encoding filter. It unifies and replaces the deprecated `base64` and `xor` types with additional features:

- **Word boundary matching**: `word` parameter (not available in `base64`/`xor`)
- **Flexible encoding filter**: Single, multiple (OR), or omit (all)
- **Supports all encoding types**: base64, base64-obf, hex, xor, url, unicode-escape, base32, base85, utf16le, utf16be, stack, wide

### Encoding Filter

| Syntax | Behavior | Example |
|--------|----------|---------|
| Omit `encoding:` | Search **all** encoded strings | `type: encoded, substr: "eval"` |
| Single string | Search single encoding type | `encoding: base64` |
| Array | Search multiple types (OR) | `encoding: [base64, hex]` |

### Examples

```yaml
# Search ALL encoded strings for "password"
- id: encoded-password
  if:
    type: encoded
    word: password    # Word boundary match (NEW!)

# Search only base64 strings
- id: base64-url
  if:
    type: encoded
    encoding: base64
    regex: "https?://"

# Search base64 OR hex for suspicious patterns
- id: multi-encoding-check
  if:
    type: encoded
    encoding: [base64, hex]
    substr: "cmd.exe"
    count_min: 2

# Case-insensitive search in XOR-decoded strings
- id: xor-malware
  if:
    type: encoded
    encoding: xor
    substr: MALWARE
    case_insensitive: true

# Density check across all encoded strings
- id: dense-encoded
  if:
    type: encoded
    substr: eval
    count_min: 5
    per_kb_min: 3.0
```

### Migration from base64/xor

The `type: base64` and `type: xor` condition types have been removed and will produce parse errors. Replace them with `type: encoded`:

```yaml
# OLD (removed — will error)
type: base64
substr: "secret"

# NEW (required)
type: encoded
encoding: base64
substr: "secret"

# OLD (removed — will error)
type: xor
regex: "malware"

# NEW (required)
type: encoded
encoding: xor
regex: "malware"
```

**Advantage**: Use `encoded` without `encoding:` to search *all* decoded strings regardless of encoding type.

## Composite Rules

```yaml
composite_rules:
  - id: reverse-shell
    desc: Reverse shell pattern
    crit: hostile
    conf: 0.95
    for: [elf, macho]
    all:                              # AND (all must match)
      - id: micro-behaviors/communications/socket/create
      - id: micro-behaviors/process/fd/dup2
      - id: micro-behaviors/process/create/shell
    any:                              # OR (at least one)
      - id: pattern-a
      - id: pattern-b
      - id: legitimate-use
    needs: 2                          # Min matches from `any:` ONLY (has no effect on `all:`)
    scope: leaf                       # Optional: tighten cross-source FPs (see Scope)
    near_bytes: 256                   # Optional: tighten by byte proximity
```

**Trait references:** Use `{ id: trait-id }` in condition lists. The `type:` field can be omitted for trait references.

**Absence detection:** A composite rule with only `none:` (no `all:` or `any:`) fires when none of the listed conditions match. This is useful for detecting the absence of expected traits:

```yaml
composite_rules:
  - id: unsigned-binary
    desc: Binary lacks any code signature
    crit: notable
    conf: 0.8
      - id: file/signed/apple
      - id: file/signed/microsoft
```

**Circular references:** Composites can reference other composites. Circular references are handled safely — composite evaluation uses a fixed-point loop (max 10 iterations). Circular references will not crash but the circularly-dependent traits may not resolve.

## Trait References in `if:`

Atomic traits can reference other traits via `if: id:`. This creates a **derived trait** that fires when the referenced trait matches. This is a hybrid between atomic traits and composites.

```yaml
traits:
  # Derived trait: adds section constraint to existing pattern
  - id: base64-in-rodata
    desc: Base64 data in rodata section
    crit: notable                    # Can change criticality
    if:
      id: objectives/anti-static/obfuscation/encoding/base64::dense-base64-encoding
      section: rodata                # Add section constraint
      count_min: 10                  # Add count constraint
```

### When to Use Trait References

**Good uses** (add value beyond the referenced trait):

| Addition | Example |
|----------|---------|
| Section constraint | `section: rodata` - limit to specific section |
| Count constraint | `count_min: 5` - require multiple occurrences |
| Density constraint | `per_kb_min: 2.0` - require density |
| Criticality change | `crit: suspicious` when base is `notable` |
| Downgrade rules | Add `downgrade:` for context-aware severity |
| Unless conditions | Add `unless:` to skip in certain contexts |

**Bad uses** (pure aliases - will produce validation warnings):

```yaml
# ❌ BAD: Pure alias, no added value
- id: stratum-tcp
  desc: Stratum mining protocol
  crit: notable                      # Same as referenced trait
  if:
    id: objectives/impact/cryptojacking/miner/protocol::stratum-tcp
    # No section, count, downgrade, unless, etc.
```

If you need a short name for use in composite rules, reference the original trait directly instead:

```yaml
# ✅ GOOD: Reference directly in composite
composite_rules:
  - id: miner-indicators
    any:
      - id: objectives/impact/cryptojacking/miner/protocol::stratum-tcp
      - id: objectives/impact/cryptojacking/miner/protocol::stratum-ssl
```

## Exception Directives

| Directive | Purpose |
|-----------|---------|
| `not:` | Filter matched strings (list of `exact`/`substr`/`regex`) |
| `unless:` | Skip if condition matches (trait refs or inline conditions) |
| `downgrade:` | Reduce criticality by one level if condition matches |

**Proximity (composites only):** `near_bytes: N`, `near_lines: N` - require evidence from different conditions to fall within a single span of N bytes/lines. Uses a sliding window: the check passes when any contiguous window of size N contains evidence from enough distinct conditions (all conditions for `all:`, `needs` conditions for `any:`).

**Scope (composites only):** `scope: outer | archive | file | leaf` — require all evidence to share an analysis-tree ancestor at the named level. Default `outer` is today's behavior (anywhere in the input). Use a stricter scope to suppress archive/multi-file false positives where two conditions happen to match in unrelated entries of the same archive. Scope filtering runs *before* `near_bytes`/`near_lines`, so the two compose: scope picks the source bucket, proximity narrows within it.

| Value | Constraint | Use case |
|-------|------------|----------|
| `outer` | anywhere in the on-disk input (default) | today's behavior |
| `archive` | same nearest enclosing archive entry; degrades to `outer` if no archive | rules that should fire only when conditions land in entries of the same archive |
| `file` | same leaf-file (deepest file-shaped unit) | rules that must see all conditions in one file even if it sits inside an archive; pools the file with its decoded payload layers |
| `leaf` | same exact analyzed unit, including decoded payload layers | strictest — both conditions must land in the same decoded layer (or the same file with no decoding) |

Concrete tree examples (`!` separates archive entries; `::` denotes decoded layers):

| Tree path | `leaf` key | `file` key | `archive` key | `outer` |
|---|---|---|---|---|
| `script.py` | input | input | input | input |
| `loader.exe::overlay::final.py` | the decoded layer | input | input (no archive) | input |
| `archive.zip!stage.exe` | `archive:stage.exe` | `archive:stage.exe` | `archive:` (single-level) | input |
| `outer.zip!inner.zip!stage.exe` | the entry | the entry | `archive:outer.zip!inner.zip` (nearest archive) | input |

```yaml
composite_rules:
  - id: anchor-dll-shellcode-injector
    crit: hostile
    all:
      - id: anchor-dll-targeting
      - id: injection-trinity-text
    scope: leaf       # both conditions must land in the same analyzed unit;
                      # suppresses archive cross-entry FPs
    near_bytes: 64    # ...AND additionally within 64 bytes of each other
```

### Downgrade Behavior

Reduces criticality by **one level** when conditions match:

| Original → Downgraded | Use Case |
|----------------------|----------|
| `hostile` → `suspicious` | Known malware signature found in security tool |
| `suspicious` → `notable` | Anti-debug technique in signed system binary |
| `notable` → `baseline` | Common capability in trusted context (becomes invisible) |

**Syntax** (works on both atomic traits and composite rules):

`downgrade:` supports full boolean logic with `all:`, `any:`, `none:`, and `needs:` - the same structure as composite rule conditions.

```yaml
traits:
  - id: debugger-check
    desc: Anti-debugging technique
    crit: suspicious                    # Suspicious by default
    conf: 0.85
    if:
      type: symbol
      exact: "ptrace"
    downgrade:                           # → notable if signed
      any:
        - id: metadata/signed/platform::apple
        - id: metadata/quality::versioned

composite_rules:
  - id: process-hollowing
    desc: Process injection technique
    crit: hostile                        # Hostile by default
    conf: 0.95
    all:
      - id: micro-behaviors/process/create
      - id: micro-behaviors/mem/alloc/rwx
    downgrade:                           # → suspicious if debugger
      all:                               # Full boolean logic supported
        - id: micro-behaviors/process/create/load/library::debugger-tool-marker
        - id: objectives/anti-analysis/packing::upx
```

**Note:** Downgrade to `baseline` removes the finding from terminal output, but it is still included in JSON output. Use `unless:` if you want to skip matching entirely.

**Debug:** Use `test-rules` to see downgrade evaluation:
```bash
cleave test-rules file.bin --rules "debugger-check"
# Shows: "Downgrade: suspicious -> notable (triggered)"
```

## KV Path Syntax

For JSON/YAML/TOML manifests (`package.json`, `manifest.json`, `Cargo.toml`, etc.):

```yaml
path: "key"                    # Top-level key
path: "a.b.c"                  # Nested access
path: "arr[0]"                 # Array index
path: "arr[*]"                 # Any array element
path: "scripts.postinstall"    # npm scripts
path: "permissions"            # Chrome extension
```

### INI-style formats (systemd, Desktop Entry)

`.service` unit files and `.desktop` entries are parsed with sections as the
top-level object. Section headers and keys are normalized to snake_case
(`[Desktop Entry]` → `desktop_entry`, `X-GNOME-Autostart-enabled` →
`x_gnome_autostart_enabled`). Known `;`-separated list keys (e.g. `Categories`,
`MimeType`, `Keywords`, `Actions`) are split into arrays; the original
unparsed value is also kept under `<section>._raw.<key>`.

```yaml
# systemd: ExecStart from /tmp
type: value
path: service.exec_start
regex: "^/tmp/"

# .desktop: Exec= invokes shell
type: value
path: desktop_entry.exec
regex: '\bbash\s+-c\b'

# .desktop: GNOME autostart enabled
type: value
path: desktop_entry.x_gnome_autostart_enabled
exact: "true"

# .desktop: Categories contains a specific tag
type: value
path: desktop_entry.categories
exact: Utility

# .desktop: secondary [Desktop Action <name>] section
type: value
path: desktop_action_new_window.exec
exists: true
```

Localized keys (`Name[cs]=...`) are dropped during parsing; only the base
key (`name`) is exposed. Use `cleave value <file>` to dump the full path map
for any structured file while authoring traits.

### Binary formats (ELF, PE, Mach-O)

`type: value` works on binaries too. Cleave synthesizes a values tree of *raw
structural reads* — strings, names, identities, hex digests, raw bit-flag
values lifted directly from binary headers, sections, and load commands.
This is the cleanest surface for build-environment / supply-chain
attribution because the data sources are stable per build pipeline.

```yaml
# PE: PDB-style attribution paths leaked from C2 frameworks
type: value
path: pe.debug.pdb.path
regex: "(^|[/\\\\])Apollo\\.pdb$"

# PE: trojanized installer using cross-vendor masquerade
type: value
path: pe.version.product_name
regex: "HWiNFO|HWMonitor"

# Mach-O: code signature identifies the developer team
type: value
path: macho.code_signature.team_id
exact: "9XQGPJ8B7K"

# ELF: vendor binary requires a specific glibc version
type: value
path: elf.needed_versions
regex: "GLIBC_2\\.38"

# PE: side-by-side manifest declares Win10+ support
type: value
path: pe.manifest.supported_os
regex: '"name":"win10"'

# ELF: built on a specific distro
type: value
path: build.distro
exact: wolfi

# Mach-O: Swift code presence (any __swift5_* section)
type: section
substr: "__swift5_"

# Cross-format: builder home directory leaked
type: value
path: build.user_home
regex: "^/home/[a-z0-9_-]{1,40}$"
```

Top-level value namespaces synthesized from binaries:

| Namespace | Contents | Examples |
|---|---|---|
| `build.*` | Cross-format toolchain attribution | `target_arch`, `toolchain`, `toolchain_family`, `distro`, `linker`, `username`, `user_home`, `build_root`, `source_paths[]`, `sanitizers[]`, `fortified[]`, `command_line`, `rust_runtime_symbols[]`, `rust_mangling`, `has_rustc_section` |
| `signing.*` | Cross-format code-signing identity | `is_signed`, `subject`, `issuer`, `thumbprint_sha1`, `serial`, `not_before`, `not_after`, `signing_time`, `team_id`, `bundle_identifier`, `authorities[]`, `entitlements.*`, `catalog`, `type`, `cdhash_sha256`, `requirements_sha256`, `notarized`, `hardened_runtime` |
| `debug.*` | Cross-format debug info | `pdb_path`, `build_id`, `has_build_id`, `has_debuglink`, `producer`, `comp_dir` |
| `pe.*` | PE-specific | `rich_header.*`, `version_info.*`, `manifest.*` (assembly_identity, requested_execution_level, supported_os, dependencies), `dll_characteristics.*` (named flag bools), `debug_directory_types[]`, `is_reproducible_build`, `has_pogo`, `has_iltcg`, `codeview_guid`, `linker_version`, `timestamp`, `checksum`, `bound_imports[]`, `resource_types[]`, `load_config.*` |
| `elf.*` | ELF-specific | `entry_section`, `relro`, `interpreter`, `comment`, `soname`, `needed[]`, `rpath[]`, `runpath[]`, `dt_flags.*` (named flag bools), `gnu_property.{ibt,shstk,pac,bti,x86_isa_level}`, `needed_versions[]` (per-lib symbol versions), `provided_versions[]` |
| `macho.*` | Mach-O-specific | `uuid`, `platform`, `min_os_version`, `sdk_version`, `tools[]`, `load_dylibs[]`, `rpath[]`, `install_name`, `linker_options[]`, `source_version`, `info_plist.*`, `launchd_plist.*`, `slices[]`, `swift_sections[]`, `cs_flags.*`, `header_flags.*` |
| `signing.*` | Signing metadata | `catalog`, `format`, `time`, `team_id`, `bundle_identifier`, `authorities[]`, `cert.{subject, issuer, serial, thumbprint_sha1}`, `validity.{not_before, not_after}` |
| `dwarf.*` | DWARF debug info (unstripped ELF) | `producers[]`, `comp_dirs[]`, `languages[]`, `source_files[]` |
| `package.*` | FDO `.note.package` self-attestation | `type` (apk/rpm/deb), `name`, `version`, `architecture`, `os`, `cpe`, `url`, `vcs` |
| `go.*` | Go buildinfo | `version`, `main_path`, `main_module.*`, `dependencies[]`, `build.*`, `vcs.{system, revision, time, modified}` |
| `hash.*` | Cluster / similarity hashes (terse stems) | `imp`, `sym`, `dylib`, `export`, `entitlement`, `gimp`, `tlsh`, `ssdeep`, `cd`, `authenti`, `rich_header` |

For derived booleans, counts, deltas, and comparisons (e.g.
`signing.is_signed`, `pe.cert_chain_depth`, `consistency.*`), prefer
`type: metrics` since those are typed integers/booleans on the metrics
structs. Use `type: value` for raw structural reads — strings, hex digests,
named identities, list contents.

Run `cleave value <binary>` on a sample to see every value path it produces;
the same paths are matchable from YAML traits.

### Value Matching

Path-only (no matcher) = existence check.

```yaml
# Existence check (field must exist)
type: value
path: "description"

# Explicit existence check
type: value
path: "description"
exists: true              # Field must exist

# Non-existence check
type: value
path: "description"
exists: false             # Field must NOT exist

# String matching
type: value
path: "scripts.postinstall"
substr: "curl"            # Contains substring

# Exact match
type: value
path: "license"
exact: "MIT"              # Exact string match

# Regex match
type: value
path: "version"
regex: "^0\\.0\\.0$"      # Version is 0.0.0
```

### Collection Size Constraints

Constrain collection size (array elements or object keys):

```yaml
# Exactly one maintainer
type: value
path: "maintainers"
size_min: 1
size_max: 1

# At least 3 dependencies
type: value
path: "bundledDependencies"
size_min: 3

# No more than 10 keywords
type: value
path: "keywords"
size_max: 10

# Empty array/object
type: value
path: "contributors"
size_max: 0
```

**For objects:**

```yaml
# At least 5 dependencies
type: value
path: "dependencies"
size_min: 5

# No dependencies
type: value
path: "dependencies"
size_max: 0
```

**Constraint Validation:**
- `size_min`/`size_max` apply to arrays (element count) and objects (key count)
- Scalars (strings, numbers, booleans) will fail size constraints
- Evidence output includes `size: N (array)` or `size: N (object)`

## Validation & Auto-Fix

### Regex Constraints

Regex patterns are validated at load time:
- Maximum 80 bytes for regex patterns
- Maximum 3 `|` alternation symbols outside character classes
- Simple alphanumeric alternation (like `foo|bar|baz`) triggers a warning to use separate atomic traits

### Auto-Fix Behaviors

- **Literal regex conversion:** Patterns without regex metacharacters (`.`, `*`, `+`, `?`, `^`, `$`, `(`, `)`, `[`, `]`, `{`, `}`, `|`, `\`) are auto-converted to `substr:` for performance
- **Size-only traits:** Traits with `size_min`/`size_max` but no `if:` condition get a synthetic "always-true" condition

### Evidence Handling

- Duplicate evidence strings are automatically deduplicated
- Evidence is capped at 16 entries per trait
- Count/density constraints are applied AFTER location filtering

## CLI Reference

```bash
cleave /path/to/file                    # Analyze file
cleave facts symbols <file>             # View unified symbols (imports/exports/functions/calls/...)
cleave facts calls <file>               # View call-site records (target + args with values)
cleave facts literals <file>            # View parser-extracted string + number literals
cleave facts text <file>                # View byte-scan text runs
cleave test-rules <file> --rules "x,y"  # Debug rules
cleave test-match <file> --type literal --pattern "eval"  # Test patterns
```

### test-match Options

| Option | Values |
|--------|--------|
| `--type` | `text`, `literal`, `symbol`, `raw`, `value`, `hex`, `encoded`, `section`, `metrics`, `tree-sitter` |
| `--method` | `exact`, `contains`, `regex`, `word` |
| `--pattern` | Search pattern |
| `--encoding` | Encoding filter for `encoded` type: `base64`, `base64,hex`, etc. |
| `--count-min`, `--count-max` | Match count bounds |
| `--per-kb-min`, `--per-kb-max` | Density bounds |
| `--section` | Restrict to section |
| `--offset`, `--offset-range` | Absolute position |
| `--section-offset`, `--section-offset-range` | Section-relative position |
| `--case-insensitive` | Case-insensitive match |
| `--path` | Path for value searches |
| `--file-type` | Override detection |

## Reference Codes

- **ATT&CK**: `T1234` or `T1234.001`
- **MBC**: `B0001` (behavior), `C0015` (micro-behavior), `E1234` (ATT&CK+MBC)

## Rule Logic & Precision
- **Proximity Clusters:** Use `regex: A.{0,32}B` to detect targeted blacklists (e.g. CIS country codes) and avoid false positives in global localization libraries.
- **Script Support:** Always include `batch` and `powershell` in `for:` lists for Windows logic. Note: `shell` requires a non-Windows platform tag to pass validation.
- **Atomic vs Composite:** `if:` blocks do not support `all`/`any`. Create atomic traits and combine them using `composite_rules`.
- **ID Formatting:** Cross-file references must use `category/path::id`. Never include the YAML filename in a trait ID.
- **Tier Constraints:** `hostile` criticality is only allowed in `objectives/` and `well-known/`. `micro-behaviors/` max out at `suspicious`.

## Where to put a metric / value path

Cleave's metric pools are organized by **computation scope**, not by category.
The decision rule:

- **Format-agnostic computation** (entropy, function counts, strings, complexity —
  the same code path regardless of binary format) → `binary.*`
- **Format-specific structural data** (sections, segments, dylibs, dynamic tags —
  semantics differ per format) → `<format>.*` (`pe.*`, `elf.*`, `macho.*`)
- **Cross-format derived signal** (single bool/string that COMBINES multiple
  format-specific sources under one name — `is_pie`, `has_signature`,
  `has_executable_stack`, `entry_in_writable_region`) → `binary.*`
- **Consistency / cross-field derivation within one format** (`text_writable`,
  `bundle_identifier_mismatch`, `cert_org_pdb_mismatch`) → on the
  format-specific struct, NOT in a separate consistency pool

Value path placement:

- **Similarity / digest hashes** (imp, sym, dylib, gimp, tlsh, ssdeep, cd, authenti, …) → `hash.*` (singular namespace, terse stems)
- **Cross-format signing data** (cert.subject, cert.issuer, validity.*, time, format, catalog) → `signing.*`
- **Format-specific value** → `<format>.*` (`pe.*`, `elf.*`, `macho.*`)

**Disjoint by data kind.** `value` carries residual structured values only (strings, paths, hashes,
identifiers, structured trees, decoded named bit-flags). Metrics carry bools,
counts, and computed scalars. Every fact lives in exactly one tree — the only
acceptable cross-dimension "split" is a raw `u32` bitfield on metrics paired
with its decoded named-bit subtree in values (e.g. `pe.dll_characteristics.*`,
`macho.cs_flags.*`).
