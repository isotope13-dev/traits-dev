# @browserless/goto 6.14.3 version drift

Verdict: **BENIGN**. The release refreshes an adblock filter database; it does
not add geolocation calls or an analysis gate. No deployment context was
provided. Package purpose, unchanged application code, registry-matching archive
content hashes, and decoded filter semantics tip the judgment.

## Provenance and decisive comparison

The supplied npm archive is @browserless/goto 6.14.3, SHA-256
`ebe4a1239fd13d17a934f04c2925896d9e82c7d006816c0c1b1a1b7458559722`.
The previous published package release is 6.12.6, SHA-256
`af58173d565d5f5b5e0fa78bcac254acf806e50f76c1442d18b6dee060a9f8f8`.
Both archives match their npm registry SHA-512 integrity fields. Forager fetched
the original prior tarball; its artifact and `.forage.json` remain in the
session scratch directory `goto-review/previous/npm/`. Version 6.14.2 is a
monorepo changelog comparison tag, not a published version of this package;
registry metadata and Forager recovery found no such package release.

`src/index.js`, `scripts/postinstall.js`, and LICENSE are byte-identical.
Manifest changes are the version/gitHead, @cliqz/adblocker-puppeteer
~1.13.1 -> ~1.14.1, and tldts ~5.6.19 -> ~5.6.23. The changelog adds a
version-bump-only entry. The remaining change is `src/engine.bin`:

| Asset | 6.12.6 | 6.14.3 |
| --- | --- | --- |
| Size | 5,327,175 bytes | 5,426,747 bytes |
| Engine serialization version | 51 | 97 |
| String compression | enabled | disabled |
| Network filters | 66,720 | 64,696 |
| Cosmetic filters | 93,940 | 61,082 |

The old shipped asset needs the format-51 decoder in @cliqz/adblocker 1.9.2;
the declared ~1.13.1 library uses format 89. The refreshed asset decodes with
@cliqz/adblocker 1.14.1. Both stored integrity checks pass. The old asset's
compressed domains become plaintext in the new serialization. Both contain the
same third-party block filters for geoplugin.net, ip-api.com, ipapi.co, and
ipinfo.io, plus site-scoped allow exceptions. These references are not new
network destinations introduced by this release.

## Execution and effects

At package load, index.js reads the asset and passes its bytes to
PuppeteerBlocker.deserialize. The exported goto helper enables the engine's
request interception when adblock is enabled, then navigates to the caller's
URL. In the dependency, onRequest converts the browser request, calls match,
and aborts matching requests with blockedbyclient; redirect resources are
served as replacement responses. Main-frame navigation continues normally.
Offline calls to match for all four flagged service URLs, as third-party XHRs
from example.org, return match=true with the corresponding block filter.

The asset is serialized data, not an executable Node module. Its 205 replacement
resources include 191 JavaScript stubs/scriptlets; none contains an HTTP URL or
fetch/XMLHttpRequest/sendBeacon/WebSocket/eval operation. Their anti-tracking
DOM/property hooks explain the embedded JavaScript. The other application
functions manipulate viewport, headers, cookies, media settings and page
content, or inject caller-supplied scripts/styles as expected for browser
automation. The existing install hook fetches the library's filter subscriptions
via got and writes the serialized engine. No newly added process execution,
credential export, persistence, or geographic execution gate was found.

## Trait correction and consumers

The three old geofencing composites require only host references. Proximity
cannot turn blocklist records into API calls or establish anti-analysis intent.
Their match populations, platforms, file types, exclusions, cardinalities and
2,000-byte proximity condition are preserved under the neutral
micro-behaviors/communications/http/ip-discovery leaf:

| Old local ID under objectives/anti-analysis/geofencing/network | New local ID under micro-behaviors/communications/http/ip-discovery |
| --- | --- |
| primary-public-geo-api-cluster | ip-api-ipwho-ipinfo-cluster |
| secondary-public-geo-api-cluster | ipapi-geoplugin-pair |
| multi-public-geo-api-check | multi-public-geo-api-references |

All three now describe service references and are notable. Only the third was
suspicious before; that severity and the anti-analysis ATT&CK/MBC mappings were
unsupported by its required evidence. The first two retain their criticality.
The country-gate objective now references the relocated third rule and retains
its independent region-context requirement and hostile severity. No other
exact or ancestor objective selectors consumed the moved composites. The
site-rank-table forbidden expectation follows the new ID.

The destination's directory consumers are in host-recon-post.yaml,
oob-cooccurrence.yaml, remote-access.yaml, ip-lookup.yaml, and host-bound/source.yaml.
Every new composite requires at least two existing endpoint atoms. Those
consumers already select those atoms, with thresholds at most two; relocation
adds no new provider or evidence offset that could newly satisfy them. The
existing multi-ip-discovery and ip-geolocation-service rules remain unchanged.

Before editing, the shared rule, consumers, site-ranking regression, and the
independently reviewed fake-wallet export/local-only/renamed fixtures were
inspected. The fake-wallet source is outside this sample batch and binds
imported/generated seed words to a JSON POST with geolocation. Its two hostile
export findings are retained, including after helper/endpoint renaming.

## Verification and losses

Run `CLEAVE=<current-cleave> python3 testdata/triage/goto-version-drift/check.py`.
All seven cases pass: reference-only catalog; repeated single primary provider;
country execution gate; existing distant ranking table; imported/generated
wallet theft; renamed wallet theft; local-only wallet import. The country-gate
objective remains hostile, with measured precision 6.0. The catalog is notable,
and duplicating one provider cannot satisfy the two-provider requirement.

Atomscan before/after scans include the archives, all analyzed members, and
registry metadata. In 6.14.3 the only removed IDs are the three mapped above;
all other findings and severities are unchanged. Their three replacements are
present on both the archive and engine.bin. Suspicious/hostile counts become
zero. Measured risk scores: archive 86 -> 49; engine.bin 72 -> 35. Application
and install-hook member scores stay 11 and 7. The older archive remains 32,
with engine.bin 18 and no suspicious/hostile findings.

The calibrated ML verdict remains benign (class 0, level -1) before and after.
Aggregate raw probability changes 0.853771 -> 0.732900; the npm-specific model
changes 0.019234 -> 0.027873. The engine member changes 0.000488 -> 0.000065.
The elevated aggregate raw score remains a calibration/model observation,
not evidence for restoring the unsupported anti-analysis claim. No supported
attack behavior was removed; country gating and both wallet-export outcomes
are retained. Scans used CLEAVE_VALIDATE=0 because the installed Atomscan's
embedded validator predates the documented naming-leaf 101-rule budget.
Final full validation uses the current Cleave release binary, which admits it.
