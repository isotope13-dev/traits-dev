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
| `text` | Extracted strings (binaries) or raw text (source) | `exact`, `substr`, `regex`, `word` | count, density, location, `case_insensitive`, `is` |
| `string_literal` | AST-backed string literals only (source) | `exact`, `substr`, `regex`, `word` | count, density, location, `case_insensitive`, `is` |
| `raw` | Raw file bytes | `exact`, `substr`, `regex`, `word` | count, density, location, `case_insensitive`, `is` |
| `symbol` | Imports/exports/forwards/functions | `exact`, `substr`, `regex` | `platforms`, `is`, `kind` |
| `hex` | Byte patterns (wildcards always extracted) | pattern string | count, density, `offset`, `offset_range`, `arch` clamped in fat binaries |
| `encoded` | **All decoded strings** | `exact`, `substr`, `regex`, `word` | count, density, location, `encoding`, `case_insensitive`, `is` |
| ~~`base64`~~ | *(removed — use `encoded`)* | | |
| ~~`xor`~~ | *(removed — use `encoded`)* | | |
| ~~`string_value`~~ | *(removed — use `text`)* | | |
| ~~`string_count` / `string_value_count`~~ | *(removed — use `metrics: binary.string_count` or a `type: text` trait with `count_min`)* | | |
| ~~`exports_count`~~ | *(removed — use `metrics: binary.export_count`)* | | |
| ~~`import_combination`~~ | *(removed — use `symbol kind: import` plus composite `all`/`any`/`needs`)* | | |
| ~~`structure`~~ | *(removed — express file-format and arch gates via trait-level `for:`/`arch:`, or check `elf.e_machine`/`macho.cpu_type`/`pe.machine` via `metrics`)* | | |
| `kv` | Manifest data | `exact`, `substr`, `regex` | `path`, `exists`, `size_min`, `size_max`, `case_insensitive` (value only) |
| `basename` | Filename | `exact`, `substr`, `regex` | `case_insensitive` |

**Matcher notes:**
- `word` - Word boundary match (equivalent to `\b{value}\b`). Available on `text`, `string_literal`, `raw`, `section`, `encoded`. NOT available on `symbol`, `basename`, `hex`.
- `is` - High-fidelity validator for common data patterns. Supported values:
  - `external_ip`: Only match if evidence contains a valid external IPv4 (rejects RFC1918, loopback, reserved).
  - `bitcoin_addr`: Only match if evidence contains a valid Bitcoin address (P2PKH, P2SH, or SegWit) with a valid checksum.
- **Symbol normalization:** Leading underscores are stripped from both loaded symbols and `exact`/`substr` patterns for cross-platform portability (macOS `_malloc`, glibc `__libc_start_main` both match `exact: "malloc"` / `exact: "libc_start_main"`). Regex patterns are not normalized.
- **`kind:` filter on `symbol`:** restrict matching to one category — `import`, `export`, `forward` (PE re-exports only), or `function` (internal functions recovered by disassembly). Omitting `kind:` matches across imports, exports, and functions as before. When `kind: forward`, the pattern is tested against both the export name *and* the forward target (`KERNEL32.LoadLibraryA`), so rules can filter either side of the re-export edge. Use `kind: import` + composites for per-import set/count queries (what `import_combination` used to do in one block).

**Which one should I use?**
- Use `text` by default for human-readable content.
- Use `string_literal` only when you specifically mean AST-backed string literals in source/script languages.
- Use `raw` when you need comments, byte-precise offsets/ranges, or matches that can cross string boundaries.
- Prefer `symbol` for simple API/function/method call detection in source and binaries when cleave extracts it cleanly. It is usually the fastest search type, and is often less brittle than AST or broad text regexes for calls like `fetch`, `appendChild`, `FormData`, `querySelectorAll`, or `document.getElementById`.
- Before writing AST for simple calls, check `cleave symbols <file>` to see whether the needed calls are already exposed as symbols.
- Use `ast` when the behavior depends on structure rather than just the presence of a call: argument relationships, assignment shape, control flow, object construction, chained access patterns, or other syntax that `symbol` cannot express precisely.


### Structural

| Type | Purpose | Fields |
|------|---------|--------|
| `ast` | Parse source | `kind`/`node`, `exact`/`substr`/`regex`/`query` (tree-sitter S-expression) |
| `syscall` | Direct syscalls | `name`, `number`, `arch` (all optional, OR within field, AND across fields) |
| `section` | Binary sections | `exact`, `substr`, `regex`, `word`, `case_insensitive`, `length_min`, `length_max`, `entropy_min`, `entropy_max`, `readable`, `writable`, `executable`, `compare_to` (default: "total"), `ratio_min`, `ratio_max` |
| `metrics` | Code metrics | `field` (e.g., `identifiers.avg_entropy`, `binary.text_to_file_ratio`, `binary.data_to_file_ratio`, `binary.rsrc_to_file_ratio`, `binary.string_count`, `elf.e_machine`), `min`, `max`, `min_size`, `max_size` |
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
```

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

### AST Kinds

`call`, `function`, `class`, `import`, `string`, `comment`, `assignment`, `return`, `binary_op`, `identifier`, `attribute`, `subscript`, `conditional`, `loop`

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

Available on `text`, `string_literal`, `raw`, `encoded`. Hex supports `offset` and `offset_range`.

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
    id: objectives/impact/cryptojacking/miner::stratum-tcp
    # No section, count, downgrade, unless, etc.
```

If you need a short name for use in composite rules, reference the original trait directly instead:

```yaml
# ✅ GOOD: Reference directly in composite
composite_rules:
  - id: miner-indicators
    any:
      - id: objectives/impact/cryptojacking/miner::stratum-tcp
      - id: objectives/impact/cryptojacking/miner::stratum-ssl
```

## Exception Directives

| Directive | Purpose |
|-----------|---------|
| `not:` | Filter matched strings (list of `exact`/`substr`/`regex`) |
| `unless:` | Skip if condition matches (trait refs or inline conditions) |
| `downgrade:` | Reduce criticality by one level if condition matches |

**Proximity (composites only):** `near_bytes: N`, `near_lines: N` - require evidence from different conditions to fall within a single span of N bytes/lines. Uses a sliding window: the check passes when any contiguous window of size N contains evidence from enough distinct conditions (all conditions for `all:`, `needs` conditions for `any:`).

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
type: kv
path: service.exec_start
regex: "^/tmp/"

# .desktop: Exec= invokes shell
type: kv
path: desktop_entry.exec
regex: '\bbash\s+-c\b'

# .desktop: GNOME autostart enabled
type: kv
path: desktop_entry.x_gnome_autostart_enabled
exact: "true"

# .desktop: Categories contains a specific tag
type: kv
path: desktop_entry.categories
exact: Utility

# .desktop: secondary [Desktop Action <name>] section
type: kv
path: desktop_action_new_window.exec
exists: true
```

Localized keys (`Name[cs]=...`) are dropped during parsing; only the base
key (`name`) is exposed. Use `cleave kv <file>` to dump the full path map
for any structured file while authoring traits.

### Value Matching

Path-only (no matcher) = existence check.

```yaml
# Existence check (field must exist)
type: kv
path: "description"

# Explicit existence check
type: kv
path: "description"
exists: true              # Field must exist

# Non-existence check
type: kv
path: "description"
exists: false             # Field must NOT exist

# String matching
type: kv
path: "scripts.postinstall"
substr: "curl"            # Contains substring

# Exact match
type: kv
path: "license"
exact: "MIT"              # Exact string match

# Regex match
type: kv
path: "version"
regex: "^0\\.0\\.0$"      # Version is 0.0.0
```

### Collection Size Constraints

Constrain collection size (array elements or object keys):

```yaml
# Exactly one maintainer
type: kv
path: "maintainers"
size_min: 1
size_max: 1

# At least 3 dependencies
type: kv
path: "bundledDependencies"
size_min: 3

# No more than 10 keywords
type: kv
path: "keywords"
size_max: 10

# Empty array/object
type: kv
path: "contributors"
size_max: 0
```

**For objects:**

```yaml
# At least 5 dependencies
type: kv
path: "dependencies"
size_min: 5

# No dependencies
type: kv
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
cleave symbols <file>                   # View symbols
cleave strings <file>                   # View strings
cleave test-rules <file> --rules "x,y"  # Debug rules
cleave test-match <file> --type string-value --pattern "eval"  # Test patterns
```

### test-match Options

| Option | Values |
|--------|--------|
| `--type` | `string-value`, `symbol`, `raw`, `kv`, `hex`, `encoded` |
| `--method` | `exact`, `contains`, `regex`, `word` |
| `--pattern` | Search pattern |
| `--encoding` | Encoding filter for `encoded` type: `base64`, `base64,hex`, etc. |
| `--count-min`, `--count-max` | Match count bounds |
| `--per-kb-min`, `--per-kb-max` | Density bounds |
| `--section` | Restrict to section |
| `--offset`, `--offset-range` | Absolute position |
| `--section-offset`, `--section-offset-range` | Section-relative position |
| `--case-insensitive` | Case-insensitive match |
| `--kv-path` | Path for KV searches |
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
