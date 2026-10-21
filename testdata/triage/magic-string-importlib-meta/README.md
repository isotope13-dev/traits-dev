# MagicString and importlib_metadata triage

All three supplied files are **BENIGN**. The conclusion follows full source
review and upstream byte comparisons, rather than scanner scores or the
absence of findings. Only the two JavaScript files require trait changes.

| SHA-256 | Identification | Verdict evidence |
| --- | --- | --- |
| `447c762cf1edd3bc7b1bbd335b6034cf82fc13aef8c0783cfd0baa403c302ed4` | MagicString 0.26.7 ES module | Exact published npm build; in-memory source edits and source maps |
| `1b23a05dbf5fab1ab9fb15ea1b03be24c5669df74c4d75618c0176f1ab244171` | MagicString 0.26.7 CommonJS module | Exact published npm build; same implementation and different module wrapper |
| `932a4c5bffb1492b68a129b45a925ce9eba98d3f88a5cd99048976dcfc82dcda` | importlib_metadata `_meta.py` | Exact published 6.8.0 source, also matching upstream 6.9.0 and 7.0.0; typing protocol stubs |

## Execution-path review

MagicString imports/requires `sourcemap-codec`, selects a Base64 encoder through
`getBtoa()`, defines classes and exports them. Selection checks browser/Node
capabilities; it neither probes analysis environments nor starts a timer.
`BitSet` indexes source positions. `Chunk` and `MagicString` split linked text
chunks, append, prepend, overwrite, move, replace, trim and clone caller-supplied
text. Bundle combines those objects. Filename options are labels used in source
maps and relative-path calculations; they do not open files.

Mapping generation walks edited/unedited chunks, tracks line and column offsets,
and passes integer segment arrays to the dependency's `encode` function.
`SourceMap.toUrl()` serializes the result as JSON and Base64-encodes it into a
`data:application/json` URL. Browser encoding uses
`btoa(unescape(encodeURIComponent(str)))`; Node uses a UTF-8 Buffer converted to
Base64. These are ordinary encoding operations. There is no encoded executable
payload, decryption, eval, subprocess creation, network transfer, persistence,
credential access or permission modification. Replacement functions and visitor
callbacks are supplied by callers; the library does not obtain or evaluate code
from a remote source. RegExp `exec` calls perform pattern matching.

The CJS and ESM bodies differ only in the dependency binding, encode-call
qualification, export assignments, strict directive, and source-map comment.
Published source maps contain the expected implementation sources; the UMD map
also embeds sourcemap-codec. The referenced GitHub project, TypeScript workaround
pull request, and MDN replacement documentation were fetched and reviewed as
reference material, rather than executable dependencies.

The sole declared runtime dependency is `sourcemap-codec: ^1.4.8`. Its published
1.4.8 package has no further dependencies. Both ES and UMD builds implement
Base64-VLQ segment encoding/decoding: a character lookup table, continuation/sign
bits, segment accumulation, and comma/semicolon separation. The UMD wrapper
selects CommonJS/AMD/global exports. Neither build fetches or executes a payload.
The package's build/test scripts are development commands, not calls made by the
sample. Actual installed dependency bytes were not provided; analysis of the
published package cannot attest to a substituted local dependency.

The Python file imports only standard-library `typing`, creates `_T`, and defines
`PackageMetadata` and `SimplePath` protocols with overload/property decorators.
Bodies consist of ellipses or docstrings. `read_text`, `joinpath`, `get_all` and
`json` describe interfaces and perform no file access, parsing, or collection.
There are no hidden imports, encoded literals, top-level payload calls or dynamic
execution. The linked importlib_metadata issue discusses typing overloads.

## Acquisition and scan evidence

On 2026-10-21, fetched registry metadata and archives directly over HTTPS and
read archive members without installing packages or executing their scripts:

- [MagicString 0.26.7 registry metadata](https://registry.npmjs.org/magic-string/0.26.7)
- [MagicString upstream](https://github.com/Rich-Harris/magic-string)
- [TypeScript export workaround](https://github.com/Rich-Harris/magic-string/pull/121)
- [String replacement documentation](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/replace)
- [sourcemap-codec 1.4.8 metadata](https://registry.npmjs.org/sourcemap-codec/1.4.8)
- [importlib_metadata 6.8.0 metadata](https://pypi.org/pypi/importlib_metadata/6.8.0/json)
- [Upstream protocol source](https://github.com/python/importlib_metadata/blob/v6.8.0/importlib_metadata/_meta.py)
- [Overload issue](https://github.com/python/importlib_metadata/issues/435)

Ran `atomscan` and `cleave facts` on every supplied file before editing and
re-ran atomscan after editing. Reviewed literals, call records, references,
value-flow limitations and the full source. No decoded payload layers appeared;
manual tracing establishes the encoding purpose. The scanner reports limited
source flow and, for JavaScript, unavailable/incomplete flow-call queries. Those
limitations were addressed by manual review and upstream comparisons, rather
than interpreted as proof of safety. Final target scans have no suspicious or
hostile traits. The Python file needs no trait edit: typing imports are accurate,
and method declarations must not become file-read behavior findings.

No deployment or parent-package provenance was supplied. An externally hostile
container or package may have included these unmodified dependencies; broad
Base64/string-manipulation heuristics are another plausible source of the labels.
Those are possible explanations, not established attribution. Their actual
source-level behavior and exact upstream matches tip the verdict toward benign;
a malicious caller or substituted dependency remains outside these artifacts.

## Trait correction and controls

Moved the single and counted JavaScript `+= identifier` observations into
`metadata/lang/source/syntax/assignment`, preserving notable severity. JavaScript
`+=` permits concatenation as well as arithmetic, so these matchers establish
assignment syntax without identifying operand types. The counted observation now
references the single canonical matcher with a four-match requirement. Its
existing HTML/JavaScript scope is retained; the single matcher now shares that
scope. HTML script-child parsing remains outside this JavaScript query, as the
HTML control documents.

Updated both exact consumers: direct-eval accumulator co-occurrence and counted
fill-buffer growth. Updated the existing AST addition/accumulator fixture
requirements and retained the AST near-miss exclusion at the new ID.
An ancestor-selector audit found no YAML selectors for the old
arithmetic branches that require replacing this member. The destination's source
syntax grouping correctly admits the moved observation; generic metadata
selection already admitted the old counted metadata observation. No new library
identity or blanket exclusion was added.

Run `python3 testdata/triage/magic-string-importlib-meta/check.py`. Controls cover
four versus three assignments, comment/string near misses, HTML query scope,
the eval consumer, and the fill-growth/DOM-output consumers. Ordinary four
concatenations must not become eval or denial-of-service findings.
