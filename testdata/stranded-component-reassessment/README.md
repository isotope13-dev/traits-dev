# Stranded loader and Grype reassessment

The supplied wheel conviction is retained. Its `zlibxjson/main.py` member is
**MALICIOUS**, independently assessed from the complete 1,219-byte source and
wheel entrypoint. The Grype 0.112.0 conda package is **BENIGN**.

## Execution evidence

`zlibxjson_command` resolves to `zlibxjson.main:init`. Importing the package
exports this function without invoking it. `init` supplies a hardcoded Discord
EXE attachment URL and `os.getenv('APPDATA')` to the download helper. The helper
creates the destination directory when absent, strips the query from the URL
basename, streams `requests.get` response chunks into the joined binary file,
and returns that same filename. The caller hands the result to a second helper,
which calls `subprocess.Popen` with `shell=True` and `CREATE_NO_WINDOW`.
Absent APPDATA skips acquisition; launch exceptions print a diagnostic.

The sole implemented console action is an undisclosed external EXE loader,
with placeholder package provenance and no compression or JSON implementation.
This evidence tips the member verdict. There is no observed install-time launch,
persistence, credential access, exfiltration, escalation or cleanup. The expired
EXE URL returned 404 through Forager, so its downstream effects and successful
activation remain unknown. The required `--all-wheels` exact-version recovery
attempt failed after unavailable PyPI metadata and a Chromium ICU startup error;
the supplied original wheel and member hashes were verified directly.

The conda payload installs only `bin/grype`; its index, recipe, recorded binary
checksum, Go main-module information and extensive dependency/license bundle
identify the Anchore scanner. Disassembly of `main.main` at `0x275f160` builds the
Grype CLI. The `runGrype` path calls report-writer construction, parallel package
cataloging and vulnerability DB loading, then `FindMatchesContext` and report
presentation. The parallel helpers directly call `pkg.Provide` and
`LoadVulnerabilityDB`. The application-update path calls `http.NewRequestWithContext`
and `http.(*Client).do` to read a version response; it does not execute that
response. Recovered upstream v0.112.0 source has SHA-256
`0e158ac297c79a132c3d5960fe13995ecb38a7f9fc81402d8102c220600d3de8`, exactly matching
the recipe's source digest. Registry authentication, networking, cryptography,
archive handling, filesystem access and database updates fit this scanner's
purpose. No deployment or operator-authorization evidence was supplied.

## Detection corrections and preservation

Four unchanged native Go package-symbol matchers moved from compiler metadata
into `metadata/import/builtin`, with names/descriptions explicitly identifying
package-member symbol references: `go-net-http-symbol-reference`,
`go-crypto-aes-symbol-reference`, `go-crypto-cipher-symbol-reference`, and
`go-crypto-tls-symbol-reference`. A linked package is a more specific observation
than compiler identity and does not establish a particular package operation.
Their direct HTTP exfiltration exclusion now references the relocated HTTP ID.

The unchanged `go-http-header-set-string` matcher moved from generic property
assignment to `micro-behaviors/communications/http/header/set`. The build-config
consumer's alternative set explicitly retains this moved member. All five
matchers retain their exact conditions, platform/type scope, criticality and
confidence; there are no aliases or duplicate replacement matchers.

The 59 ancestor compiler selectors were inspected: they are exclusions or
contextual downgrades, not positive attack evidence. They continue selecting
compiler observations; library symbols alone are no longer treated as compiler
metadata. The compiled standard-library control retains the independent
`metadata/lang/compiler/systems::go-binary` finding and all four relocated
observations. Plain quoted package names do not supply native symbols. The
header controls distinguish `net/http.Header.Set`, `net/http.Header.Get`, and
an unrelated setter. The existing GraphAlgo RAT source still receives its five
hostile tasking, reconnaissance, self-deletion and exfiltration findings.

The existing ten linked-downloader/session/credential controls and thirteen
APPDATA/decoded-payload controls pass. They include renamed helper positives and
unrelated paths, returned values, response streams, file writes and visible
process near misses. No Python deployment behavior was removed or downgraded.

## TruffleHog false identity correction

The archive-member comparison also exposed an inaccurate TruffleHog source-package
identity on Grype's vendored Google Cloud detector directories. The required
`/detectors/` fragment identifies neither TruffleHog nor a scanner. The related
`handlers/testdata` fragment is also generic, and a PE under `decoders` is not
TruffleHog evidence. Both path matchers now require a TruffleHog-named source root;
the decoder-fixture alternative was removed from the product composite. The
independent native-decoder fixture observation remains unchanged.

Direct Telegram-token and archive-traversal consumers, and SAST directory
exclusion/downgrade consumers were inspected before narrowing. A separately
fetched Go module verified against sum.golang.org and upstream TruffleHog v3.88.0 source are kept
with provenance in scratch. Its actual detector source retains detector identity
and scanner context; its handler fixture retains the handler exception. The
existing benign package traversal-test fixture remains free of hostile findings.
A copy of the existing GraphAlgo RAT inside an unrelated `detectors` directory
retains all five hostile findings without acquiring a scanner identity. The
removed Grype observation was a false product attribution, not lost attack
coverage. No hostile or suspicious trait was weakened.

## Hostile coverage limit

The Python member retains two suspicious deployment findings and the full set
of notable acquisition, APPDATA staging, query stripping, shell execution and
window-suppression observations. Investigation of the entire source, entrypoint,
flow facts, renamed controls and downloadable stage found no additional supported
attack outcome. A generic hidden HTTP-file launch, even beside a Discord EXE URL,
also fits legitimate bootstrap/updater code; this URL's relationship to the fetch
is manually clear but the existing CDN composite only requires co-occurrence.
No shared hostile rule can honestly infer the unknown EXE's actions or the
package's deceptive purpose from these neutral primitives alone. No duplicate or
inflated hostile traits were added to meet a quota. The manual malicious verdict
therefore remains stronger than the rules/classifier.

Before/after counts, every archive-member change and model values are recorded
in `comparison.json`. Raw reports, complete facts, disassembly, consumer audit,
Forager logs and recovered source with `.forage.json` provenance are retained in
`/usr/local/var/cyclotron/tmp.noindex/cyclotron-90084b2c/scratch/stranded-analysis`.
`marker-notes.txt` contains the exact one-line judgement marker contents.

The committed TruffleHog positive-control tar contains the unmodified Abbysale
detector, a handler test ZIP and its license from the separately fetched source
archive (SHA-256 `8040dc349e9a169029c089c1cf8bd1a4e7909b420fe41308e62b9ec21560958c`).
The RAT control reuses `testdata/hostile/graphalgo-rat.go` without executing it.
Run `python3 testdata/stranded-component-reassessment/check.py` for the five
relocations; the archive controls are also registered in `testdata/expectations.toml`.
The final repository check is `make validate`, after scans and marker writes.

## Final comparison

| Artifact | Hostile before/after | Suspicious before/after | Classifier before/after |
| --- | --- | --- | --- |
| Confirmed-malicious zlibxjson wheel | 0 / 0 | 2 / 2 | BENIGN / BENIGN |
| Individually malicious main.py | 0 / 0 | 2 / 2 | BENIGN / BENIGN |
| Benign Grype conda | 0 / 0 | 0 / 0 | BENIGN / BENIGN |

All 1,359 archive analysis units were compared. The five relocated findings
retain their severity and observations. The only other loss is the false
TruffleHog product label on Grype's info archive and parent. Grype's notable
count is 506 → 505; no material attack detection is lost. Model values are
unchanged: the wheel/member have probability 0.99525124 at calibrated FP level
5000, while Grype has probability 0.32396817 outside the alert grid. The model
still misses the malicious loader. Its v18 feature specification predates v21;
Python flow facts also report incomplete queries, addressed by direct source
tracing rather than by claiming runtime success.
