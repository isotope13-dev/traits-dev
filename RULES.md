# Cleave rule language

A rule names an observation and the evidence required to report it. A trait has
one condition. A composite combines conditions. Both can cite existing findings.
Choose the directory and criticality from the claim. [Taxonomy](TAXONOMY.md)

[Rule fields](#a-rule-file) · [Matcher index](#condition-fields) ·
[Composition](#composition) · [Exclusions](#exclusions-and-downgrades) ·
[Verification](#verification)

## Choose a matcher

Start with `cleave facts FILE`. When a parsed field proves the claim, use
`type: value` with its `path`. Rules share the extracted value. Finding the
same spelling elsewhere in the file says less.

For example, `cleave facts values /bin/ls` on macOS reports the dynamic
linker's path from a Mach-O load command. This condition tests that field.

```yaml
if: {type: value, path: macho.dyld_path, exact: /usr/lib/dyld}
```

Use `cleave facts metrics FILE` for numeric fields such as `binary.is_pie`.
Use `cleave facts calls FILE` for call sites, resolved targets, and any
recovered arguments. The available facts depend on the file.

| If the claim depends on | Start with |
| --- | --- |
| An observation another rule already makes | `id` |
| A parsed field, dependency, or named flag | `value` with `path` |
| A numeric measure or threshold | `metrics` with `field` |
| A section, symbol, import, call, or call argument | `section` or `symbol` |
| A recovered direct system call and its constant arguments | `syscall` |
| The file's name or directory | `basename` or `path` |
| A distinctive spelling anywhere in readable content | `text` |
| Its occurrence as a literal or a comment | `literal` or `comment` |
| A decoded string, raw content, or byte signature | `encoded`, `raw`, `hex` |
| Source structure the facts cannot express | `tree-sitter` |
| A byte relationship the native matchers cannot express | `yara` |

For example, `json.loads(record)` yields a call fact with target `json.loads`
and an identifier named `record` at argument zero. A comment quoting the same
line yields no call fact. Use `text` if the spelling suffices. To require the
invocation and its argument, match both on the same call as shown below.

Prefer `exact` for a whole fact, `substr` for a literal fragment, and `word`
when token boundaries matter. Use `regex` for actual variation. Narrow `for` to
the formats that carry the evidence. Reserve a live syntax-tree query or a YARA
scan for the relationship that remains. Measure expensive rules on a real file
and a near miss large enough to expose the cost.

## A rule file

```yaml
defaults:
  for: [python]
  platforms: [unix, windows]
  crit: notable

traits:
  - id: read-record
    desc: Reads a JSON record from text
    if:
      type: symbol
      kind: call
      exact: json.loads
      arg: {index: 0, kind: identifier, name: record}

  - id: write-record
    desc: Serializes a record as JSON
    if:
      type: symbol
      kind: call
      exact: json.dumps
      arg: {index: 0, kind: identifier, name: record}

composite_rules:
  - id: read-and-write-record
    desc: Nearby JSON record parsing and serialization
    near_lines: 8
    all:
      - id: read-record
      - id: write-record
```

The two calls must occur near each other. The rule makes no claim about their
order or whether the output of one reaches the other.

`defaults` is a mapping. `traits` and `composite_rules` are lists. Omit empty
sections. Indentation determines which object owns each option. Unknown keys
fail validation.

| Where | Keys |
| --- | --- |
| Defaults and both rule forms | `for platforms arch crit conf mbc attack` |
| Defaults and both rule forms | `size_min size_max` |
| Defaults and atoms only | `entropy_min entropy_max` |
| Both rule forms | `id desc ref if not unless downgrade` |
| Atoms only | `count_min count_max per_kb_min per_kb_max` |
| Composites only | `all any needs scope near_lines near_bytes` |

`desc` accepts `description`, `crit` accepts `criticality`, `conf` accepts
`confidence`, and `if` accepts `condition`. Each rule supplies its own `id`
and `desc`. A rule field replaces its file default, including a list field.
Only the fields in the first three rows can be inherited.

- `id` is local to the directory. The full ID is `directory/path::local-id`.
  All YAML files in the directory share that namespace. A filename contributes
  nothing to the ID.
- `desc` states what matched. Prefer a short verb phrase that holds for every
  passing case. `conf` is confidence in that claim, from 0 to 1, default 1.
- `crit` sets significance, default `baseline`. `component` marks incomplete
  evidence, `baseline` a nearly universal observation, and `notable` an
  observation worth seeing in a diff. `suspicious` admits plausible benign use.
  `hostile` requires attack evidence. `exception` names benign context in a
  composite. The taxonomy gives the placement constraints on these levels.
- `mbc` and `attack` are strings containing the most specific applicable MBC
  or ATT&CK ID, such as `B0015.001` or `T1056.001`. Use `none` to clear an
  inherited mapping. `ref` records a source URL or `sha256:<hash>`.
- `size_min` and `size_max` bound the file size in bytes. `entropy_min` and
  `entropy_max` bound whole-file byte entropy (0 to 8). Bounds are inclusive.
  A size-only trait can omit `if`. See [engine findings](#engine-findings) for
  the other common use of a conditionless trait.

### Targets

`for`, `platforms`, and `arch` are lists. Declare file types and platforms
directly or through defaults. Choose platforms on which the observation has
the stated meaning. Group expansion filters out incompatible file types. An
explicit incompatible type, such as `pe` with `platforms: [macos]`, is a
validation issue.

`for` takes a union of types or groups, then subtracts exclusions. For example,
`for: [binaries, -pe]` selects binary formats except PE. A quoted `'!pe'` is
equivalent. Exclusions alone start with all concrete types. The parser also
accepts comma-separated names in a list item. Give rules a positive scope.
Repository validation requires concrete coverage and flags blanket `all`.
An empty list, `none`, and `unknown` are invalid authoring targets.

Validation caps atomic rules by matcher and effective concrete file type
count. Count after defaults, alias and group expansion, and platform
filtering. Raw and hex normally allow up to three types, and AST up to two.
Use the limit reported for the matcher. Narrow the scope to the formats
that supply the evidence. When formats expose different facts, put the
format-specific matchers in separate atoms and combine them as needed.

| Group | Coverage |
| --- | --- |
| `archives` | Concrete archive and package container formats |
| `binaries` | ELF, Mach-O, PE, class, pyc, BEAM, Wasm, DEX, static libraries |
| `scripts` | Script interpreters, including shells, JCL, mIRC, and ircII |
| `source` | Compiled-language source, including TypeScript and Clojure |
| `manifests` | Manifests, lockfiles, and structured configuration formats |
| `build` | Makefile, CMake, Xcode project, Dockerfile |
| `documents` | PDF, RTF, HTML, Markdown, text, OLE, OOXML, ODF |
| `media` (`carriers`) | Image, font, audio, and video carriers |
| `images`, `fonts`, `audio` | Subsets of the media formats |

`data` is the concrete opaque-data type. `shellcode` targets headerless code.
A container type selects the container itself. Compatible archive base types can
also apply to specialized containers. Scope the member rule to its own format.

Use these names for concrete file types.

```text
7z aiff apk apk_alpine applescript asar asp avif batch beam bmp bz2 c cab
cargo.lock cargo.toml cfml chm chrome-manifest class clojure cmake composer
composer.json composer.lock conda cpan cpio cpp cran crate crx csharp data
deb desktop-entry dex dmg dockerfile dos_com egg elf elixir font gem
gemfile.lock gentoo_binpkg gif github-actions go go.mod go.sum go_module
groovy gyp gz hackage hex html ico ipa ircii iso jar java javascript jcl
jpeg json jsp kotlin lnk lua lzma macho makefile markdown mirc mp3 mp4 msi
ne nib npm nupkg objectivec oci_image odf oledoc ooxml package-lock.json
package.json pbxproj pdf pe perl pgp_signature phar php pickle pipfile.lock
pkg_macos pkginfo plist png pnpm-lock.yaml poetry.lock postscript powershell
pub pyc pyproject.toml python python-sdist rar reg registry requirements.txt
rpa rpm rpyc rtf ruby rust scala shell shellcode snap squashfs src_info
static-lib svg swift systemd-service tar tex text tiff typescript vbs vhd
vsix vsix-manifest wasm wav webp whl xbps xml xpi xz yaml yara yarn.lock zig
zip zst
```

Common aliases include `so` for ELF, `dylib` for Mach-O, `dll` for PE, `py`
for Python, `js` for JavaScript, `ole` for legacy Office, and `docx` for
OOXML. `apk` denotes Android. Alpine packages use `apk_alpine`. The explicit
spellings `ts` and `typescript` share JavaScript rule targeting. `cpp` shares
C targeting. Use `cleave facts fileid FILE` to inspect analyzer identification.

`platforms` accepts the following names. Within `unix` and `appliance` the
indented names also match their respective umbrella. Name `android` and `ios`
explicitly when they apply. Use `all` alone and only where the taxonomy permits.

```text
unix
  linux macos aix solaris freebsd openbsd netbsd dragonflybsd openwrt qnx
  esxi zos
appliance
  routeros fortios panos iosxe junos netscaler ivanti vxworks
windows android ios commodore64 apple2 vmcms sapabap zxspectrum all
```

`arch` selects the architecture of the analyzed artifact. Omission means `all`.
Names are `x86`, `x86-64`, `aarch64`, `arm`, `riscv`, `mips`, `powerpc`,
`powerpc64`, `sparc`, `m68k`, `superh`, and `s390`. Common aliases include
`amd64`, `arm64`, `riscv64`, `ppc64le`, and `s390x`. On universal Mach-O,
an architecture restriction also limits byte searches to the applicable slice.

## Condition fields

Every condition is a mapping with a `type`. A trait reference may consist of
`id` alone. The index lists the supported fields for each type. Capitalized
names stand for these field sets and have no YAML spelling of their own.

```text
PATTERN   exact substr regex
WORDS     exact substr regex word
CASE      case_insensitive
LENGTH    length_min length_max
LOCATION  section offset offset_range section_offset section_offset_range
```

```text
trait        id
value        path PATTERN eq ne match exists LENGTH CASE is not
metrics      field min max min_size max_size
symbol       PATTERN kind arg args receiver alias module_level platforms is not
import       PATTERN platforms is not
export       PATTERN platforms is not
function     PATTERN platforms is not
syscall      name number arch args
section      WORDS CASE LENGTH entropy_min entropy_max readable writable
             executable compare_to size_ratio_min size_ratio_max
             entropy_ratio_min entropy_ratio_max
path         PATTERN CASE basename dirname is
basename     PATTERN CASE is
text         WORDS CASE LENGTH LOCATION encoding platforms is not
             exclude_comments exclude_html_comments
comment      WORDS CASE platforms is not
literal      WORDS CASE LOCATION kind value radix platforms is not
             exclude_docstrings
raw          WORDS CASE LENGTH LOCATION is not
encoded      WORDS CASE LOCATION encoding is not
hex          pattern LOCATION not
tree-sitter  PATTERN CASE kind node query language
yara         source
```

`string_literal` is an alias for `literal`. YAML uses `tree-sitter` with a
hyphen. Use `encoded` for Base64 and XOR searches. The CLI has its own option
spellings. Use the YAML field names in rule files.

### Patterns and validators

Choose one pattern method. `exact` tests equality on a fact such as a symbol,
literal, or field. In a raw scan,
`exact` requires a whole trimmed line. On extracted strings it requires the
whole string. `substr` finds a literal fragment, `word` requires word
boundaries, and `regex` uses Rust regex syntax. Use single-quoted YAML for
regexes containing backslashes. Anchor a regex when the entire value matters.
Cleave preserves the matched evidence without using capture groups. Use plain
parentheses where precedence or repetition needs grouping, except under `is`.
Bound negated classes to the expected field length, for example `[^,]{1,40}`,
and simplify nested repetitions.

`case_insensitive: true` folds case on matchers that expose it. For declared
symbols (imports, exports, forwards, and functions), condition-level
`platforms` limits the lookup. Put platform gates on the rule for text,
comments, literals, and source call, member, bind, or identifier facts.
File size, count, and density also belong on the rule. Put location filters
inside the condition that finds the bytes.

`is` validates a regex's first capture group, or the matched text when the
regex has none. Write other groups as `(?:...)`. `connect to ([0-9.]{7,15})`
with `is: external_ip` validates only the address. An `exact`, `substr`, or
`word` match is fixed text, so it gives `is` nothing to test. On a call
argument `is` validates that argument's text. Use a validator when the spelling
alone admits invalid values.

| Validator | Test |
| --- | --- |
| `valid_ip` | Contains a valid IPv4 address, including private addresses |
| `external_ip` | Contains a valid external IPv4 address |
| `bitcoin_addr` | Contains a checksum-valid Bitcoin address |
| `base64` | Whole value is valid standard or URL-safe Base64 |
| `random_like` | Identifier resembles generated text |
| `sus_hostname` | A hostname or URL contains a generated-looking host label |
| `{typo_of: top-npm-packages}` | One edit from a listed name |
| `{typo_of: top-pypi-packages}` | Same check against the PyPI dataset |

`typo_of` admits an adjacent transposition and excludes listed names and known
lookalikes. `base64` accepts wrapping whitespace and optional padding. These
validators establish properties of a string. Context supplies its meaning.

## Structured facts

### Values

`value` reads a parsed field. Inspect `cleave facts values FILE` for paths and
actual types. A package dependency belongs in a manifest field match even when
the same name occurs in a README.

| Path | Selection |
| --- | --- |
| `scripts.test` | Nested object key |
| `scripts["test.unit"]` | Literal key containing a dot |
| `maintainers[0].name` | Field of the first array element |
| `content_scripts[*].matches` | Field across all array elements |
| `dependencies.*` | Values under every key |
| `package.json::name` | Archive member field in an `eq` or `ne` comparison |

A bare `path` or `exists: true` tests presence. `exists: false` tests absence.
Use `exact`, `substr`, or `regex` for content. Array content matches when an
element matches. `length_min` and `length_max` count string bytes, array
elements, or object keys. Numbers, booleans, and null have no length.
`size_min` and `size_max` are aliases here.

For `eq` and `ne`, a sibling prefix names the basename case-insensitively.
If several entries share the name, the shallowest wins. Only analyzed entries
supply values. Each operand supports one prefix. Literal and existence checks
read the current file's value tree.

`eq` and `ne` take another **path**. Either side may be sibling-qualified.
Strings, numbers, and booleans compare as trimmed, lowercase text. Missing
paths, objects, and null supply no comparable value. Arrays supply scalars.
For each right value, look for a left value that satisfies the relation.
`match: any` (default) requires one such right value. `match: all` requires
one for every right value. With one left value, `ne` and `all` mean the left
value differs from every right value.

```yaml
type: value
path: README.md::markdown.first_heading
ne: package.json::name
```

systemd and Desktop Entry expose snake_case section and key names. Known list
keys have array values. In binaries, look under `pe`, `elf`, or `macho` for
format structures, `build` for toolchain identity, `debug` for debug records,
`signing` for signer data, and `hash` for digests. Other producers expose
namespaces such as `go`, `package`, and `dwarf`. Use the actual facts on the
target format.

### Metrics

`metrics` looks up a numeric `field`. `min` and `max` are inclusive bounds
on its value. `min_size` and `max_size` constrain file bytes. A missing metric
fails even when zero would satisfy the bound. Inspect `cleave facts metrics
FILE` for available fields. Common binary measures live under `binary`.
Format-specific measures and derived consistency checks live under their format.

```yaml
type: metrics
field: binary.overlay_ratio
min: 0.9
max: 1
min_size: 4096
```

### Symbols, calls, and imports

`symbol` searches named facts. Use `kind` when the role matters. `import`,
`export`, and `function` are shorthand types for the corresponding kinds.
Use the full `symbol` form for the additional options in the index.

| Kind | Evidence |
| --- | --- |
| `import` | Imported target |
| `export` | Exported symbol |
| `forward` | PE forwarded export name or forward target |
| `function` | Function name |
| `call` | Invocation and its arguments |
| `member` (alias `attribute`) | Dotted member access |
| `bind` (alias `assignment`) | Static assignment target |
| `identifier` | Bare identifier |

Inspect `cleave facts symbols FILE` for normalized names and roles. Use dotted
call targets without parentheses, such as `json.loads`. Symbol `exact` and
`substr` normalize leading underscores as the engine does. Write regexes
against the normalized spelling. Match the actual fact when languages differ.
For call, member, bind, and identifier facts, the evaluator tests the name
pattern. A symbol-level `is` or `not` does not filter those names. For
validation of a call argument's text, put `is` under `arg`.

For `kind: import`, `alias` filters the explicit local binding. Use `alias: {}`
to require any explicit alias. Otherwise supply `exact`, `substr`, or `regex`
under `alias`. The outer pattern still matches the imported target.

For `kind: bind`, `arg: {kind: object}` tests the assigned expression shape.
Only one shape filter is available on a binding.

For `kind: call`, `arg` requires one argument to satisfy every supplied field.
`args` requires distinct arguments of the same call to satisfy all filters.
Two named fields of one keyword object can qualify when each filter explicitly
selects the index and a distinct `from.field`. If both `arg` and `args` are
given, the single filter and the list must both pass.

| Argument field | Meaning |
| --- | --- |
| `index` | Zero-based position. Omit for any argument. |
| `kind` | Shape of the argument as reported by `facts calls` |
| `value`, `radix` | Integer and source-written base (2, 8, 10, or 16) |
| `exact`, `substr`, `regex` | String or template value |
| `name`, `name_regex` | Syntactic identifier name |
| `is` | String validator on the argument's own text |
| `from` | Origin of the argument in the value-flow graph |

Argument shapes include `string`, `number`, `identifier`, `bool`, `template`,
`null`, `object`, `array`, `function`, `call`, and `expression`.
`module_level: true` requires a call in module-level code. A conditional block
can contain such a call. `false` imposes no constraint. `receiver.from` traces
the receiver of a method call. Read `cleave facts calls FILE` first and
`cleave facts flow FILE` when the claim depends on provenance.

### Value flow

Under `arg.from` or `receiver.from`, choose **one** origin selector.

| Selector | Evidence required |
| --- | --- |
| `call` | Originating call whose canonical target matches the regex |
| `value` | A contributing literal matching the regex |
| `whole_value` | A proven complete string matching the regex |
| `whole_number` | A proven complete integer equal to this value |
| `member` | A member read whose canonical path matches the regex |
| `field_exists: true` | The named field is explicitly present |
| `field_absent: true` | A concrete map provably lacks the named field |

`field` selects a named field before tracing. It is required for presence and
absence. A present field may have an unknown value. An opaque object supplies
no proof of absence. A substring from a concatenation may satisfy `value`.
Use `whole_value` and anchors to test a complete method name or mode.

With `call`, `literal` is a regex on a literal input to the originating call.
`argument` selects that input's zero-based position (default 0). Under `call`,
`value`, or `member`, `through` supplies up to 32 explicit transfer models.
Each names a `call` regex and its contributing inputs. Use `arguments` for up
to 32 indices, `receiver: true` for the receiver, or both. Model only transfers
the library makes.
Unknown expressions and missing flow data supply no evidence of origin.

```yaml
type: symbol
kind: call
exact: json.loads
arg:
  index: 0
  from:
    call: '^read_record$'
```

Producer support varies by language. For example, CFML tag attributes appear
in a keyword object at argument zero. `cfoutput:expression` denotes a template
output expression. `cffile:read-result` denotes a read result and retains the
tag's keyword object. Dynamic attributes and unmodeled control flow can leave
values unknown. A static origin establishes a possible flow.

### Syscalls

`syscall` tests statically recovered syscall sites. `name`, `number`, and
`arch` each take a list of alternatives. All supplied fields and every entry
in `args` must hold at the same site. Use the reported syscall architecture
spelling, such as `x86_64`. Numbers are architecture-specific.

An argument requires a zero-based `index`. `value` tests equality. `mask`
requires every set bit in the mask to be set in the argument. Both may apply.
An unresolved argument fails the test. Counts refer to recovered sites. A
single instruction may execute many times or never.

### Sections and paths

`section` tests the name and properties of a binary section. `length_min`
and `length_max` measure section bytes. `entropy_min` and `entropy_max` bound
section entropy. `readable`, `writable`, and `executable` accept booleans.
Combine them to test permissions on the same section.

`size_ratio_min` and `size_ratio_max` bound the sum of selected section sizes
divided by file size. To change the denominator, set `compare_to` to a regex
selecting reference sections. Omission or `total` uses file size.
`entropy_ratio_min` and `entropy_ratio_max` compare mean section entropies.
Without `compare_to`, the reference is the other sections with positive
entropy. Inspect `cleave facts sections FILE` to choose the reference.

`path` searches the file's path. `basename: true` selects its last component.
`dirname: true` selects its directory. `type: basename` is shorthand for
`type: path` with `basename: true`. A renameable filename can supply context.
An identity or behavior claim needs evidence that survives a rename.

## Text and bytes

| Type | Search unit |
| --- | --- |
| `text` | Readable source or text, extracted binary strings, decoded layers |
| `literal` | Parsed string or numeric literal |
| `comment` | Parsed source comment |
| `raw` | Undecoded file content, including bytes outside extracted strings |
| `encoded` | Decoded strings, optionally selected by encoding chain |
| `hex` | Byte pattern with optional wildcards, skips, and alternatives |

Use `text` for a spelling. Use `literal` when being a language constant is
part of the evidence, and `comment` when being a comment matters. On source,
`text` can match prose, identifiers, and quoted examples. On binaries, `raw`
can find bytes that string extraction misses. On `text` and `raw` use
`length_min` and `length_max` to bound the matched span in bytes.

- `text.encoding` accepts `any` (default, includes decoded layers) and `none`
  (undecoded content only). Plain binary text still uses extracted strings.
- `exclude_comments: true` masks parsed language comments during raw source
  searches. `exclude_html_comments: true` masks HTML and ASP.NET comments.
  Both preserve offsets. Coverage depends on the parser and search layer.
- `literal` defaults to `kind: string`. Its string matcher supports location
  and `exclude_docstrings: true` skips Python module, class, and function
  docstrings. With `kind: number`, the evaluator tests `value` (an integer),
  `radix` (its written base), or both.
- `encoded.encoding` accepts one name, a list of alternatives, or a chain.
  Omit it for all decoded strings. `base64` matches any chain containing that
  link. `[base64, hex]` accepts either. `xor+base64` requires consecutive
  links in that order. Use the spelling in the extracted evidence. Examples
  include `base64-obf`, `url`, `unicode-escape`, `base32`, `base85`,
  `utf16le`, `utf16be`, `stack`, and `wide`.

### Byte patterns

`hex.pattern` is a space-separated string. Quote it. Use a single hex matcher
when the byte relationship fits this grammar.

| Token | Meaning |
| --- | --- |
| `7F` | One literal byte |
| `??` | Any byte |
| `A?`, `?F` | High or low nibble fixed |
| `~00` | Any byte except 00 |
| `[4]`, `[2-8]` | Skip exactly four, or two through eight bytes |
| `(47 49 46 \| 50 4E 47)` | Alternative byte sequences |

An unbounded search requires at least three concrete bytes. A short signature
needs a tight offset, bounded range, or small file-size ceiling. Validation
also checks whether binary matchers require a section.

```yaml
type: hex
pattern: '7F 45 4C 46'
offset: 0
```

### Location, count, and density

On matchers with location fields, `offset` selects a file offset.
`offset_range: [start, end]` includes the start and excludes the end.
Negative offsets count back from the end. `null` leaves an endpoint open.
For example, `[-1024, null]` searches the last KiB.

`section` on a content matcher confines the search to a named section.
Section lookup permits conventional spellings such as `text` for `.text` or
`__text`. `overlay` names the trailing region beyond mapped binary sections.
`section_offset` and `section_offset_range` use the section as origin and
require `section`. Use one offset or range in each coordinate system.

For an atom, `count_min` (normally 1) and `count_max` bound occurrences.
`per_kb_min` and `per_kb_max` bound occurrences per KiB of file size. Put
these keys beside `if`. Apply location constraints first, then count the
surviving matches. Count sites with a matcher that reports occurrences.
The report may deduplicate or cap displayed evidence. Its length is a poor
proxy for the match count.

## Structural searches

### Tree-sitter

Use `tree-sitter` when a relationship in the syntax tree supplies evidence
that facts, text, and their composition cannot express. A parsed call with
a particular argument already has a fact matcher. A call required inside a
particular syntactic construct may need a tree query.

The simple form selects an abstract `kind` or a grammar-specific `node` and
tests its source text with `exact`, `substr`, or `regex`. Abstract kinds
include `call`, `function`, `class`, `import`, `string`, `comment`,
`assignment`, `return`, `binary_op`, `identifier`, `attribute`, `subscript`,
`conditional`, and `loop`. Their concrete nodes depend on the language.
Strings include their quotes. A function node includes its body. A call
includes its arguments, and `exact` can also match its extracted target name.

The query form supplies `query`, a Tree-sitter S-expression. Omit `kind` and
`node` in this form. Declare the query grammar with `language` or let
validation infer grammars from `for`. At runtime the file determines the
parse tree. Use a named node and bind a capture. A literal
predicate on a required capture can let cleave skip most of the tree.

```yaml
type: tree-sitter
language: python
query: |
  (with_statement
    body: (block
      (return_statement) @evidence))
```

This matches a return directly in a Python `with` body. Checking for both
keywords in the file would lose the nesting constraint. A query must bind a
capture to report evidence. If it uses `@evidence`, only that capture supplies
locations, and a pattern that omits it contributes no occurrence. Otherwise
captures supply locations. Each complete query match counts once.

### YARA

`yara.source` holds a complete inline rule compiled by YARA-X. Use it when
byte arithmetic or relationships between matches exceed `hex`, offsets,
counts, and composites. One fixed string or magic number needs no YARA scan.

```yaml
type: yara
source: |
  rule indexed_footer {
    strings:
      $footer = "RECORD-END"
    condition:
      filesize >= 16 and $footer at uint32(4)
  }
```

Here four bytes at offset 4 supply the little-endian offset of the marker.
A fixed `offset` cannot express that indirect address.

## Composition

`all` and `any` take lists of conditions. If both lists are present, both
must pass. `all` requires every entry. `any` requires `needs` matches,
default 1. `needs` applies only to `any`. A composite's `if` is shorthand for
a single-entry `all`. Use one form. To nest another conjunction or disjunction,
name it in a separate composite and reference its ID.

`{id: read-record}` and `{type: trait, id: read-record}` are equivalent.
A bare ID resolves in the current directory. Use `dir/path::id` elsewhere.
A directory path selects matching descendants, with an optional trailing slash.
The reference takes only `id`. To constrain an occurrence to a section, put
the restriction on its originating content matcher.

A directory reference can contribute several distinct findings to `needs`.
Replacing two required IDs under `all` with their directory lets one
descendant satisfy the rule. When several alternatives must count as one role,
group them in a named composite. Check ancestor selectors when moving rules.

### Scope and proximity

Scope determines which findings may satisfy a composite together.

| `scope` | Shared boundary |
| --- | --- |
| `leaf` | Exact analyzed unit, including a single decoded layer |
| `file` | One member file and its decoded layers |
| `nest` | One JVM class and its `$`-named nestmates, else `file` |
| `archive` | Nearest enclosing archive of any kind, else `file` |
| `package` | Nearest enclosing ecosystem package, else `file` |
| `outer` | Entire top-level analysis |

If `scope` is omitted, cleave selects it from `for` in priority order. Any
ecosystem package type selects `package`. Otherwise any archive type selects
`archive`. Otherwise `registry` selects `outer`. Everything else selects
`file`. A fetched artifact and its separately fetched registry metadata can
be joined with `outer`. A local package already has a `package` boundary.

For a file-local composite, check every concrete type declared in `for`.
Every `all` leg must be able to match that type, and `any` must be able to
produce enough matches to meet `needs`. A `policy/ft-impossible` diagnostic names a
type that cannot satisfy a required leg. Correct the composite scope or the
leg's scope according to where the evidence can actually occur.

For a composite across members, include the container **and** the evidence
types in `for`. For example, `[zip, javascript, python]` admits a ZIP and
findings in both source languages. In a package containing a nested generic
ZIP, `archive` groups the inner ZIP's members together. `package` can also
see other members of that package.

`near_bytes` and `near_lines` require qualifying locations in one window of
the given span. The window must cover the required legs and meet the `any`
threshold. Use locations from a common source when claiming proximity. A
compound finding can carry a location from only one of its constituents.
Two nearby findings do not prove order, ownership, or the direction of a flow.

### Engine findings

An engine finding can be referenced by ID just like a YAML finding. Source
imports use `metadata/import/<ecosystem>/<target>::<local-name>`. The target
is normalized to lowercase path components. An explicit local alias keeps its
spelling. Relative Python imports have a `relative/<level>/` prefix. JavaScript
imports use the `npm` ecosystem.

For `import requests as r` the full ID is `metadata/import/python/requests::r`.
Use `metadata/import/python/requests` to accept any local name. An import
establishes a dependency. Require a call fact for an invocation.

To tune an existing engine finding, define a trait at its ID with `desc` and
`unless` or `downgrade`. Omit `if` and all size, entropy, count, and density
gates on the trait. The override adjusts the emitted finding at its original
criticality and cannot produce a finding on its own.

## Exclusions and downgrades

| Directive | Operand | Effect |
| --- | --- | --- |
| `not` | List of string exceptions | Filters matching evidence |
| `unless` | List of conditions | Any match suppresses the finding |
| `downgrade` | Mapping of `all`, `any`, `needs`, `scope` | Lowers severity |

Use `not` to discard an unwanted spelling of the matched value. An exception
sees only the matched text, never the string around it. Put nearby context in
the match as an optional group: `curl\s+https?://(localhost)?` lets
`not: [localhost]` apply. A bare string
or `{substr: text}` is a case-insensitive substring. `{exact: Text}` tests
case-sensitive equality. `{regex: pattern}` uses a case-sensitive regex by
default. Use one method per exception. Matcher-local `not` is available on
the types listed in the index. Use `unless` when evidence elsewhere in the
file disqualifies the whole finding.

An `unless` condition is file-local. A downgrade also defaults to file-local.
To use wider context, name its scope. A container-scoped downgrade can join
a named container finding with an inline path condition on the matched member.
Two additional downgrade scopes are `parent` (immediate analyzed parent only)
and `file-or-parent` (the matched file or that parent).

A successful downgrade takes one step, from `hostile` to `suspicious`, from
`suspicious` to `notable`, or from `notable` to `baseline`. A demoted finding
remains reportable. Other unreferenced low-tier findings can be omitted after
evaluation. For a negative guard on a downgrade, name a context rule with its
own `unless` and reference it from the downgrade.

A `crit: exception` composite identifies benign context. Build it from named
notable findings or other exceptions. Every exception needs a consumer. A host
can suppress with `unless: [{id: vendor-updater}]` or lower severity with
`downgrade: {any: [{id: vendor-updater}]}` when that context matches.
A normal positive directory reference skips exception findings.
When a suppression relies on signer identity, cite a verified signer under
`metadata/signature/verified/`. A claimed signer name alone proves no trust.

Validation expands references when checking suppression limits.

| Check | `unless` | `downgrade` |
| --- | --- | --- |
| Distinct rules reached | At most 64 | At most 256 |
| Distinct path-only traits reached | At most 1 | At most 8 |
| Downgrade on a `notable` rule | — | At most 4 direct and 8 expanded |

A separate check flags 10 direct suppressor entries or 48 entries after
expanding aggregator composites across a rule's own `unless` and `downgrade`.
A large exclusion list is a reason to revisit what the positive matcher proves.

## Verification

Inspect the fact that supplies the evidence, then run the finished rule on a
positive case and a near miss. For the opening example, compare a call that
takes `record` with an otherwise identical call that takes `other`. Include a
comment quoting the positive call. Only the invocation with the named argument
should qualify.

```sh
cleave facts calls sample.py
cleave --traits-dir . test-rules --rules "$rule_id" sample.py
cleave test-match --type text --method contains --pattern 'record' sample.py
make validate  # standalone changes
```

`test-match` probes individual search methods. `test-rules` evaluates the
authored YAML and shows conditions, evidence, downgrades, and precision.
Hostile composites have an authoring bar of 3.5 precision. The engine computes
the score. Use it alongside benign controls. A passing validator alone cannot
establish the rule's claim.

`make validate` checks the repository rules and labeled fixtures with the
selected cleave binary. Run it from the complete checkout. Select changed rules
and their consumers with `test-rules --rules` while keeping the complete trait
registry loaded. Use the [validation and fixture instructions](README.md#validation)
when adding samples or recording a baseline failure. Unknown matchers and
fields fail validation. During normal scanning, a build that supports
forward-compatible loading skips an unparseable rule file with a warning.
Use the build that will run the rules.

Validation checks regex cost, AST grammar and query cost, and whole-rule
runtime. The normal regex review limits are 90 bytes and three alternations
outside character classes. Bound repetitions to the evidence. Express literal
alternatives as reusable findings when each has independent meaning. For
performance work, `make validate-profile` runs fresh measurements. Compare the
cost of equivalent rules on the same inputs. [Repository checks](README.md)
