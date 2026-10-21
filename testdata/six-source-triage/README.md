# Source triage: Google Cloud metadata, six, and ShopMagic

All three submitted artifacts are **BENIGN** on the balance of their contents,
execution paths, packaging and upstream comparisons. Their supplied SHA-256
values were independently verified. No original sample was executed.

## af53c5409959 — Google Cloud Go repository metadata

The 158,121-byte JSON document is a catalog of 348 Go client libraries. Every
record contains exactly eight string fields: API short name, distribution name,
description, language, client-library type, documentation URL, release level and
library type. Every distribution name equals its enclosing key; all languages
are Go. All 348 URLs have the canonical
`https://cloud.google.com/go/docs/reference/cloud.google.com/go/` prefix.
There are no executable hooks, dependency downloads, encoded payloads or code
fields. Full parsing and the facts views found no additional encoded content.

[Google's repository documentation](https://raw.githubusercontent.com/googleapis/google-cloud-go/main/internal/README.md)
explains that `internal/gapicgen/generator` generates this catalog for external
package-list tools. A fetched
[historical catalog](https://raw.githubusercontent.com/googleapis/google-cloud-go/7656129e1cffbfb788d849f3b35c28c7ac69054f/internal/.repo-metadata-full.json)
shares 280 entries, 256 byte-for-byte equivalent as parsed records. The differing
catalog versions do not establish an exact upstream revision for this specimen.
The accessapproval and storage documentation pages were fetched in full and
contain the expected official API documentation. All 348 listed URLs were also fetched with a 128 KiB response cap: every
request returned HTTP 200 and remained on docs.cloud.google.com. Response
prefixes and titles are recorded in the scratch evidence.
These are documentation references, not runtime endpoints or dependencies.

The external malware label has no behavioral support in this file. Possible
explanations include a label inherited from a containing artifact or cloud/API
vocabulary triggering broad heuristics; the source's labeling rationale and
original containing package were not supplied. No trait change was needed.

## 1c61d71502a8 — vendored six 1.16.0 compatibility module

The entire 34,581-byte source was compared with
[six's 1.16.0 release](https://raw.githubusercontent.com/benjaminp/six/1.16.0/six.py).
There is exactly one changed line: the UserDict MovedAttribute mapping specifies
`IterableUserDict` for Python 2 and `UserDict` for Python 3. Tracing the constructor
shows these are attribute selectors, not executable source or an extra loader.
Everything else matches the release source, including import-time statements.
The original parent package is unknown; the filename is consistent with vendoring.

The actual paths explain the sensitive-looking operations:

- `_SixMetaPathImporter` registers namespaced six.moves proxies. Descriptor
  resolution imports the version-appropriate standard-library module and caches
  the requested attribute. Strings naming HTTP clients, servers and subprocess
  are compatibility mappings; they do not create a server or launch a process.
- `sys.meta_path.append(_importer)` installs this in-process import finder. Its
  lookup accepts only the registered names; this is not durable persistence.
- On Python 3, `exec_` resolves the builtin exec. Import-time exec_ defines the
  fixed `raise_from` helper. On Python 2 the exec wrapper implements caller
  namespaces and defines the fixed `reraise` helper. Neither path obtains code
  from a network, credential store or hidden blob. The exported exec_ API can
  execute caller-supplied code, as its documented compatibility purpose requires.
- Reflection, frame access, metaclasses, iteration, print wrappers, and text/byte
  conversion implement the compatibility API. The facts extractor's sole
  Base64-decoded lead comes from `MERCHANTABILITY` in the license, not a decoder
  or payload. There is no runtime Base64 decoding here.

The contents and release comparison tip the verdict. A malware package could
vendor this same benign module, but no parent package or deployment context was
provided. The external label may reflect that association, or broad exec/import
hook heuristics. These are hypotheses, not established provenance.

Trait changes require a real HTTPBasicAuthHandler call and real HTTP-server
imports rather than names stored in the proxy tables. The print observation now
requires a subprocess argument list; builtin lookup is no longer called a CLI
subcommand. The redundant eval/exec/compile getter atom, misplaced under OS API
resolution, is covered by the existing canonical reflection getter trait; its
unreferenced pure-OR grouping was removed. No YAML consumers reference either
removed ID, and no ancestor directory selectors select the changed namespaces.
The unrelated getter atoms retain their existing definitions. Removed the
incorrect B0024 mapping (single-instance execution) from Python hook observations.
No hook observation in that file requires a second-instance guard.

The six identity now requires the module-level importer class, find_module and
load_module methods, and with_metaclass helper. It works under vendored filenames
and does not suppress any capability. There were no consumers of the replaced
basename identity. Reflection already had 100 rules; consolidation avoids an
unnecessary additional getter trait or a directory split.

## b2faf006fb64 — ShopMagic newsletter form JavaScript

The 1,986-byte minified script is byte-identical to WordPress's
[ShopMagic lists-form.js distribution](https://plugins.svn.wordpress.org/shopmagic-for-woocommerce/trunk/dist/lists-form.js).
The original
[TypeScript](https://plugins.svn.wordpress.org/shopmagic-for-woocommerce/trunk/assets/js/lists-form.ts)
and [PHP shortcode registration](https://plugins.svn.wordpress.org/shopmagic-for-woocommerce/trunk/src/Marketing/Subscribers/SubscriptionFormShortcode.php)
were fetched and inspected, as were the plugin manifest and readme.

The initial IIFE exposes `window.ShopMagic.shortcodeForm`; calling that API
selects and validates one HTML form and its message container, then attaches a
submit handler. The handler prevents default submission, sends that form's
FormData by HTTP POST to `shopmagic_form.ajax_url`, parses the JSON response and
shows a text message with success/error classes. It assigns `innerText`, not
executable HTML. The generator/Promise helper implements compiled async/await;
it does not evaluate generated source. No other network request or sensitive
source is present.

Upstream PHP registers `wp-i18n` for the translation helper and initializes the
URL with `admin_url('admin-ajax.php')`. Thus the fetched integration explains the
network operation as the plugin's newsletter subscription workflow. The isolated
sample does not include the deployed site's configuration, so its actual runtime
URL cannot be recovered; no external destination is hardcoded in this artifact.
Byte identity and the complete intended data flow support BENIGN. Possible
external-label explanations are containing-package association or generic
minified form-POST heuristics; the labeling rationale is unavailable.
No trait change was needed: HTTP POST, FormData and JSON response capabilities
remain notable.

## Verification

Run `python3 testdata/six-source-triage/verify.py` for positive API/argv calls and
negative string-only references, quoted source, and an incomplete identity.
The synthetic controls are parsed, never executed. The original six sample was
also checked with test-rules as the positive identity fixture.

Fresh `atomscan --no-update --mode slow --format json <sample>` runs used this
checkout through CLEAVE_TRAITS_DIR. Each emitted zero suspicious and zero hostile
traits. six's identity and actual exec/import/reflection/encoding observations
remain; the false handler/server/CLI observations disappear. ShopMagic retains
its notable network operations. Verdicts are based on the preceding manual
analysis and provenance checks, not these scan labels. The scanners report
limited flow graphs on Python and JavaScript; full source review and the upstream
diffs supply the missing control-flow context.

Raw facts, before/after scans, fetched sources, and the URL fetch log are under
`/usr/local/var/cyclotron/tmp.noindex/cyclotron-98e79cc7/scratch/triage-three/`.
The three judgement markers are adjacent to the original sample paths.
