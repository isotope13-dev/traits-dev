# Browser export, acquisition, and cookie capabilities

This pass completes the pending seven-rule browser-export reconciliation. It
retires three unsupported hostile wrappers and moves three actual browser
exports into the resulting space. `stealer/browser` remains at **85 combined
rules**, with no exceptions or new directory levels. Four neutral observations
move to existing HTTP cookie, cookie-store, TLS, and custom-archive leaves.
The [move manifest](browser-export-final-moves.csv) gives every destination.

The original matchers, file/platform scopes, confidence, and criticality of all
seven moved rules are preserved. Eight descriptions and five moved local IDs
are clarified. The generic TLS reference loses its inherited browser-password
ATT&CK mapping. No regex repair was needed: apparent doubled escapes came from
the displayed snapshot representation, not the YAML values.

## Admission decisions

| Evidence | Home | Deciding boundary |
|---|---|---|
| Recursive browser-extension storage acquisition plus file-to-HTTP flow | `stealer/browser` | Required transmission refines local acquisition into probable export. |
| Silent browser-profile targeting, credential stores, multipart upload and cleanup | `stealer/browser` | Browser-owned data determines the source, despite multiple browser brands. |
| System cookie store, Facebook session-field sequence and TLS writing | `stealer/browser` | The conjunction supports probable cookie export; no runtime proof is claimed. |
| `SSL_write` reference alone | `communications/socket/ssl` | Generic TLS writing has no cookie subject. Existing binary symbol matchers have different scope and bodies. |
| Specialized browser-cookie reader module | `communications/http/cookies` | Capability follows the library's function, not the bundler or an artifact identity. |
| HTTP cookie-jar module marker | `communications/http/cookie-store` | Cookie storage remains distinct from the protocol's generic cookie operations. |
| PyInstaller archive-cookie read diagnostic | `data/archive/custom` | Its resource is an archive footer, not HTTP session storage. |

The archive diagnostic's provenance is visible in
[PyInstaller's archive reader](https://github.com/pyinstaller/pyinstaller/blob/develop/bootloader/src/pyi_archive.c):
it reads an `ARCHIVE_COOKIE` structure. The diagnostic keeps its existing
Python/bytecode scope; this migration does not silently add native coverage.
The taxonomy guide now states these admission and tie-breaking rules.

## Retirements and consumer preservation

The [retirement record](browser-export-final-retirements.json) stores the full
three original definitions. None had an exact consumer.

- `pyinstaller-cookie-stealer` combined bundle/module/SQLite clues without a
  required export. The specialized reader and bundle observations remain.
- `adhoc-browser-data-stealer` combined ad-hoc signing and generic libcurl use
  with alternatives. Its binary-eligible Notes path does not identify browser
  data; the other alternatives cannot match Mach-O. An inert Notes-client
  control reproduced the hostile false positive before retirement.
- `native-chromium-wallet-stealer` required a browser-store basename and a wallet
  brand, not acquisition or transmission. A two-string source control reproduced
  its hostile false positive. Both useful content clues remain independently
  visible after retirement.

The [directory-consumer audit](browser-export-final-directory-consumers.csv)
covers **59 references in 53 consumers**, including exclusions. Five Chromium
consumers need no new alternatives: both relocated exporters require a surviving
Chromium acquisition/profile rule. Likewise, the Safari exporter requires its
surviving session-field rule. The [implication record](browser-export-final-acquisition-implications.json)
identifies those dependencies; 54 valid Boolean assignments across three source
prefixes confirm existence equivalence. No new umbrella rules or aliases are
needed.

The Python collector's `needs: 3` deserves separate treatment: it already accepts
both credential-access/browser and stealer/browser, so the same relocated IDs
remain in its candidate union. Retirement intentionally removes the unsupported
wrapper from that union. Safari's exclusion retains real acquisition through the
required field rule; a generic TLS reference intentionally stops excluding an
otherwise valid multi-app finding. Spatial consumers accepting both the source
and export prefixes retain the same moved findings and evidence spans.

Sixteen exclusions explicitly retain the archive-specific diagnostic after its
move. Generic HTTP modules no longer imply PyInstaller bundling. The moved
markers were Python/bytecode-scoped, so binary-only exclusions and filesystem
consumers could not previously match them. The polyglot downgrade is binary-only
and likewise loses no eligible evidence. All changes are recorded in the
[label/exclusion record](browser-export-final-repairs.json).

The proof protects **64 original definitions**, checks effective settings and
all exact references, and verifies every receiver is leaf-only and within 85.
Changes outside this migration are recorded separately in the
[concurrent-change record](browser-export-final-concurrent-changes.json).
A concurrently introduced CPUID reference included a YAML filename in its ID;
the [incidental correction](browser-export-final-incidental-reference-fix.json)
points it to the existing trait so the catalog can load.

## Verification and limits

Twelve synthetic controls pass **33 assertions**: 31 individual findings and two
full scans proving that the former false-positive controls emit no browser-export
verdict while retaining their primitive findings. Each of the three moved exports
has a positive and a no-transport counterpart. The established stealer suite adds
**38 assertions** in 19 controls, for **71 assertions across 31 controls**.
Fixtures are scanned, never executed. See the
[fixture README](../../testdata/taxonomy/browser-export-final/README.md) and
[runner](../../scripts/check-browser-export-routing.py).

All **1,841 corpus fixtures** pass in an isolated copy restoring only the known
pre-existing shell-decoder definition; the
[isolation record](browser-export-final-validation-isolation.json) stores both
versions. The live repository retains its shell-decoder change and still fails
that PyAigis corpus check. Strict validation reports **96 diagnostics**, with
**147 oversized directories** in the shared tree. Neither the isolated pass nor
this batch is a claim that live `make validate` passes.

## Remaining audit and validator opportunities

- Audit the rest of `fs/temp/pyinstaller`: module names, archive operations,
  bundle structure and actual temporary-path use still need distinct homes.
  In particular, source `text exact` matches complete trimmed lines; native
  bootloader diagnostics restricted to Python/bytecode merit a scope review.
- Use composite file-type reachability checks to expose source-only acquisition
  legs advertised as native export. Keep semantic admission review separate:
  libcurl presence alone cannot be mechanically equated with transmission.
- Keep identical-body checking sensitive to effective scope and exclusions.
  This pass found no identical atomic matcher body requiring a merge among the
  moved rules; text references and binary symbol matchers are distinct evidence.
- Review the remaining browser-export chains for similarly unsupported source or
  transport claims. At 85 rules, any further split must follow a documented source
  or acquisition distinction, not a bundler, implementation language or platform.
